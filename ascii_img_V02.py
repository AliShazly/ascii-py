import time
import argparse
import sys
from PIL import Image
from termcolor import *
import colorama
colorama.init()

chars_html = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']
chars = chars_html[::-1]
palette = (
    12, 12, 12,  # Gray
    197, 15, 31,  # Red
    19, 161, 14,  # Green
    193, 156, 0,  # Yellow
    0, 55, 218,  # Blue
    136, 23, 152,  # Magenta
    58, 150, 221,  # Cyan
    204, 204, 204  # White
) + (0, 0, 0) * 248
palette_colors = ['grey', 'red', 'green', 'yellow',
                  'blue', 'magenta', 'cyan', 'white', 'grey']
palette_image = Image.new("P", (1, 1), 0)
palette_image.putpalette(palette)


def main():
    parser = argparse.ArgumentParser()
    mods = parser.add_mutually_exclusive_group()
    parser.add_argument('-r', '--resolution', type=int, default=100,
                        help='Width to resize the image to, in pixels. Higher value means more detail. Default=100')
    mods.add_argument('--html', action='store_true',
                      help='Output an HTML file containing the result to the current directory.')
    mods.add_argument('-c', '--color', action='store_true',
                      help='Print the output to the console in color (limited palette).')
    args = parser.parse_args(sys.argv[2:])
    try:
        im = Image.open(sys.argv[1])
    except FileNotFoundError as e:
        sys.stderr.write(f'{e}: Did you forget the file extension?')
        quit()

    resized = image_resize(im, args)
    ascii_pixels = '\n'.join(image_to_ascii_grayscale(resized, args))
    if args.color:
        color_values = image_to_ascii_color(resized)
        x = 0
        for i in ascii_pixels:
            if i != '\n':
                cprint(i, color=color_values[x], on_color='on_grey', end='')
                x += 1
            else:
                print(i, end='')
    else:
        if not args.html:
            print(ascii_pixels, end = '')
        else:
            with open('ascii.htm', 'w') as f:
                f.write(f'<pre style="font: 10px/5px monospace;">\n{ascii_pixels}</pre>')
            print('HTML Exported')


def image_resize(image, args):
    new_width = args.resolution
    (old_width, old_height) = image.size
    aspect_ratio = old_height/old_width
    new_height = int(aspect_ratio * new_width)
    new_dim = (new_width, new_height)
    new_image = image.resize(new_dim)
    return new_image


def image_to_ascii_grayscale(image, args):
    resolution = args.resolution
    image = image.convert('L')
    grayscale_values = list(image.getdata())
    if not args.html:
        ascii_pixels = ''.join(chars[i//25] for i in grayscale_values)
    else:
        ascii_pixels = ''.join(chars_html[i//25] for i in grayscale_values)
    ascii_image = [ascii_pixels[i:i+resolution]for i in range(0, len(ascii_pixels), resolution)]
    return ascii_image


def image_to_ascii_color(image):
    image_dithered = image.convert('RGB').quantize(palette=palette_image)
    image_values = list(image_dithered.getdata())
    color_values = [palette_colors[i] if i !='\n' else 'grey' for i in image_values] # Draws \n in grey
    return color_values


if __name__ == '__main__':
    main()
