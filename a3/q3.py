import requests
import json
import base64
from nacl import pwhash, secret, utils
from binascii import unhexlify

psp = 'social justice'
salt = unhexlify('0322e4bdb68decafabc0f5596fd1ea1ed1de97774dbc33ad9b84a27e87224264')
olimit = 524288
mlimit = 16777216
message = "I love CS458"
kdf = pwhash.kdf_scryptsalsa208sha256

kjessie = kdf(secret.SecretBox.KEY_SIZE, psp, salt, opslimit=olimit, memlimit = mlimit)
box = secret.SecretBox(kjessie)
nonce = utils.random(secret.SecretBox.NONCE_SIZE)

encrypted = base64.b64encode(box.encrypt(message, nonce))

url="https://whoomp.cs.uwaterloo.ca/458a3/api/psp/send"
payload = {
  "api_token": "4a177312a3a5022bfccf8d11b2cd92cc55cc3e14033c5cd3555ffa76582aa8d3",
  "to": "jessie",
  "message": encrypted
}
headers = {
  "content-type": "application/json",
  "accept": "application/json"
}
response = requests.post(url, data=json.dumps(payload), headers=headers)

print(response.text)
print(response.status_code, response.reason)

url="https://whoomp.cs.uwaterloo.ca/458a3/api/psp/inbox"
payload = {
  "api_token": "4a177312a3a5022bfccf8d11b2cd92cc55cc3e14033c5cd3555ffa76582aa8d3",
}
response = requests.post(url, data=json.dumps(payload), headers=headers)

print(box.decrypt(base64.b64decode(json.loads(response.text)[0]['message'])))
