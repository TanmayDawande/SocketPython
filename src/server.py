import socket
import struct
import crypto_engine as cr
import rsa_encrypt as rsae
import sys
import math
import argparse
import os


def pack(var):
    packed = struct.pack("!I", len(var.encode('utf-8')))
    return packed+var.encode('utf-8')
    # Creating a packet where first bits are the length of the message
    # ! is for standard network byte order and I is for unsigned int

def start_server(arg_host, arg_port):
    host = arg_host
    port = arg_port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"[*] Started listening on {host} and port {port}")
        conn, addr = server_socket.accept()
        with conn:
            print(f"[+] Connected by {addr}")
            print("[*] Performing RSA Handshake...")
            #server's own keys that are sent to the client
            N_server = rsae.N
            e_server = 65537
            d_server = rsae.d
            key_string = f"{N_server}, {e_server}" #this is called string interpolation
            conn.sendall(pack(key_string))

            header = conn.recv(4)
            header_decoded = struct.unpack("!I", header)
            recieved_keys = conn.recv(header_decoded[0])
            N_and_e = recieved_keys.decode('utf-8')
            split_keys = N_and_e.split(',')
            #client's keys that are recieved
            N_client = int(split_keys[0])
            e_client = int(split_keys[1])

            conn.sendall(b'1')
            print("[+] Server initialized its own keys and recieved client keys")
            print("[+] Sending ACK")

            try:
                while True:
                
                    data_bits_struct = conn.recv(4)
    
                    #catch empty buffer if provided
                    if not data_bits_struct:
                        print("\n[-] Client disconnected.")
                        break 
                    
                    data_bits = struct.unpack("!I", data_bits_struct)
                    data = conn.recv(data_bits[0])
                    data = cr.decrypt(data, N_server, d_server)
                    if not data:
                        break
    
                    print(f"[Client]: {data}")
                    message = input("[You]: ")
                    print("[*] Waiting for the message...")
                    conn.sendall(pack(cr.generate_cyphertext(message, N_client, e_client)))

            except KeyboardInterrupt:
                print("\n[!] keyboard interrupt. exiting now...")

            except ConnectionResetError:
                print("\n[-] connection was forcebly closed by the remote host")

    print("[*] Connection Closed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Babel-TCP Secure Server Node")
    parser.add_argument("--host", default="127.0.0.1", help="IP address to bind to")
    parser.add_argument("--port", type=int, default=65432, help="Port to listen on")

    args = parser.parse_args()

    os.system('cls' if os.name == 'nt' else 'clear')
    start_server(args.host, args.port)
