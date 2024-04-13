from flask import Flask, jsonify, request
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()
    text_to_translate = data.get('text', '')
    result = translator.translate(text_to_translate)
    return jsonify({
        'src': result.src,
        'dest': result.dest,
        'origin': result.origin,
        'text': result.text,
        'pronunciation': result.pronunciation
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
