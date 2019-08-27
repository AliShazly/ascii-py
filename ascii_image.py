#! /usr/bin/env python3

import argparse
from PIL import Image
from termcolor import *
import colorama
import requests
from io import BytesIO
import json
import random
import string
import platform

colorama.init()

CHARS = ['.', ',', ':', ';', '+', '*', '?', '%', 'S', '#', '@']
PALETTE = (
    12, 12, 12,  # Gray
    197, 15, 31,  # Red
    19, 161, 14,  # Green
    193, 156, 0,  # Yellow
    0, 55, 218,  # Blue
    136, 23, 152,  # Magenta
    58, 150, 221,  # Cyan
    204, 204, 204  # White
) + (0, 0, 0) * 248  # Filling the rest of the palette with black
PALETTE_COLORS = ['grey', 'red', 'green', 'yellow',
                  'blue', 'magenta', 'cyan', 'white', 'grey']
PALETTE_IMAGE = Image.new('P', (1, 1), 0)
PALETTE_IMAGE.putpalette(PALETTE)


def image_resize(image, width=None, height=None):
    (old_width, old_height) = image.size
    # Chars are drawn at a 2:1 height:width ratio in the terminal
    old_height = old_height // 2
    if width is None and height is None:
        return image
    if width is None:
        aspect_ratio = height / float(old_height)
        dim = (int(old_width * aspect_ratio), height)
    else:
        aspect_ratio = width / float(old_width)
        dim = (width, int(old_height * aspect_ratio))
    resized = image.resize(dim)
    return resized


def image_to_ascii_greyscale(image, resolution, char_list):
    image = image.convert('L')
    greyscale_values = list(image.getdata())
    ascii_pixels = ''.join(char_list[i // 25] for i in greyscale_values)
    ascii_image = [ascii_pixels[i:i + resolution]
                   for i in range(0, len(ascii_pixels), resolution)]
    return ascii_image


def image_to_ascii_color(image):
    image_dithered = image.convert('RGB').quantize(palette=PALETTE_IMAGE)
    image_values = list(image_dithered.getdata())
    color_values = [PALETTE_COLORS[i] for i in image_values]
    return color_values


# https://stackoverflow.com/a/26665998
def rgb_to_ansi_escape(r, g, b):
    if r == g and g == b:
        if r < 8:
            return 16
        if r > 248:
            return 231
        return round(((r - 8) / 247) * 24) + 232

    ansi = 16 + (36 * round(r / 255 * 5)) + \
        (6 * round(g / 255 * 5)) + round(b / 255 * 5)
    return ansi


def supports_256_color():
    if platform.system() in ("Linux", "Darwin"):
        import curses
        curses.setupterm()
        if curses.tigetnum("colors") >= 256:
            return True
    return False


def print_image(img, resolution, greyscale=False, bg_color=False, fg_color=True):
    if greyscale:
        bg_color = False
        fg_color = False

    original_aspect_ratio = img.size[0] / img.size[1]
    img = image_resize(img, width=resolution)
    ascii_list = image_to_ascii_greyscale(img, resolution, CHARS)
    ascii_pixels = '\n'.join(ascii_list)
    _256_color = supports_256_color()

    if _256_color:
        color_values = list(img.getdata())
    else:
        color_values = image_to_ascii_color(img)

    idx = 0  # Can't use enumerate because newline chars need to be ingnored
    for i in ascii_pixels:
        if i != '\n':
            if _256_color:
                color = rgb_to_ansi_escape(*color_values[idx])
                print(
                    f"\033[48;5;{color if bg_color else 0};38;5;{color if fg_color else 256}m{i}\033[0;00m", end='')
                idx += 1
            else:
                cprint(i, color=(color_values[idx] if fg_color else 'white'),
                       on_color=(
                           f'on_{color_values[idx]}' if bg_color else 'on_grey'),
                       end='')
                idx += 1
        else:
            print(i, end='')
    print('')


def get_image_from_url(url):
    r = requests.get(args.url)
    r.raise_for_status()
    img = Image.open(BytesIO(r.content)).convert('RGB')
    return img


def export_json(filepath, img, resolution):
    original_aspect_ratio = img.size[0] / img.size[1]
    resized = image_resize(img, width=resolution)
    width, height = resized.size
    ascii_list = image_to_ascii_greyscale(resized, resolution, CHARS)
    ascii_pixels = '\n'.join(ascii_list)

    values_dict = {
        'width': width,
        'height': height,
        'aspect': original_aspect_ratio,
        'image': ascii_pixels
    }
    rand_string = ''.join(random.choices(
        string.ascii_uppercase + string.ascii_lowercase + string.digits, k=8))
    with open(f'{filepath}/ascii_image_{rand_string}.json', 'w+') as outfile:
        json.dump(values_dict, outfile)
    print(f'{filepath}/ascii_image_{rand_string}.json exported.')


def main():
    parser = argparse.ArgumentParser()
    mods = parser.add_mutually_exclusive_group()
    inputs = parser.add_mutually_exclusive_group()
    parser.add_argument('-r', '--resolution', type=int, default=100,
                        help='Width to resize the image to, in pixels. Higher value means more detail. Default=100')
    parser.add_argument('-j', '--json', type=str,
                        help='Specify filepath for JSON output. To be used for embedding in webpages.')
    mods.add_argument('-c', '--color', action='store_true',
                      help='Print the ascii charecters to the console in color')
    parser.add_argument('-b', '--background', action='store_true',
                        help='Print the ascii charecters to the console with colored backgrounds')
    inputs.add_argument('-f', '--file', type=str,
                        help='Specify a file to turn into ASCII')
    inputs.add_argument('-u', '--url', type=str,
                        help='Specify an image URL to turn into ASCII')
    args = parser.parse_args()

    if args.url:
        img = get_image_from_url(args.url)
    elif args.file:
        img = Image.open(args.file)
    else:
        raise ValueError("Must provide image input")

    if args.json:
        export_json(args.json, img, args.resolution)
    else:
        foreground = True if args.color else False
        background = True if args.background else False
        greyscale = False if foreground or background else True
        print_image(img, args.resolution, greyscale, background, foreground)


if __name__ == '__main__':
    main()
