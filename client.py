import socket

host = '127.0.0.1'
port = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((host, port))
    print("Connected to server")

    while True:
        msg = input("You: ")
        client.send(msg.encode())

        data = client.recv(1024)
        print("Server:", data.decode())

except Exception as e:
    print("Error:", e)

finally:
    client.close()
    print("Disconnected")