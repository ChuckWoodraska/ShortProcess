import psutil
from typing import List, Dict, Any

class ProcessMonitor:
    @staticmethod
    def get_processes() -> List[Dict[str, Any]]:
        """
        Retrieves a list of running Python processes and Docker containers.
        """
        process_list = []
        
        # 1. Get Python processes from psutil
        for p in psutil.process_iter(['pid', 'name', 'status']):
            try:
                name = p.info['name'].lower()
                if 'python' in name:
                    connections = p.connections(kind='inet')
                    ports = [conn.laddr.port for conn in connections if conn.status == psutil.CONN_LISTEN]
                    
                    try:
                        cmdline = " ".join(p.cmdline())
                    except (psutil.AccessDenied, psutil.ZombieProcess):
                        cmdline = p.info['name']
                    
                    if not cmdline:
                        cmdline = p.info['name']

                    # Split into process name and arguments
                    # Simple heuristic: first part is process, rest is args
                    parts = cmdline.split(' ', 1)
                    proc_name = parts[0]
                    args = parts[1] if len(parts) > 1 else ""

                    process_list.append({
                        'pid': p.info['pid'],
                        'name': proc_name, # Short name
                        'image': "",       # No image for local processes
                        'arguments': args, # Arguments
                        'status': p.info['status'],
                        'ports': ports
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        # 2. Get Docker containers from docker CLI
        process_list.extend(ProcessMonitor.get_docker_containers())
        
        return process_list

    @staticmethod
    def get_docker_containers() -> List[Dict[str, Any]]:
        container_list = []
        import subprocess
        import json
        
        try:
            # simple format that mimics json to avoid "invalid template" issues on older dockers if {{json .}} isn't supported
            # But let's try the standard '{{ json . }}' first or a manual pipe format.
            # Using a pipe delimiter is safer for custom parsing if simpler.
            # Format: ID|Image|Names|Command|Status|Ports
            # Use --no-trunc to get the full command
            output = subprocess.check_output(
                ["docker", "ps", "--no-trunc", "--format", "{{.ID}}|{{.Image}}|{{.Names}}|{{.Command}}|{{.Status}}|{{.Ports}}"],
                text=True
            )
            
            for line in output.strip().split('\n'):
                if not line: continue
                parts = line.split('|')
                if len(parts) >= 6:
                    cid, image, name, command, status, ports_raw = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]
                    
                    # Parse ports: "0.0.0.0:9990->8000/tcp, :::9990->8000/tcp"
                    # We typically want the public facing ports.
                    # Simplistic extraction of numbers from the string or just keeping the string.
                    # The UI expects a list of ports.
                    
                    # Extracting ports like "9990"
                    ports = []
                    # Split by comma
                    port_entries = ports_raw.split(',')
                    for entry in port_entries:
                        # entry might be "0.0.0.0:9990->8000/tcp" or "80/tcp"
                        if '->' in entry:
                            # It's a mapping: 0.0.0.0:PORT->...
                            left_side = entry.split('->')[0]
                            # Find the port number in the left side
                            if ':' in left_side:
                                try:
                                    port_str = left_side.split(':')[-1]
                                    ports.append(int(port_str))
                                except ValueError:
                                    pass
                        else:
                            # Just an exposed port like "8080/tcp" usually internal if no mapping, but let's grab it if it looks like a port
                             if '/' in entry:
                                 try:
                                     port_str = entry.split('/')[0]
                                     # Filter out things that aren't numbers
                                     if port_str.isdigit():
                                        ports.append(int(port_str))
                                 except ValueError:
                                     pass

                    # Clean up command: sometimes it comes quoted like "command"
                    command = command.strip('"')

                    container_list.append({
                        'pid': cid[:12], # Shorten ID for display
                        'name': name,    # Container Name
                        'image': image,  # Image Name
                        'arguments': command,
                        'status': status,
                        'ports': ports
                    })
                    
        except Exception as e:
            # Fallback or silent fail if docker command not found or fails
            print(f"Error fetching docker stats: {e}")
            pass
            
        return container_list
