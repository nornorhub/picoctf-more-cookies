# Adapted from python2 solution by Martin Carlisle on youtube
# With help from github copilot <3

import requests
import base64

s=requests.Session()
s.get('http://mercury.picoctf.net:10868/')
cookie = s.cookies['auth_name']
unb64 = base64.b64decode(cookie)
unb64b = base64.b64decode(unb64)
# first 128-bit block is IV, flip IV bit to flip plaintext bit "admin=0" to "admin=1"
# looping through bytes (16 bytes because 128-bit block)
for i in range(0, 128):
    pos=i//8
    guessdec = unb64b[0:pos] + (unb64b[pos]^(1<<(i%8))).to_bytes(1, 'big') + unb64b[pos+1:]
    guess=base64.b64encode(base64.b64encode(guessdec))
    r=requests.get('http://mercury.picoctf.net:10868/', cookies={"auth_name": guess.decode()})
    if "pico" in r.text:
        print("Flag: " + r.text.split("<code>")[1].split("</code>")[0])
        break
