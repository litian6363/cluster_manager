#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AES加密解密

需要使用pyCryptodome模块进行AES加密，安装：
pip install pycryptodome

pyCryptodome支持 python2.4 之后的版本和所有 python3 的版本
"""

from Crypto.Cipher import AES
import base64


class MyAES:
    def __init__(self, key, iv):
        self.key = bytes(key, encoding='utf8')
        self.iv = bytes(iv, encoding='utf8')
        self.mode = AES.MODE_CBC

    def my_encrypt(self, text):
        """加密函数"""
        text = bytes(text, encoding='utf8')  # 加密的文本必须是bytes
        # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）
        my_aes = AES.new(self.key, self.mode, self.iv)
        # 如果text不是16的倍数，那就补足为16的倍数
        length = 16
        count = len(text)
        add = length - (count % length)
        text = text + (b' ' * add)
        cipher_text = my_aes.encrypt(text)
        # 统一把加密后的text转化为base64
        return base64.b64encode(cipher_text)

    def my_decrypt(self, text):
        """把base64解密后，用rstrip()去掉补足的字符"""
        my_aes = AES.new(self.key, self.mode, self.iv)
        plain_text = my_aes.decrypt(base64.b64decode(text))
        return plain_text.rstrip()
