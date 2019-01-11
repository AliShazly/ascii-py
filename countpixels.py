from PIL import Image, ImageDraw, ImageFont, ImageOps
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

chars = ['€', '‚', 'ƒ', '„', '…', '†', '‡', 'ˆ', '‰', 'Š', '‹', 'Œ', 'Ž', '‘', '’', '“', '”', '•', '–', '—', '˜', '™', 'š', '›', 'œ', 'ž', 'Ÿ', '¡', '¢', '£', '¤', '¥', '¦', '§', '¨', '©', 'ª', '«', '¬', '®', '¯', '°', '±', '²', '³', '´', 'µ', '¶', '·', '¸', '¹', 'º', '»', '¼', '½', '¾', '¿', 'À', 'Á', 'Â',
         'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï', 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', '×', 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'ß', 'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î', 'ï', 'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', '÷', 'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'þ', 'ÿ']

def count_pixels(chars):
    scores = []
    for i in chars:
        txt = Image.new('L', (100, 100), (255))
        fnt = ImageFont.truetype('consolas.ttf', 60)
        d = ImageDraw.Draw(txt)
        d.text((0, 0), i, font=fnt, fill=(0))
        txt = ImageOps.invert(txt)
        scores.append((i, sum(txt.getdata())/25500))
    scores.sort(key=lambda x: x[1])

    names = [i[0] for i in scores]
    values = [i[1] for i in scores]

    x_pos = [i for i, _ in enumerate(names)]

    plt.bar(x_pos, values, color='green')
    plt.xlabel('Char')
    plt.ylabel('Score')

    plt.xticks(x_pos, names)

    plt.show()

    return names

def test():
    white = Image.new('L', (100, 100), (255))
    black = Image.new('L', (100, 100), (0))
    max_score = sum(white.getdata())
    min_score = sum(black.getdata())
    print(f'max: {max_score} min: {min_score}')


chars_sorted = count_pixels(chars)
print(chars_sorted)
# test()