import numpy as np
import cv2
from requests import get
from requests.auth import HTTPBasicAuth
import sys
from asciimatics.screen import Screen
import time
from PIL import Image
from termcolor import *
import colorama
colorama.init()

chars = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']
chars = chars[::-1]
resolution = 50
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
palette_colors = ['grey','red','green','yellow','blue','magenta','cyan','white','grey']
palette_image = Image.new("P", (1, 1), 0)
palette_image.putpalette(palette)

url = 'http://192.168.0.221:8081/shot.jpg'

def image_resize(image, new_width):
	(old_width, old_height) = image.size
	aspect_ratio = old_height/old_width
	new_height = int(aspect_ratio * new_width)
	new_dim = (new_width, new_height)
	new_image = image.resize(new_dim)
	return new_image

def image_to_ascii_grayscale(image):
    image = image.convert('L')
    grayscale_values = list(image.getdata())
    ascii_pixels = ''.join(chars[i//25] for i in grayscale_values)
    ascii_image = [ascii_pixels[i:i+resolution] for i in range(0, len(ascii_pixels), resolution)]
    return ascii_image

def image_to_ascii_color(image):
    image_dithered = image.convert('RGB').quantize(palette = palette_image)
    image_values = list(image_dithered.getdata())
    pixel_values = [palette_colors[i] if i != '\n' else 'red' for i in image_values]
    return pixel_values

def get_video_stream(url):
    img_resp = get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_RGB)
    return pil_img

def display_screen(screen):
    while True:
        start = time.time()
        frame = get_video_stream(url)
        resized = image_resize(frame, resolution)
        ascii_img = image_to_ascii_grayscale(resized)
        # TODO: Make this better
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

# def display_terminal():  # Janky af but fast
#     while True:
#         start = time.time()
#         frame = get_video_stream(url)
#         resized = image_resize(frame, resolution)
#         print('\n'.join(image_to_ascii_grayscale(resized)))
#         end = time.time()
#         print(f'Loop completed in {round(end-start, 2)} seconds')

def display_terminal():
    while True:
        frame = get_video_stream(url)
        resized = image_resize(frame, resolution)
        pixel_values = image_to_ascii_color(resized)
        ascii_pixels = '\n'.join(image_to_ascii_grayscale(resized))
        # TODO: Make this better
        x = 0
        for i in ascii_pixels:
            if i != '\n':
                cprint(i, color=pixel_values[x], end = '')
                x += 1
            else:
                print(i, end = '')

def write_html():
    while True:
        frame = get_video_stream(url)
        resized = image_resize(frame, resolution)
        ascii_printable = '\n'.join(image_to_ascii_grayscale(resized))
        with open('ascii.htm', 'w') as f:
            f.write(f'<pre style="font: 10px/5px monospace;">{ascii_printable}</pre>')


# write_html()
display_terminal()
# Screen.wrapper(display_screen)
