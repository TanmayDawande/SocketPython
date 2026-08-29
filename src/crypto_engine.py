import math
import rsa_encrypt

def generate_cyphertext(message, N, e):
    message_bytes = message.encode('utf-8')
    M = int.from_bytes(message_bytes, byteorder='big')
    # print(f"{pow(M, e, N)}") debugging
    return f"{pow(M, e, N)}"

def decrypt(C, N, d):
    C = int(C)
    # print(C) debugging 
    M_decrypted = pow(C, d, N)
    bit_length = math.ceil(M_decrypted.bit_length() / 8)
    #this calculates the bytelehgth which is needed in the to_bytes
    decrypt_bytes = M_decrypted.to_bytes(bit_length, byteorder="big")
    return decrypt_bytes.decode('utf-8')
