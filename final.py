import numpy as np
import cv2
import string
import matplotlib.pyplot as plt
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import hashlib
import subprocess


def open(appname):
    cmd=f'''open "{appname}"'''
    subprocess.run(cmd, shell=True)



def derive_key(u_key):
    hash = hashlib.sha256(u_key.encode()).digest()[:16]
    # print("log successful")
    return hash

def e_key(msg,u_key):
    key=derive_key(u_key)
    Cipher = AES.new(key, AES.MODE_CBC)
    ct=Cipher.encrypt(pad(msg.encode(),AES.block_size))
    # print("log successful")
    return Cipher.iv+ct

def decrypt_message(cipher_bytes,u_key):
    key=derive_key(u_key) #key is 16 bytes
    iv=cipher_bytes[:16]
    ct=cipher_bytes[16:]
    Cipher = AES.new(key, AES.MODE_CBC, iv)
    # print("log successful")

    return unpad(Cipher.decrypt(ct),AES.block_size).decode()

   
d={chr(i):i for i in range(256)}
c={i:chr(i) for i in range(256)} 

img = cv2.imread('image.jpg')

key=str(input("enter the key: "))
msg=str(input("enter the message: "))

e_bytes=e_key(msg,key)

l=len(e_bytes)

print("length of encrypted text: ",l)

n=0
m=0
z=0
kl=0

for i in range(l):
    img[n,m,z]=e_bytes[i]^d[key[kl]]
    n=n+1  
    m=m+1
    m=(m+1)%3
    z=(z+1)%3
    kl=(kl+1)%len(key)

cv2.imwrite("encrypted_image.jpg",img) 
open("encrypted_image.jpg")
# print("log successful")

n,m,z=0,0,0
kl=0
again=str(input("enter the key: "))
if again==key:
    e_bytes=bytearray()
    for i in range(l):
        e_bytes.append(img[n,m,z]^d[key[kl]])
        n=n+1  
        m=m+1
        m=(m+1)%3
        z=(z+1)%3
        kl=(kl+1)%len(key)
    decrpyted_text=decrypt_message(e_bytes,again)
    print(decrpyted_text)

else:
    print("log failed")

cv2.imwrite("decrypted_image.jpg",img) 
open("decrypted_image.jpg")
print("log successful")
