from flask import Flask, request, jsonify
import easyocr
import os

app = Flask(__name__)

# Dictionary mapping language names to their codes
language_codes = {
    'Abaza': 'abq',
    'Adyghe': 'ady',
    'Afrikaans': 'af',
    'Angika': 'ang',
    'Arabic': 'ar',
    'Assamese': 'as',
    'Avar': 'ava',
    'Azerbaijani': 'az',
    'Belarusian': 'be',
    'Bulgarian': 'bg',
    'Bihari': 'bh',
    'Bhojpuri': 'bho',
    'Bengali': 'bn',
    'Bosnian': 'bs',
    'Simplified Chinese': 'ch_sim',
    'Traditional Chinese': 'ch_tra',
    'Chechen': 'che',
    'Czech': 'cs',
    'Welsh': 'cy',
    'Danish': 'da',
    'Dargwa': 'dar',
    'German': 'de',
    'English': 'en',
    'Spanish': 'es',
    'Estonian': 'et',
    'Persian (Farsi)': 'fa',
    'French': 'fr',
    'Irish': 'ga',
    'Goan Konkani': 'gom',
    'Hindi': 'hi',
    'Croatian': 'hr',
    'Hungarian': 'hu',
    'Indonesian': 'id',
    'Ingush': 'inh',
    'Icelandic': 'is',
    'Italian': 'it',
    'Japanese': 'ja',
    'Kabardian': 'kbd',
    'Kannada': 'kn',
    'Korean': 'ko',
    'Kurdish': 'ku',
    'Latin': 'la',
    'Lak': 'lbe',
    'Lezghian': 'lez',
    'Lithuanian': 'lt',
    'Latvian': 'lv',
    'Magahi': 'mah',
    'Maithili': 'mai',
    'Maori': 'mi',
    'Mongolian': 'mn',
    'Marathi': 'mr',
    'Malay': 'ms',
    'Maltese': 'mt',
    'Nepali': 'ne',
    'Newari': 'new',
    'Dutch': 'nl',
    'Norwegian': 'no',
    'Occitan': 'oc',
    'Pali': 'pi',
    'Polish': 'pl',
    'Portuguese': 'pt',
    'Romanian': 'ro',
    'Russian': 'ru',
    'Serbian (cyrillic)': 'rs_cyrillic',
    'Serbian (latin)': 'rs_latin',
    'Nagpuri': 'sck',
    'Slovak': 'sk',
    'Slovenian': 'sl',
    'Albanian': 'sq',
    'Swedish': 'sv',
    'Swahili': 'sw',
    'Tamil': 'ta',
    'Tabassaran': 'tab',
    'Telugu': 'te',
    'Thai': 'th',
    'Tajik': 'tjk',
    'Tagalog': 'tl',
    'Turkish': 'tr',
    'Uyghur': 'ug',
    'Ukranian': 'uk',
    'Urdu': 'ur',
    'Uzbek': 'uz',
    'Vietnamese': 'vi'
}

@app.route('/ocr', methods=['POST'])
def perform_ocr():
    # Check if image and languages are provided in the request
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    if 'languages' not in request.form:
        return jsonify({'error': 'No languages provided'}), 400
    
    image_file = request.files['image']
    language_names = request.form.getlist('languages')
    
    # Check if the request specifies all languages
    if 'all' in language_names:
        # Use all available languages
        languages = list(language_codes.values())
    else:
        # Map the language names to their corresponding language codes
        languages = [language_codes.get(lang) for lang in language_names]
        
        # Check if any language name is invalid
        if None in languages:
            return jsonify({'error': 'Invalid language'}), 400
    
    temp_image_path = "temp_image.png"
    image_file.save(temp_image_path)
    
    reader = easyocr.Reader(languages, gpu=False)  # Set the specified languages
    result = reader.readtext(temp_image_path)
    
    os.remove(temp_image_path)
    
    ocr_results = [word[1] for word in result]  # Extract text from result
    
    return jsonify({'results': ocr_results}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
