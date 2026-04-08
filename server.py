#!/usr/bin/env python3
"""
SERVER SCRIPT - Socket Connection Implementation
Author: [Your Name]
Date: [Today's Date]
"""

import socket
import sys

def start_server(host='127.0.0.1', port=12345):
    """Start TCP server that listens for client connections."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"[✓] SERVER STARTED: Listening on {host}:{port}")
        print("[i] Waiting for client connection...\n")
        
        client_socket, client_address = server_socket.accept()
        print(f"[✓] CONNECTION ESTABLISHED: {client_address[0]}:{client_address[1]}")
        
        while True:
            data = client_socket.recv(1024)
            if not data:
                print("[!] Client disconnected unexpectedly")
                break
                 
            message = data.decode('utf-8').strip()
            print(f"[←] CLIENT: {message}")
            
            if message.lower() == 'exit':
                response = "Connection closing per client request"
                client_socket.send(response.encode('utf-8'))
                print("[✓] Closing connection gracefully")
                break
                
            response = f"Server received: '{message}' | Timestamp: {time.strftime('%H:%M:%S')}"
            client_socket.send(response.encode('utf-8'))
            print(f"[→] SERVER RESPONSE SENT")
            
    except KeyboardInterrupt:
        print("\n[!] Server stopped by user (Ctrl+C)")
    except Exception as e:
        print(f"[✗] ERROR: {type(e).__name__} - {e}", file=sys.stderr)
    finally:
        if 'client_socket' in locals():
            client_socket.close()
            print("[✓] Client socket closed")
        server_socket.close()
        print("[✓] Server socket closed\n")

if __name__ == "__main__":
    import time
    start_server()