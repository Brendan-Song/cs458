import requests
import json
import base64
import nacl.encoding
import nacl.signing
import nacl.utils
from nacl.hash import blake2b
from nacl.public import PrivateKey, Box
from binascii import unhexlify

url="https://whoomp.cs.uwaterloo.ca/458a3/api/pke/get-key"
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

url="https://whoomp.cs.uwaterloo.ca/458a3/api/pke/set-key"
payload = {
  "api_token": "4a177312a3a5022bfccf8d11b2cd92cc55cc3e14033c5cd3555ffa76582aa8d3",
  "public_key": pkme_encoded
}
response = requests.post(url, data=json.dumps(payload), headers=headers)

print(response.text)
print(response.status_code, response.reason)

pkjessie = nacl.public.PublicKey(hex_key, encoder=nacl.encoding.Base64Encoder)
box = Box(skme, pkjessie)
message = "I love CS458"

encrypted = box.encrypt(message)

url="https://whoomp.cs.uwaterloo.ca/458a3/api/pke/send"
payload = {
  "api_token": "4a177312a3a5022bfccf8d11b2cd92cc55cc3e14033c5cd3555ffa76582aa8d3",
  "to": "jessie",
  "message": base64.b64encode(encrypted)
}
response = requests.post(url, data=json.dumps(payload), headers=headers)

print(response.text)
print(response.status_code, response.reason)

url="https://whoomp.cs.uwaterloo.ca/458a3/api/pke/inbox"
payload = {
  "api_token": "4a177312a3a5022bfccf8d11b2cd92cc55cc3e14033c5cd3555ffa76582aa8d3",
}
response = requests.post(url, data=json.dumps(payload), headers=headers)

print(json.loads(response.text)[0]['message'])
print(response.status_code, response.reason)

received = base64.b64decode(json.loads(response.text)[0]['message'])
print(box.decrypt(received))
