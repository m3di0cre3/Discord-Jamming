import requests
import json
import random

url = 'http://127.0.0.1:5000/receive_progress'
data = 'GRAHH'

while 1:
    cmd = input()
    if cmd == '0':
        data = random.randint(1, 100)
        url = 'http://127.0.0.1:5000/receive_progress'
        response = requests.post(url, json=data)
    elif cmd == '1':
        data = 'Current song : snow bunny heaven'
        url = 'http://127.0.0.1:5000/receive_song'
        response = requests.post(url, json=data)
    else:
        print("QUIT GG")
        break
