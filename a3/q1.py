import requests
import json

url="https://whoomp.cs.uwaterloo.ca/458a3/api/plain/send"
payload = {
  "api_token": "4a177312a3a5022bfccf8d11b2cd92cc55cc3e14033c5cd3555ffa76582aa8d3",
  "to": "jessie",
  "message": "SGVsbG8sIHdvcmxkIQ=="
}
headers = {
  "content-type": "application/json",
  "accept": "application/json"
}
response = requests.post(url, data=json.dumps(payload), headers=headers)

print(response.text)
print(response.status_code, response.reason)

url="https://whoomp.cs.uwaterloo.ca/458a3/api/plain/inbox"
payload = {
  "api_token": "4a177312a3a5022bfccf8d11b2cd92cc55cc3e14033c5cd3555ffa76582aa8d3",
}
response = requests.post(url, data=json.dumps(payload), headers=headers)

print(response.text)
print(response.status_code, response.reason)
