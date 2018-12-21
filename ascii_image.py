import argparse
import sys
from PIL import Image
from termcolor import *
import colorama
import requests
from io import BytesIO
colorama.init()

chars_html = ['@', '#', 'S', '%', '?', '*', '+',
              ';', ':', ',', '.']  # TODO: Change char list
chars = chars_html[::-1]  # Reverse colors when being printed white-on-black
palette = (
    12, 12, 12,  # Gray
    197, 15, 31,  # Red
    19, 161, 14,  # Green
    193, 156, 0,  # Yellow
    0, 55, 218,  # Blue
    136, 23, 152,  # Magenta
    58, 150, 221,  # Cyan
    204, 204, 204  # White
) + (0, 0, 0) * 248  # Filling the rest of the palette with black
palette_colors = ['grey', 'red', 'green', 'yellow',
                  'blue', 'magenta', 'cyan', 'white', 'grey']
palette_image = Image.new('P', (1, 1), 0)
palette_image.putpalette(palette)

def image_resize(image, width=None, height=None):
    (old_width, old_height) = image.size
    old_height = old_height//2 # Chars are drawn at a 2:1 height:width ratio in the terminal
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

def image_to_ascii_grayscale(image, args):
    resolution = args.resolution
    image = image.convert('L')
    grayscale_values = list(image.getdata())
    if not args.html:
        ascii_pixels = ''.join(chars[i//25] for i in grayscale_values)
    else:
        ascii_pixels = ''.join(chars_html[i//25] for i in grayscale_values)
    ascii_image = [ascii_pixels[i:i+resolution]
                   for i in range(0, len(ascii_pixels), resolution)]
    return ascii_image

def image_to_ascii_color(image):
    image_dithered = image.convert('RGB').quantize(palette=palette_image)
    image_values = list(image_dithered.getdata())
    color_values = [palette_colors[i] if i !=
                    '\n' else 'grey' for i in image_values]  # Draws \n in grey
    return color_values

def main():
    parser = argparse.ArgumentParser()
    mods = parser.add_mutually_exclusive_group()
    parser.add_argument('-r', '--resolution', type=int, default=100,
                        help='Width to resize the image to, in pixels. Higher value means more detail. Default=100')
    mods.add_argument('--html', action='store_true',
                      help='Output an HTML file containing the result to the current directory.')
    mods.add_argument('-c', '--color', action='store_true',
                      help='Print the ascii charecters to the console in color')
    parser.add_argument('-b', '--background', action='store_true',
                        help='Print the ascii charecters to the console with colored backgrounds')
    args = parser.parse_args(sys.argv[2:])
    try:
        r = requests.get(sys.argv[1])
        r.raise_for_status()
        im = Image.open(BytesIO(r.content)).convert('RGBA')
    except requests.exceptions.MissingSchema:
        try:
            im = Image.open(sys.argv[1])
        except FileNotFoundError as e:
            print(f'{e}: Did you forget the file extension?')
            sys.exit()
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit()

    resized = image_resize(im, width=args.resolution)
    ascii_pixels = '\n'.join(image_to_ascii_grayscale(resized, args))
    # TODO: Don't print pixel by pixel
    if args.color or args.background:
        color_values = image_to_ascii_color(resized)
        x = 0
        for i in ascii_pixels:
            if i != '\n':
                cprint(i, color=(color_values[x] if args.color else 'white'), on_color=(
                    f'on_{color_values[x]}' if args.background else 'on_grey'), end='')
                x += 1
            else:
                print(i, end='')
    else:
        if not args.html:
            print(ascii_pixels, end='')
        else:
            with open('ascii.htm', 'w') as outfile:
                outfile.write(
                    f'<pre style="font: 10px/5px monospace;">\n{ascii_pixels}</pre>')
            print('HTML Exported')

if __name__ == '__main__':
    main()
