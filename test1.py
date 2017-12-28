#!usr/bin/env python3
# -*- coding: utf-8 -*-

from web.tools.aes import MyAES

a = MyAES('IamnotaherobutIs', 'ervedwithheroes.')

text = a.my_encrypt('bibibibi')

print(a.my_decrypt(b'Oe796cr1sLfm07coeFaQ4FjxdG1Cl9d0Rsw34t4lceMElh/Dh5TlB4xrx9sMiEL5CH03+h0Iu8DKsEJRhInPAhvUDgBBD82YsjimuDUJ1MOerxQupBATudg6JYwj9b+tn9Mlf7o26ADU1tiLZW7N9a0DYxJpVc168VZGrhH0BQY='))
print(a.my_decrypt(text))
