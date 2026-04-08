#!/usr/bin/env python3
"""
CLIENT SCRIPT - Socket Connection Implementation
Author: [Ganesh Ghimire]
Date: [4/8/2026]
"""

import socket
import sys

def start_client(host='127.0.0.1', port=12345):
    """Connect to server and exchange messages."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        print(f"[i] Attempting connection to {host}:{port}...")
        client_socket.connect((host, port))
        print(f"[✓] CONNECTED to server at {host}:{port}\n")
        
        while True:
            message = input("[→] Enter message (type 'exit' to quit): ").strip()
            
            if not message:
                print("[!] Empty message not sent")
                continue
                
            client_socket.send(message.encode('utf-8'))
            
            if message.lower() == 'exit':
                print("[i] Waiting for server acknowledgment...")
                data = client_socket.recv(1024)
                print(f"[←] SERVER: {data.decode('utf-8')}")
                break
                
            data = client_socket.recv(1024)
            if not data: 
                print("[!] Server disconnected")
                break
            print(f"[←] SERVER: {data.decode('utf-8')}\n")
            
    except ConnectionRefusedError:
        print(f"[✗] CONNECTION REFUSED: Is the server running on {host}:{port}?", file=sys.stderr)
        print("[!] Start server.py FIRST before running client.py", file=sys.stderr)
    except KeyboardInterrupt:
        print("\n[!] Client stopped by user (Ctrl+C)")
    except Exception as e:
        print(f"[✗] ERROR: {type(e).__name__} - {e}", file=sys.stderr)
    finally:
        client_socket.close()
        print("[✓] Connection closed\n")

if __name__ == "__main__":
    start_client()