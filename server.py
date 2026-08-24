import socket
import struct
import rsa_encrypt
import sys

host  = '127.0.0.1'
port = 65432

def pack(var):
    packed = struct.pack("!I", len(var.encode('utf-8')))
    return packed+var.encode('utf-8')
    # Creating a packet where first bits are the length of the message
    # ! is for standard network byte order and I is for unsigned int

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"(+) Start listening on {host} and port {port}")
    conn, addr = server_socket.accept()
    with conn:
        print(f"(+) Connected by {addr}")
        print("(+) Performing RSA Handshake...")

        N = rsa_encrypt.N
        e = 65537
        key_string = f"{N}, {e}" #this is called string interpolation
        conn.sendall(pack(key_string))
        print("(+) Waiting for ACK...")
        flag = conn.recv(1)
        if(flag == b'1'):
            print("(+) Server Handshake established! Commensing chat")
        else:
            sys.exit("(+) Handshake failed exiting now...")

        while True:

            data_bits_struct = conn.recv(4)
            data_bits = struct.unpack("!I", data_bits_struct)
            data = conn.recv(data_bits[0])
            if not data:
                break
            if data.decode('utf-8') == "Close":
                break

            print(f"message: {data.decode('utf-8')}")
            message = input("reply: ")
            print("(+) Waiting for the message...")
            conn.sendall(pack(message))

print("(+) Connection Closed")
