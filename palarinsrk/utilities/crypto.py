'''
Created on Feb 16, 2014

@author: noskillz
'''
from Crypto.Cipher import AES
from Crypto import Random
import binascii

hexkey = 'fe553a0ad7707eb357abb2d0fe3b683d80dff50ded88b68aa5f2f4bf2edd66f1'

BLOCK_SIZE = 32
IV_BYTE_LENGTH = 16

PADDING = '{'
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

def AES_encrypt_account(bankaccount):
    key = binascii.unhexlify(hexkey)
    IV = Random.get_random_bytes(IV_BYTE_LENGTH)
    mode = AES.MODE_CBC
    encryptor = AES.new(key, mode, IV=IV)
    ciphertext = encryptor.encrypt(pad(bankaccount))
    return (ciphertext, IV)

def AES_decrypt_account(ciphertext, IV):
    key = binascii.unhexlify(hexkey)
    mode = AES.MODE_CBC
    encryptor = AES.new(key, mode, IV=IV)
    account = encryptor.decrypt(ciphertext).rstrip(PADDING)
    return account