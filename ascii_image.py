import argparse
from PIL import Image
from termcolor import *
import colorama
import requests
from io import BytesIO
import json

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
    old_height = old_height // 2  # Chars are drawn at a 2:1 height:width ratio in the terminal
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


def image_to_ascii_grayscale(image, resolution, char_list):
    image = image.convert('L')
    grayscale_values = list(image.getdata())
    ascii_pixels = ''.join(char_list[i // 25] for i in grayscale_values)
    ascii_image = [ascii_pixels[i:i + resolution] for i in range(0, len(ascii_pixels), resolution)]
    return ascii_image


def image_to_ascii_color(image):
    image_dithered = image.convert('RGB').quantize(palette=palette_image)
    image_values = list(image_dithered.getdata())
    color_values = [palette_colors[i] for i in image_values]
    return color_values


def main():
    parser = argparse.ArgumentParser()
    mods = parser.add_mutually_exclusive_group()
    inputs = parser.add_mutually_exclusive_group()
    parser.add_argument('-r', '--resolution', type=int, default=100,
                        help='Width to resize the image to, in pixels. Higher value means more detail. Default=100')
    mods.add_argument('--html', action='store_true',
                      help='Output an HTML file containing the result to the current directory.')
    parser.add_argument('-j', '--json', action='store_true',
                        help='Output ASCII image and info to JSON. To be used for embedding in webpages.')
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
        r = requests.get(args.url)
        r.raise_for_status()
        img = Image.open(BytesIO(r.content)).convert('RGB')
    elif args.file:
        img = Image.open(args.file)

    resized = image_resize(img, width=args.resolution)
    width, height = resized.size
    char_list = chars_html if args.html else chars
    ascii_pixels = '\n'.join(image_to_ascii_grayscale(resized, args.resolution, char_list))

    if args.json and (args.color or args.background):
        pixel_color_values = list(resized.getdata())
        reshaped = []
        idx = 0
        for i in ascii_pixels:
            if i != '\n':
                reshaped.append(pixel_color_values[idx])
                idx += 1
            else:
                reshaped.append((0, 0, 0))
        values_dict = {
            'width': width,
            'height': height,
            'image': ascii_pixels,
            'pixel_values': reshaped
        }
        with open('ascii_image.json', 'w') as outfile:
            json.dump(values_dict, outfile)
        print('JSON Exported')
        return

    elif args.json:
        values_dict = {
            'width': width,
            'height': height,
            'image': ascii_pixels
        }
        with open('ascii_image.json', 'w') as outfile:
            json.dump(values_dict, outfile)
        print('JSON Exported')
        return

    if args.color or args.background:
        color_values = image_to_ascii_color(resized)
        idx = 0  # Can't use enumerate because newline chars need to be ingnored
        for i in ascii_pixels:
            if i != '\n':
                cprint(i, color=(color_values[idx] if args.color else 'white'),
                       on_color=(f'on_{color_values[idx]}' if args.background else 'on_grey'),
                       end='')
                idx += 1
            else:
                print(i, end='')
    else:
        if args.html:
            with open('ascii.htm', 'w') as outfile:
                outfile.write(f'<pre style="font: 10px/5px monospace;">\n{ascii_pixels}</pre>')
            print('HTML Exported')

        else:
            print(ascii_pixels, end='')


if __name__ == '__main__':
    main()
