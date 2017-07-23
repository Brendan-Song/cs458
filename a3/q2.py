import requests
import json
import nacl.secret
import nacl.utils
import base64
from binascii import unhexlify

kjessie = unhexlify("ecd6ecd5128917210387e7597023e556ae35ff267f0e287352df7df3205f6b0c")
box = nacl.secret.SecretBox(kjessie)
message = "I love CS458"

encrypted = base64.b64encode(box.encrypt(message))

url="https://whoomp.cs.uwaterloo.ca/458a3/api/psk/send"
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

url="https://whoomp.cs.uwaterloo.ca/458a3/api/psk/inbox"
payload = {
  "api_token": "4a177312a3a5022bfccf8d11b2cd92cc55cc3e14033c5cd3555ffa76582aa8d3",
}
response = requests.post(url, data=json.dumps(payload), headers=headers)

print(box.decrypt(base64.b64decode(json.loads(response.text)[0]['message'])))
