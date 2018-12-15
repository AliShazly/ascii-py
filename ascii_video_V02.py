import numpy as np
import cv2
from PIL import Image
import time 
import sys
import os
import pafy
import argparse

chars = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']
chars = chars[::-1]

def cv_to_pillow(image):
    img_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_RGB)
    return pil_img

def image_resize(image, width = None, height = None):
    dim = None
    (old_width, old_height) = image.size
    if width is None and height is None:
        return image
    if width is None:
        aspect_ratio = height / float(old_height)
        dim = (int(old_width * aspect_ratio), height)
    else:
        aspect_ratio = width / float(old_width)
        dim = (width, int(old_height * aspect_ratio))
    resized = image.resize(dim)
    return resized, dim

def image_to_ascii_grayscale(image):
    image = image.convert('L')
    grayscale_values = list(image.getdata())
    ascii_pixels = ''.join(chars[i//25] for i in grayscale_values)
    ascii_image = [ascii_pixels[i:i+resolution] for i in range(0, len(ascii_pixels), resolution)]
    return ascii_image

def get_frame_data(): # TODO add a progress bar
    frame_list = []
    print('Converting to ASCII, do not resize window.')
    while True:
        ret, frame = cap.read()
        if ret:
            pil_frame = cv_to_pillow(frame)
            resized, dim = image_resize(pil_frame, width = resolution)
            frame_list.append(('\n'.join(image_to_ascii_grayscale(resized))))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return
        else:
            os.system(f'mode con: cols={dim[0]} lines={dim[1]}')
            cap.release()
            cv2.destroyAllWindows()
            return frame_list

def display_terminal():
    frame_list = get_frame_data()
    while True:
        for i in frame_list:
            print(i)
            time.sleep(1/fps)

# TODO put this in a main() func
parser = argparse.ArgumentParser()
mods = parser.add_mutually_exclusive_group()
parser.add_argument('-r', '--resolution', type=int, default=100,
                    help='Width to resize the image to, in pixels. Higher value means more detail. Default=100')
mods.add_argument('-y','--youtube', type=str, default = None ,
                    help='Use a youtube video as input')
mods.add_argument('-f', '--file', type=str, default = None,
                    help='File to convert to ascii')
args = parser.parse_args()

resolution = args.resolution
if args.youtube:
    url = args.youtube
    vPafy = pafy.new(url)
    play = vPafy.getbest(preftype="webm")
    cap = cv2.VideoCapture(play.url)
elif args.file:
    cap = cv2.VideoCapture(args.file)

fps = cap.get(cv2.CAP_PROP_FPS)
display_terminal()