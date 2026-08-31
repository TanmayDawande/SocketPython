import struct
import rsa_encrypt as rsae
import crypto_engine as cr
import sys

class SecureNODE:
    def __init__(self, socket):
        self.socket = socket

        self.my_N = rsae.N
        self.my_d = rsae.d
        self.my_e = 65537

        self.your_N = None
        self.your_e = None


    def _pack(self, var : str) -> bytes:
        packed = struct.pack("!I", len(var.encode('utf-8')))
        return packed+var.encode('utf-8')
        # Creating a packet where first bits are the length of the message
        # ! is for standard network byte order and I is for unsigned int

    def _unpack(self, header):
        unpacked = struct.unpack("!I", header)
        data = self.socket.recv(unpacked[0])
        return data

    def sendHandshake(self):
        key_string = f"{self.my_N}, {self.my_e}" #this is called string interpolation
        self.socket.sendall(self._pack(key_string))
    def recieveHandshake(self):
        header = self.socket.recv(4)
        header_decoded = struct.unpack("!I", header)
        recieved_keys = self.socket.recv(header_decoded[0])
        N_and_e = recieved_keys.decode('utf-8')
        split_keys = N_and_e.split(',')
        #client's keys that are recieved
        self.your_N = int(split_keys[0])
        self.your_e = int(split_keys[1])


    def pack_and_encrypt(self, message : str):
        cyphertext_msg = cr.generate_cyphertext(message, self.your_N, self.your_e)
        self.socket.sendall(self._pack(cyphertext_msg))
        
    def unpack_and_decrypt(self):
        header = self.socket.recv(4)
        if not header:
            return None
        data = cr.decrypt(self._unpack(header), self.my_N, self.my_d)
        return data