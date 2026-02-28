import socket
import subprocess
import sys
import time
import threading
import os
from src.process_monitor import ProcessMonitor

def start_dummy_server(port, stop_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', port))
    sock.listen(1)
    # print(f"Dummy server listening on port {port}")
    while not stop_event.is_set():
        sock.settimeout(1.0)
        try:
            conn, addr = sock.accept()
            conn.close()
        except socket.timeout:
            continue
    sock.close()

def test_process_detection():
    port = 9999
    stop_event = threading.Event()
    server_thread = threading.Thread(target=start_dummy_server, args=(port, stop_event))
    server_thread.start()
    
    # Give the server a moment to start
    time.sleep(1)
    
    try:
        processes = ProcessMonitor.get_processes()
        found = False
        for p in processes:
            # We are running this test script, which is a python process
            # and we just started a thread listening on the port within this process.
            # So we expect to find *ourselves* (or the current process) listening on 9999.
            if port in p['ports']:
                found = True
                print(f"Successfully detected process: {p['name']} (PID: {p['pid']}) on port {port}")
                break
        
        if not found:
            print(f"FAILED: Could not find process listening on port {port}")
            print("Found processes:", processes)
            sys.exit(1)
        else:
            print("PASSED: Process detection working correctly.")
            
    finally:
        stop_event.set()
        server_thread.join()

if __name__ == "__main__":
    test_process_detection()
