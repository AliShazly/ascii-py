import numpy as np
import cv2
from PIL import Image
import time 
import sys
import os
from asciimatics.screen import Screen
from asciimatics.renderers import StaticRenderer
from asciimatics.effects import Print
from asciimatics.scene import Scene
import termcolor as tc
import colorama
colorama.init()

cap = cv2.VideoCapture('vid.mp4')
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
palette_colors = ['grey','red','green','yellow','blue','magenta','cyan','white','grey']
palette_image = Image.new("P", (1, 1), 0)
palette_image.putpalette(palette)

def cv_to_pillow(image):
    img_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_RGB)
    return pil_img

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

def get_frame_data():
    frame_list = []
    print('Converting video to ascii...')
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            pil_frame = cv_to_pillow(frame)
            resized = image_resize(pil_frame, resolution)
            frame_list.append(image_to_ascii_grayscale(resized))
            cv2.imshow('frame', gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return
        else:
            cap.release()
            cv2.destroyAllWindows()
            return frame_list

def display_screen(screen): # Check pacman sample and make a sprite object to animate
    frame_list = get_frame_data()
    for i in range(100):
        scenes = []
        effects = [Print(screen, StaticRenderer(str(i)),0,0)]
        scenes.append(Scene(effects))
    screen.play(scenes)

def display_terminal():  # Janky af but fast
    while True:
        frame_list = get_frame_data()
        os.system('cls' if os.name == 'nt' else 'clear')
        for i in frame_list:
            print('\n'.join(i))
            time.sleep(.033)


display_terminal()

# if __name__ == "__main__":
#     while True:
#         Screen.wrapper(display_screen)
#         sys.exit(0)