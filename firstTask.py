import pytesseract
from JSON_Helper import Output, Source


def first_task(img):
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\Student\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'
    text = pytesseract.image_to_string(img, lang='eng+rus')[:-1]
    height, width = img.shape[:2]

    eng_alphabet = 'abcdefghijklmnopqrstuvwxyz'
    eng_alphabet = eng_alphabet + eng_alphabet.upper()
    eng_count = 0
    rus_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    rus_alphabet = rus_alphabet + rus_alphabet.upper()
    rus_count = 0
    for c in text:
        if c in eng_alphabet:
            eng_count += 1
        if c in rus_alphabet:
            rus_count += 1
    if eng_count > rus_count:
        text = pytesseract.image_to_string(img, lang='eng')[:-1]
    else:
        text = pytesseract.image_to_string(img, lang='rus')[:-1]

    for i in range(len(text)):
        if text[i] != ' ' and text[i] != '\n':
            text = text[i:]
            break
    for i in range(len(text) - 1, -1, -1):
        if text[i] != ' ' and text[i] != '\n':
            text = text[:i + 1]
            break
    text = text.replace('\n', ' ')
    while text.count('  ') > 0:
        text = text.replace('  ', ' ')

    return Output(text=text, source=Source(width=width, height=height))
