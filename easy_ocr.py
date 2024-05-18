import easyocr
import os
print(os.getcwd())
path = os.getcwd()
folder_name = "test_image"
image_name = "2.png"
image_path = os.path.join(path, folder_name, image_name)
# image_path

reader = easyocr.Reader(['en'], gpu=False)  
result = reader.readtext(image_path, detect_languages=True)
    
for (bbox, text, prob) in result:
    print(f'Text: {text}, Probability: {prob}')