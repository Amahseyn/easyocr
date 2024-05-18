from flask import Flask, request, jsonify
import easyocr
import os
from googletrans import Translator

app = Flask(__name__)
translator = Translator()
langs = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'he': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'or': 'odia',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'ug': 'uyghur',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu'
}


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

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()
    text_to_translate = data.get('text', '')
    dest_language = data.get('dest', 'en')  # Default destination language is English if not provided
    result = translator.translate(text_to_translate, dest=dest_language)
    return jsonify({
        'src': result.src,
        'dest': result.dest,
        'origin': result.origin,
        'text': result.text,
        'pronunciation': result.pronunciation
    })

@app.route('/ocr-translate', methods=['POST'])
def perform_ocr_and_translate():
    # Check if image and languages are provided in the request
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    if 'languages' not in request.form:
        return jsonify({'error': 'No languages provided'}), 400
    
    image_file = request.files['image']
    language_codes = request.form.getlist('languages')
    
    # Check if the request specifies all languages
    if 'all' in language_codes:
        # Use all available languages
        languages = list(langs.keys())
    else:
        languages = language_codes
    
    temp_image_path = "temp_image.png"
    image_file.save(temp_image_path)
    
    reader = easyocr.Reader(languages, gpu=False)  # Set the specified languages
    result = reader.readtext(temp_image_path)
    
    os.remove(temp_image_path)
    
    ocr_results = [word[1] for word in result]  # Extract text from result
    
    # Translate the extracted text into the specified languages
    translated_results = {}
    for lang_code in language_codes:
        lang_name = langs.get(lang_code)
        translated_texts = []
        for text in ocr_results:
            translation = translator.translate(text, dest=lang_code)
            translated_texts.append(translation.text)
        translated_results[lang_name] = translated_texts
    
    return jsonify({'results': translated_results}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
