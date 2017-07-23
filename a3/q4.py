import requests
import json
import base64
import nacl.encoding
import nacl.signing
import pickle
from binascii import unhexlify

signing_key = nacl.signing.SigningKey.generate()
verify_key = signing_key.verify_key

verify_key_encoded = verify_key.encode(encoder=nacl.encoding.Base64Encoder)

url="https://whoomp.cs.uwaterloo.ca/458a3/api/signed/set-key"
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

message = "I love CS458"
signed = signing_key.sign(message)

url="https://whoomp.cs.uwaterloo.ca/458a3/api/signed/send"
payload = {
  "api_token": "4a177312a3a5022bfccf8d11b2cd92cc55cc3e14033c5cd3555ffa76582aa8d3",
  "to": "jessie",
  "message": base64.b64encode(signed)
}
response = requests.post(url, data=json.dumps(payload), headers=headers)

print(response.text)
print(response.status_code, response.reason)
