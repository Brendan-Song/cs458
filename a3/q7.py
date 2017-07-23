import requests
import json
import base64
import nacl.encoding
import nacl.signing
import nacl.utils
import pickle
from nacl.hash import blake2b
from nacl.public import PrivateKey, Box
from binascii import unhexlify

signing_key = nacl.signing.SigningKey.generate()
verify_key = signing_key.verify_key

verify_key_encoded = verify_key.encode(encoder=nacl.encoding.Base64Encoder)

url="https://whoomp.cs.uwaterloo.ca/458a3/api/prekey/set-identity-key"
payload = {
  "api_token": "4a177312a3a5022bfccf8d11b2cd92cc55cc3e14033c5cd3555ffa76582aa8d3",
  "public_key": verify_key_encoded
}
headers = {
  "content-type": "application/json",
  "accept": "application/json"
}
response = requests.post(url, data=json.dumps(payload), headers=headers)

print(response.text)
print(response.status_code, response.reason)

skme = PrivateKey.generate()
pkme = skme.public_key
pkme_encoded = pkme.encode(encoder=nacl.encoding.RawEncoder)

signed = signing_key.sign(pkme_encoded)

url="https://whoomp.cs.uwaterloo.ca/458a3/api/prekey/set-signed-prekey"
payload = {
  "api_token": "4a177312a3a5022bfccf8d11b2cd92cc55cc3e14033c5cd3555ffa76582aa8d3",
  "public_key": base64.b64encode(signed)
}
response = requests.post(url, data=json.dumps(payload), headers=headers)

print(response.text)
print(response.status_code, response.reason)

url="https://whoomp.cs.uwaterloo.ca/458a3/api/prekey/get-identity-key"
payload = {
  "api_token": "4a177312a3a5022bfccf8d11b2cd92cc55cc3e14033c5cd3555ffa76582aa8d3",
  "user": "jessie"
}
response = requests.post(url, data=json.dumps(payload), headers=headers)

encodedprekey = json.loads(response.text)['public_key']
print(response.status_code, response.reason)

print(encodedprekey)
verifykey = nacl.signing.VerifyKey(encodedprekey, encoder=nacl.encoding.Base64Encoder)
print(verifykey)

url="https://whoomp.cs.uwaterloo.ca/458a3/api/prekey/get-signed-prekey"
payload = {
  "api_token": "4a177312a3a5022bfccf8d11b2cd92cc55cc3e14033c5cd3555ffa76582aa8d3",
  "user": "jessie"
}
response = requests.post(url, data=json.dumps(payload), headers=headers)

jkey = verifykey.verify(base64.b64decode(json.loads(response.text)['public_key']))
pkjessie = nacl.public.PublicKey(jkey, encoder=nacl.encoding.RawEncoder)

message = "I love CS458"
box = Box(skme, pkjessie)

encrypted = box.encrypt(message)

url="https://whoomp.cs.uwaterloo.ca/458a3/api/prekey/send"
payload = {
  "api_token": "4a177312a3a5022bfccf8d11b2cd92cc55cc3e14033c5cd3555ffa76582aa8d3",
  "to": "jessie",
  "message": base64.b64encode(encrypted)
}
response = requests.post(url, data=json.dumps(payload), headers=headers)

print(response.text)
print(response.status_code, response.reason)

url="https://whoomp.cs.uwaterloo.ca/458a3/api/prekey/inbox"
payload = {
  "api_token": "4a177312a3a5022bfccf8d11b2cd92cc55cc3e14033c5cd3555ffa76582aa8d3",
}
response = requests.post(url, data=json.dumps(payload), headers=headers)

print(json.loads(response.text)[0]['message'])
print(response.status_code, response.reason)

received = base64.b64decode(json.loads(response.text)[0]['message'])
print(box.decrypt(received))
