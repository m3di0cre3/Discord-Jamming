import requests
import json
import random

data = {
    'key1': str(random.randint(1, 100)),
    'key2': str(random.randint(1, 100))
}

url = 'http://127.0.0.1:5000/receive_data'
response = requests.post(url, json=data)

# print("Response status code:", response.status_code)
# print("Response content:", response.text)

# try:
#     response_json = response.json()
#     print(response_json)
# except requests.exceptions.JSONDecodeError as e:
#     print("Failed to parse response as JSON:", e)
