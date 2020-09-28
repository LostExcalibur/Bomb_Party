import string

import pyperclip as pc
from PIL import ImageGrab, ImageOps
import pytesseract

try:
    from PIL import Image
except ImportError:
    import Image


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def assign_score(mot):
    score = 0
    for char in unused_letters:
        if char in mot:
            score += 1
    return score        


def find_word(letters):
    with open("frgut.txt", "r", encoding="utf-8") as handle:
        mots = handle.readlines()

    letters = letters.lower().strip()

    mots_corrects_lettres = [mot.strip() for mot in mots if letters in mot]
    mots_corrects = [mot for mot in mots_corrects_lettres if mot not in used_words]

    if len(mots_corrects) == 0:
        best_word = ''
    else:
        best_word = max(mots_corrects, key=assign_score)

    pc.copy(best_word)

    return best_word


def screenshot():
    image = ImageGrab.grab(bbox=(700, 575, 765, 610))
    image.save('sc.png')


def clarify_image():
    imagegray = Image.open('sc.png')
    imagegray = ImageOps.equalize(imagegray)
    imagegray = ImageOps.invert(imagegray)
    imagegray.save('sc.png')


def recognition():
    return "".join([char for char in pytesseract.image_to_string(Image.open('sc.png')) if char in string.ascii_letters])


def solve_using_ocr():
    screenshot()
    clarify_image()

    syllabe = recognition()
    mot = find_word(syllabe)
    print(syllabe, mot)
    return mot


def solve_using_clipboard():
    syllabe = pc.paste()
    mot = find_word(syllabe)
    print(syllabe, mot)
    return mot


first = pc.paste()
used_words = []
solve = ''
unused_letters = [x for x in string.ascii_lowercase]


while True:
    clip = pc.paste()
    if clip != first and solve != clip:
        solve = solve_using_clipboard()
        
        for letter in unused_letters:
            if letter in solve:
                unused_letters.remove(letter)
        
        used_words.append(solve)
        first = clip

    if len(unused_letters) == 0:
        unused_letters = string.ascii_lowercase

    clip = pc.paste()
