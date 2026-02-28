# Process Viewer App

A Python GUI application used to monitor Python processes and Docker containers running on your system. It displays detailed information including process IDs, command line arguments, Docker image names, and listening ports.

## Features

- **Process Monitoring**: Detects running Python processes and displays their full command line arguments.
- **Docker Monitoring**: Lists active Docker containers with their Names, Image Names, fully qualified Commands, and Port Mappings.
- **Port Detection**: Shows listening ports for both local processes and containers.
- **Modern UI**: Built with `customtkinter` for a clean, dark-mode compatible interface.
- **Manual Refresh**: Update the list on demand.

## Prerequisites

- Python 3.12+
- Docker (for container monitoring)
- X11 Server (only if running via Docker on Linux)

## Installation & Running Locally

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ShortProcess
   ```

2. **Set up environment** (using `uv` or `pip`):
   ```bash
   # Using uv (recommended)
   uv venv
   uv pip install -r pyproject.toml
   # OR install packages manually
   pip install customtkinter psutil packaging
   ```

3. **Run the application**:
   ```bash
   # From the project root
   source .venv/bin/activate  # if using venv
   python src/main.py
   ```

## Running with Docker

To monitor the *host* system from within a Docker container, you need to provide the container with specific access permissions (PID namespace, Docker socket, and X11 socket).

### 1. Build the Image

```bash
docker build -t process-viewer .
```

### 2. Run the Container

Run the following command (for Linux/X11):

```bash
docker run -it --rm \
    --net=host \
    --pid=host \
    -e DISPLAY=$DISPLAY \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    process-viewer
```

**Explanation of Flags:**
- `--net=host`: Allows the container to see host network (optional for `psutil` network connections check, but recommended).
- `--pid=host`: **Critical**. Allows `psutil` inside the container to see processes on the host machine.
- `-v /var/run/docker.sock:/var/run/docker.sock`: **Critical**. Allows the container to use the host's Docker daemon to run `docker ps`.
- `-e DISPLAY=$DISPLAY` and `-v /tmp/.X11-unix:/tmp/.X11-unix`: Required to render the GUI on the host screen.

> **Note**: You may need to allow local X11 connections if you get a "cannot connect to display" error:
> `xhost +local:docker`

## Project Structure

- `src/main.py`: Entry point.
- `src/ui.py`: GUI implementation using `customtkinter`.
- `src/process_monitor.py`: Logic for detecting processes and containers.
