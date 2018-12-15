import numpy as np
import cv2
from requests import get
from requests.auth import HTTPBasicAuth
import sys
from asciimatics.screen import Screen
import time
from PIL import Image

chars = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']
chars = chars[::-1]
resolution = 150
palette = (
    12,12,12, # Gray 
    197, 15, 31, # Red
    19, 161, 14, # Green
    193, 156, 0, # Yellow
    0, 55, 218, # Blue
    136, 23, 152, # Magenta
    58, 150, 221, # Cyan
    204, 204, 204 # White
) + (0,0,0) * 248
palette_image = Image.new("P", (1, 1), 0)
palette_image.putpalette(palette)


url = 'http://10.1.27.202:8081/shot.jpg'
cap = cv2.VideoCapture(0)

def image_resize(image, width=None, height=None):
    dim = None
    (old_height, old_width) = image.shape[:2]

    if width is None and height is None:
        return image

    if width is None:
        ratio = height / float(old_height)
        dim = (int(width * ratio), old_height)

    else:
        ratio = width / float(old_width)
        dim = (width, int(old_height * ratio))

    resized = cv2.resize(image, dim)
    return resized

def image_to_ascii_grayscale(image):
    grayscale_values = []
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            grayscale_values.append(image[i][j])
    ascii_pixels = ''.join(chars[i//25] for i in grayscale_values)
    ascii_image = [ascii_pixels[i:i+resolution] for i in range(0, len(ascii_pixels), resolution)]
    return ascii_image

def image_to_ascii_color(image):
    ascii_image = image_to_ascii_grayscale(image)
    
    

def get_video_stream(url):
    img_resp = get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    img_greyscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img_greyscale

def display_screen(screen):
    while True:
        start = time.time()
        frame = get_video_stream(url)
        resized = image_resize(frame, width=resolution)
        ascii_img = image_to_ascii_grayscale(resized)
        y = 0
        for i in ascii_img:
            screen.print_at(i, 0, y)
            y += 1
        screen.refresh()
        key = screen.get_key()
        if key in (ord('Q'), ord('q')):
            quit()
        if screen.has_resized():
            Screen.wrapper(display_screen)
        end = time.time()
        print(f'Loop completed in {round(end-start, 2)} seconds')

def display_terminal():  # Janky af but fast
    while True:
        start = time.time()
        frame = get_video_stream(url)
        resized = image_resize(frame, resolution)
        print('\n'.join(image_to_ascii_grayscale(resized)))
        end = time.time()
        print(f'Loop completed in {round(end-start, 2)} seconds')

def write_html():
    while True:
        frame = get_video_stream(url)
        resized = image_resize(frame, resolution)
        ascii_printable = '\n'.join(image_to_ascii_grayscale(resized))
        with open('ascii.htm', 'w') as f:
            f.write(f'<pre style="font: 10px/5px monospace;">{ascii_printable}</pre>')


# write_html()
# display_terminal()
Screen.wrapper(display_screen)
