import socket
import struct
import sys
import crypto_engine as cr
import rsa_encrypt as rsae
import argparse
import os


def pack(var):
    packed = struct.pack("!I", len(var.encode('utf-8')))
    return packed+var.encode('utf-8')
    # Creating a packet where first bits are the length of the message
    # ! is for standard network byte order and I is for unsigned int

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
        N_server = int(split_keys[0])
        e_server = int(split_keys[1])
        #servers keys recieved by the client

        N_client = rsae.N
        e_client = 65537
        d_client = rsae.d
        #client's own keys that are sent to server
        key_string = f"{N_client},{e_client}" 
        #this is called string interpolation
        #learning - dont give space after comma in f"{N_client},{e_client}"
        client_socket.sendall(pack(key_string))

        print("[*] Waiting for ACK...") #ack after the client sends its keys.
        flag = client_socket.recv(1)
        if(flag == b'1'):
            print("[+] ACK recieved")
            print("[+] Server Handshake established! Commencing chat")
        else:
            sys.exit("[-] Handshake failed exiting now...")
        
        
        try:
            while True:
                message = input("[You]: ")
                client_socket.sendall(pack(cr.generate_cyphertext(message, N_server, e_server)))
                print("[+] Message sent to server...")
                print("[*] Waiting for the message...")
    
    
                data_bits_struct = client_socket.recv(4)

                #if client disconnects, an ugly error is prevented. Ai suggested this
                if not data_bits_struct:
                    print("\n[-] Server disconnected.")
                    break 

                data_bits = struct.unpack("!I", data_bits_struct)
                data = client_socket.recv(data_bits[0])
                data_decrypt = cr.decrypt(data, N_client, d_client)
                print(f"[Server]: {data_decrypt}")

        except KeyboardInterrupt:
            print("\n[!] keyboard interrupt detected. exiting now...")

        except ConnectionResetError:
            print("\n[-] connection closed by client. exiting...")

    print("[*] Connection closed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Babel-TCP Secure Client Node")
    parser.add_argument("--host", default="127.0.0.1", help="IP address to bind to")
    parser.add_argument("--port", type=int, default=65432, help="Port to listen on")

    args = parser.parse_args()
    os.system('cls' if os.name == 'nt' else 'clear')
    start_client(args.host, args.port)