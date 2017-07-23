import requests
import json
import base64
import nacl.encoding
import nacl.signing
import nacl.utils
import nacl.secret
from nacl.hash import blake2b
from nacl.public import PrivateKey, Box
from binascii import unhexlify

url="https://whoomp.cs.uwaterloo.ca/458a3/api/surveil/get-key"
payload = {
  "api_token": "4a177312a3a5022bfccf8d11b2cd92cc55cc3e14033c5cd3555ffa76582aa8d3",
  "user": "jessie"
}
headers = {
  "content-type": "application/json",
  "accept": "application/json"
}
response = requests.post(url, data=json.dumps(payload), headers=headers)

hex_key = json.loads(response.text)['public_key']
key = base64.b64decode(hex_key)
print(blake2b(key))
print(response.status_code, response.reason)

skme = PrivateKey.generate()
pkme = skme.public_key

pkme_encoded = pkme.encode(encoder=nacl.encoding.Base64Encoder)

url="https://whoomp.cs.uwaterloo.ca/458a3/api/surveil/set-key"
payload = {
  "api_token": "4a177312a3a5022bfccf8d11b2cd92cc55cc3e14033c5cd3555ffa76582aa8d3",
  "public_key": pkme_encoded
}
response = requests.post(url, data=json.dumps(payload), headers=headers)

print(response.text)
print(response.status_code, response.reason)

govkey = "lQBIde0SY48XNHaLbLDMv7CcTm/ri5jFHc2L+eFVKio="
pkgov = nacl.public.PublicKey(govkey, encoder=nacl.encoding.Base64Encoder)
pkjessie = nacl.public.PublicKey(hex_key, encoder=nacl.encoding.Base64Encoder)

message = "I love CS458"
messagekey = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
mbox = nacl.secret.SecretBox(messagekey)
mencrypted = mbox.encrypt(message)

jbox = Box(skme, pkjessie)
jencrypted = jbox.encrypt(messagekey)

gbox = Box(skme, pkgov)
gencrypted = gbox.encrypt(messagekey)

finalmessage = jencrypted + gencrypted + mencrypted

url="https://whoomp.cs.uwaterloo.ca/458a3/api/surveil/send"
payload = {
  "api_token": "4a177312a3a5022bfccf8d11b2cd92cc55cc3e14033c5cd3555ffa76582aa8d3",
  "to": "jessie",
  "message": base64.b64encode(finalmessage)
}
response = requests.post(url, data=json.dumps(payload), headers=headers)

print(response.text)
print(response.status_code, response.reason)

url="https://whoomp.cs.uwaterloo.ca/458a3/api/surveil/inbox"
payload = {
  "api_token": "4a177312a3a5022bfccf8d11b2cd92cc55cc3e14033c5cd3555ffa76582aa8d3",
}
response = requests.post(url, data=json.dumps(payload), headers=headers)

print(json.loads(response.text)[0]['message'])
print(response.status_code, response.reason)

received = base64.b64decode(json.loads(response.text)[0]['message'])
print(received[:72])
print(received[72:144])
print(received[144:])
mkey = jbox.decrypt(received[:72])
mbox = nacl.secret.SecretBox(mkey)
mdecrypted = mbox.decrypt(received[144:])
print(jbox.decrypt(received[:72]))
print(mdecrypted)
