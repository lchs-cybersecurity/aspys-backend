from random import randint
from string import ascii_letters
from hashlib import sha256

charselect = ascii_letters+"0123456789"
keylen = randint(40,50)
key = ""

for i in range(keylen):
    key += charselect[randint(0,len(charselect)-1)]

with open('extension_key.txt', 'w+') as extkeyfile:
    # salt later, if necessary
    extkeyfile.write(sha256(key.encode()).hexdigest())

print("KEY: {}".format(key))

