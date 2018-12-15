import numpy as np
import cv2
import time
import argparse
import sys

# TODO: learn to use sys.argv[1] 
# TODO: Impliment --color
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, default = None)
    parser.add_argument('--resolution', type=int, default=100)
    parser.add_argument('--html', type=bool, default=False)
    args = parser.parse_args()
    resized = image_resize(args)
    image_to_ascii_grayscale(resized, args)

chars_html = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']
chars = chars_html[::-1]

def image_resize(args):
    width = args.resolution
    image = cv2.imread(args.image, cv2.IMREAD_GRAYSCALE)
    dim = None
    (old_height, old_width) = image.shape[:2]
    ratio = width / float(old_width)
    dim = (width, int(old_height * ratio))

    resized = cv2.resize(image, dim)
    return resized

def image_to_ascii_grayscale(image, args):
    grayscale_values = []
    html = args.html
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            grayscale_values.append(image[i][j])
    ascii_pixels = ''.join((chars[i//25] if not html else chars_html[i//25] for i in grayscale_values))
    ascii_image = [ascii_pixels[i:i+args.resolution] for i in range(0, len(ascii_pixels), args.resolution)]
    ascii_printable = '\n'.join(ascii_image)
    if not html:
        sys.stdout.write(ascii_printable)
        return
    else:
        with open('ascii.htm', 'w') as f:
            f.write(f'<pre style="font: 10px/5px monospace;">{ascii_printable}</pre>')
        sys.stdout.write('HTML Exported')
        return

if __name__ == '__main__':
    main()
