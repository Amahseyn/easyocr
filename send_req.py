import requests

# Endpoint URL
url = 'http://localhost:5000/ocr-translate'  # Replace with your actual server address

# Image file path
image_path = 'test_image/1.jpg'

languages = ['fr', 'de', 'es']  # French, German, Spanish

# Prepare the data
files = {'image': open(image_path, 'rb')}
data = {'languages': languages}

# Send POST request
response = requests.post(url, files=files, data=data)

# Check if the request was successful
if response.ok:
    # Check the content type of the response
    content_type = response.headers.get('content-type')
    if 'application/json' in content_type:
        # Print the translated results
        translated_results = response.json()['results']
        for lang, texts in translated_results.items():
            print(f"Translated texts in {lang}:")
            for text in texts:
                print(text)
            print()
    else:
        print("Unexpected content type:", content_type)
else:
    print("Error:", response.text)