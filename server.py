import socket

# Server configuration
host = '127.0.0.1'
port = 9999

# Create socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Bind and listen
    server.bind((host, port))
    server.listen(1)
    print("Server listening on port", port)

    # Accept connection
    conn, addr = server.accept()
    print("Connected by", addr)

    while True:
        data = conn.recv(1024)
        if not data:
            break

        print("Client:", data.decode())

        # Send response
        response = input("Reply: ")
        conn.send(response.encode())

except Exception as e:
    print("Error:", e)

finally:
    conn.close()
    server.close()
    print("Server closed")