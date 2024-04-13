from googletrans import Translator
translator = Translator()
result = translator.translate('Mikä on nimesi')
print(result.src)
print(result.dest)
print(result.origin)
print(result.text)
print(result.pronunciation)