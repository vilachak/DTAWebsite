# Copyright 2022-2023, IT Cell, Directorate of Treasuries & Accounts, Nagaland. All rights reserved.
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import algorithms
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


class AesCrypto(object):
    def __init__(self, key, iv):
        self.key = key.encode('utf-8')[:32]
        self.iv = iv.encode('utf-8')[:16]
        self.mode = AES.MODE_CBC
        self.block_size = 16

    @staticmethod
    def pkcs7_padding(data):
        if not isinstance(data, bytes):
            data = data.encode()
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        return padded_data

    def encrypt(self, plaintext):
        cryptor = AES.new(self.key, self.mode, self.iv)
        plaintext = plaintext
        plaintext = self.pkcs7_padding(plaintext)
        ciphertext = cryptor.encrypt(plaintext)
        return b2a_hex(ciphertext).decode('utf-8')

    def decrypt(self, ciphertext):
        cryptor = AES.new(self.key, self.mode, self.iv)
        plaintext_decrypted = cryptor.decrypt(a2b_hex(ciphertext))
        plaintext_decrypted = bytes.decode(plaintext_decrypted)
        return plaintext_decrypted
