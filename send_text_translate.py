import requests

# Define the URL of the translation endpoint
url = "http://127.0.0.1:5000/translate"

# Define the request payload with text to translate and destination language
payload = {
    "text": "Hello, how are you?",
    "dest": "spanish"
}

# Make the POST request
response = requests.post(url, json=payload)

# Print the response
print(response.json())
