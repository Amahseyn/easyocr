import requests
import json

url = 'http://localhost:5000/translate'
data = {'text': 'Mikä on nimesi'}
headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(data), headers=headers)

print(response.status_code)
print(response.json())
