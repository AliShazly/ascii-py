import numpy as np
import cv2
from PIL import Image
import time
import sys
import os
import pafy
import argparse

chars = ['.', ',', ':', ';', '+', '*', '?', '%', 'S', '#', '@'] # TODO: Change char list

def cv_to_pillow(image):
    img_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_RGB)
    return pil_img

def image_resize(image, width=None, height=None):
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

def image_to_ascii_grayscale(image, args):
    resolution = args.resolution
    image = image.convert('L')
    grayscale_values = list(image.getdata())
    ascii_pixels = ''.join(chars[i//25] for i in grayscale_values)
    ascii_image = [ascii_pixels[i:i+resolution]
                   for i in range(0, len(ascii_pixels), resolution)]
    return ascii_image

def get_video_data(args):
    frame_list = []
    if args.youtube:
        try:
            url = args.youtube[-11:]
            vPafy = pafy.new(url)
            play = vPafy.getbest(preftype="webm")
            cap = cv2.VideoCapture(play.url)
        except AttributeError as e:
            sys.stdout.write(f'ERROR: Youtube music links do not currently work')
            sys.exit()
    elif args.file:
        try:
            cap = cv2.VideoCapture(args.file)
            if cap.read() == (False, None):
                raise FileNotFoundError(f'File path {args.file} not found.')
        except FileNotFoundError as e:
            sys.stdout.write(f'ERROR: {e}')
            sys.exit()
    elif args.webcam:
        try:
            cap = cv2.VideoCapture(0)
            if cap.read() == (False, None):
                raise FileNotFoundError(f'Webcam not found.')
        except FileNotFoundError as e:
            sys.stdout.write(f'ERROR: {e}')

    fps = cap.get(cv2.CAP_PROP_FPS)
    if args.realtime or args.webcam:
        return cap, fps
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    iteration = 0
    while True:
        print(f'Converting to ASCII, do not resize window... {int(iteration/length*100)}%', end = '\r')
        iteration +=1
        ret, frame = cap.read()
        if ret:
            pil_frame = cv_to_pillow(frame)
            resized, dim = image_resize(pil_frame, width=args.resolution)
            ascii_image = image_to_ascii_grayscale(resized, args)
            frame_list.append('\n'.join(ascii_image))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            os.system(f'mode con: cols={dim[0]} lines={dim[1]}')
            cap.release()
            cv2.destroyAllWindows()
            return frame_list, fps

def display_terminal(args):
    frame_list, fps = get_video_data(args)
    while True:
        for i in frame_list:
            sys.stdout.write(i)
            time.sleep(1/fps)

# TODO: Maybe refactor some stuff, this function is just repeated code from get_video_data
def display_realtime(args):
    cap, fps = get_video_data(args)
    while True:
        try:
            ret, frame = cap.read()
            pil_frame = cv_to_pillow(frame)
            resized, dim = image_resize(pil_frame, width=args.resolution)
            frame_pos = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            # Only resizing the image on the first iteration of the loop
            if frame_pos <= 2:
                os.system(f'mode con: cols={dim[0]} lines={dim[1]}')
            ascii_image = image_to_ascii_grayscale(resized, args)
        except cv2.error:
            cap, fps = get_video_data(args)
        sys.stdout.write('\n'.join(ascii_image))
        time.sleep(1/fps)

def main(): 
    # TODO: Merge with webcam
    parser = argparse.ArgumentParser()
    inputs = parser.add_mutually_exclusive_group()
    parser.add_argument('-r', '--resolution', type=int, default=100,
                        help='Width to resize the image to, in pixels. Higher value means more detail.')
    parser.add_argument('-rt', '--realtime', action='store_true',
                        help='Get frame data and play video simultaneously. Will cause slowdown on larger resolutions')
    inputs.add_argument('-y', '--youtube', type=str, default=None,
                      help='Use a youtube video as input')
    inputs.add_argument('-f', '--file', type=str, default=None,
                      help='File to convert to ascii')
    inputs.add_argument('-w', '--webcam', action='store_true',
                      help='Use webcam as video input')
    args = parser.parse_args()
    if args.realtime or args.webcam:
        display_realtime(args)
    else:
        display_terminal(args)

if __name__ == '__main__':
    main()
