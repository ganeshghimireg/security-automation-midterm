import socket

target = input("Enter target (127.0.0.1 or scanme.nmap.org): ")

try:
    start_port = int(input("Start port: "))
    end_port = int(input("End port: "))

    print(f"\nScanning {target}...\n")

    for port in range(start_port, end_port + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)

        result = s.connect_ex((target, port))

        if result == 0:
            print(f"Port {port} is OPEN")
        else:
            print(f"Port {port} is CLOSED")

        s.close()

except ValueError:
    print("Invalid port number!")

except socket.gaierror:
    print("Hostname could not be resolved!")

except socket.error:
    print("Could not connect to server!")