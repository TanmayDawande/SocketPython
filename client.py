import socket
import struct
import sys

host = '127.0.0.1' 
port = 65432

def pack(var):
    packed = struct.pack("!I", len(var.encode('utf-8')))
    return packed+var.encode('utf-8')
    # Creating a packet where first bits are the length of the message
    # ! is for standard network byte order and I is for unsigned int

def generate_cyphertext(message, N, e):
    message_bytes = message.encode('utf-8')
    M = int.from_bytes(message_bytes, byteorder='big')
    # print(f"{pow(M, e, N)}") debugging
    return f"{pow(M, e, N)}"


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((host, port))
    header = client_socket.recv(4)
    header_decoded = struct.unpack("!I", header)
    recieved_keys = client_socket.recv(header_decoded[0])
    N_and_e = recieved_keys.decode('utf-8')
    split_keys = N_and_e.split(',')
    N = int(split_keys[0])
    e = int(split_keys[1])
    
    client_socket.sendall(b'1')
    print("(+) Client Handshake successful! Commensing chat")
    while True:
        message = input("message: ")
        client_socket.sendall(pack(generate_cyphertext(message, N, e)))
        print("(+) Message sent to server...")
        print("(+) Waiting for the message...")


        data_bits_struct = client_socket.recv(4)
        data_bits = struct.unpack("!I", data_bits_struct)
        data = client_socket.recv(data_bits[0])
        print(f"reply: {data.decode('utf-8')}")

print("(+)Connection closed")