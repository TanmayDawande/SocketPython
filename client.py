import socket

host = '127.0.0.1' 
port = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((host, port))
    print(f"(+) Connected to {host}:{port}")

    while True:
        message = input("Message: ")
        client_socket.sendall(message.encode('utf-8'))
        print("(+) Message sent to server...")

        data = client_socket.recv(1024)
        print(f"Message from server: {data.decode('utf-8')}")

print("(+)Connection closed")