from PIL import Image
import numpy as np
import cv2
import requests
import sys
from asciimatics.screen import Screen
import time

image = Image.open('img.png').convert('L')
chars = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']
chars = chars[::-1]
resolution = 100

url = 'http://192.168.0.221:8081/shot.jpg'
cap = cv2.VideoCapture(1)


def resize(image, new_width):
	(old_width, old_height) = image.size
	aspect_ratio = old_height/old_width
	new_height = int(aspect_ratio * new_width)
	new_dim = (new_width, new_height)
	new_image = image.resize(new_dim)
	return new_image

def image_to_ascii_grayscale(image):
	grayscale_values = list(image.getdata())
	ascii_pixels = ''.join((chars[i//25] for i in grayscale_values))
	ascii_image = [ascii_pixels[i:i+resolution] for i in range(0, len(ascii_pixels), resolution)]
	return ascii_image

def get_video_stream(url):
	img_resp = requests.get(url)
	img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
	img = cv2.imdecode(img_arr, -1)
	img_greyscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	pil_img = Image.fromarray(img_greyscale)
	return pil_img

def display_screen(screen):
    while True:
        start = time.time()
        frame = get_video_stream(url)
        resized = resize(frame, resolution)
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
        resized = resize(frame, resolution)
        print('\n'.join(image_to_ascii_grayscale(resized)))
        end = time.time()
        print(f'Loop completed in {round(end-start, 2)} seconds')

# display_terminal()
Screen.wrapper(display_screen)

# image input
# video input
# webcam input
