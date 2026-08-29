import socket
import struct
import sys
import argparse
import os


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


def start_client(arg_host, arg_port):
    host = arg_host
    port = arg_port
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
        print("[+] Client Handshake successful! Commencing chat")
        try:
            while True:
                message = input("[You]: ")
                client_socket.sendall(pack(generate_cyphertext(message, N, e)))
                print("[+] Message sent to server...")
                print("[*] Waiting for the message...")
    
    
                data_bits_struct = client_socket.recv(4)
                data_bits = struct.unpack("!I", data_bits_struct)
                data = client_socket.recv(data_bits[0])
                print(f"[Server]: {data.decode('utf-8')}")

        except KeyboardInterrupt:
            print("\n[!] keyboard interrupt detected. exiting now...")

        except ConnectionResetError:
            print("\n[-] connection closed by client. exiting...")

    print("[*] Connection closed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Babel-TCP Secure Server Node")
    parser.add_argument("--host", default="127.0.0.1", help="IP address to bind to")
    parser.add_argument("--port", type=int, default=65432, help="Port to listen on")

    args = parser.parse_args()
    os.system('cls' if os.name == 'nt' else 'clear')
    start_client(args.host, args.port)