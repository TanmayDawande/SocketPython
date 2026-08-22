import socket

host  = '127.0.0.1'
port = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"(+) Start listening on {host} and port {port}")
    conn, addr = server_socket.accept()
    with conn:
        print(f"(+) Connected by {addr}")
        while True:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                if data.decode('utf-8') == "Close":
                    break

                print(f"The message is: {data.decode('utf-8')}")
                message = input("reply: ")
                conn.sendall(message.encode("utf-8"))

print("(+) Connection Closed")
