import socket
import struct

host = '127.0.0.1' 
port = 65432

def pack(var):
    packed = struct.pack("!I", len(var.encode('utf-8')))
    return packed+var.encode('utf-8')
    # Creating a packet where first bits are the length of the message
    # ! is for standard network byte order and I is for unsigned int


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((host, port))
    print(f"(+) Connected to {host}:{port}")

    while True:
        message = input("message: ")
        client_socket.sendall(pack(message))
        print("(+) Message sent to server...")


        data_bits_struct = client_socket.recv(4)
        data_bits = struct.unpack("!I", data_bits_struct)
        data = client_socket.recv(data_bits[0])
        print(f"reply: {data.decode('utf-8')}")
        print("(+) Waiting for the message...")

print("(+)Connection closed")