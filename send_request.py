import requests
import os 
# Define the URL of the Flask server
url = 'http://localhost:5000/ocr'  # Adjust the URL if your server is running on a different host or port

# Specify the image file path
path = os.getcwd()
folder_name = "test_image"
image_name = "2.png"
image_path = os.path.join(path, folder_name, image_name)

# Specify the list of languages
languages = ['English', 'French']  # Adjust the languages as needed

# Open the image file
with open(image_path, 'rb') as file:
    # Prepare the payload for the POST request
    payload = {'languages': languages}
    files = {'image': file}
    
    # Send the POST request
    response = requests.post(url, files=files, data=payload)
    
    # Check the response
    if response.status_code == 200:
        result = response.json()
        print(result)
    else:
        print(f'Error: {response.status_code}')
