#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AES加密解密

需要使用pyCryptodome模块进行AES加密，安装：
pip install pycryptodome

pyCryptodome支持 python2.4 之后的版本和所有 python3 的版本
"""


__author__ = 'LiTian'


from Crypto.Cipher import AES
import base64


class MyAES:
    def __init__(self, key, iv):
        self.key = bytes(key, encoding='utf8')
        self.iv = bytes(iv, encoding='utf8')
        self.mode = AES.MODE_CBC

    def my_encrypt(self, text):
        """加密函数"""
        # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）
        my_aes = AES.new(self.key, self.mode, self.iv)
        # 如果AES加密的text不是16的倍数，那就使用PKCS5Padding来为text填充（例如缺6位，则补6个6），如果刚好是16的倍数，则补16个bytes的16
        length = 16
        count = len(text)
        self.padding = length - (count % length)
        text = text + (chr(self.padding) * self.padding)
        text = bytes(text, encoding='utf8')  # 加密的文本必须是bytes
        cipher_text = my_aes.encrypt(text)
        # 统一把加密后的bytes转化为base64
        return str(base64.b64encode(cipher_text), encoding='utf8')

    def my_decrypt(self, text):
        """用base64解密后，用rstrip()去掉补足的字符"""
        my_aes = AES.new(self.key, self.mode, self.iv)
        plain_text = my_aes.decrypt(base64.b64decode(bytes(text, encoding='utf8')))
        return str(plain_text, encoding='utf8').rstrip(chr(self.padding))
