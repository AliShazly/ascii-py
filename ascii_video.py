import cv2
from PIL import Image
import time
import sys
import os
import pafy
import argparse
import json

from ascii_image import image_resize, image_to_ascii_grayscale

chars = ['.', ',', ':', ';', '+', '*', '?', '%', 'S', '#', '@']  # TODO: Change char list


def cv_to_pillow(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img)
    return pil_img


def get_video_data(cap, resolution):
    frame_list = []
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    iteration = 0
    while True:
        print(f'Converting to ASCII, do not resize window... {int(iteration / length * 100)}%', end='\r')
        iteration += 1
        ret, frame = cap.read()
        if ret:
            pil_frame = cv_to_pillow(frame)
            resized = image_resize(pil_frame, width=resolution)
            width, height = resized.size
            ascii_image = image_to_ascii_grayscale(resized, resolution, chars)
            frame_list.append('\n'.join(ascii_image))
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            os.system(f'mode con: cols={width} lines={height}')
            cap.release()
            cv2.destroyAllWindows()
            return frame_list, width, height


def display_terminal(frame_list, fps):
    while True:
        for i in frame_list:
            sys.stdout.write(i)
            time.sleep(1 / fps)


def display_realtime(cap, fps, resolution):
    while True:
        try:
            ret, frame = cap.read()
            pil_frame = cv_to_pillow(frame)
            resized = image_resize(pil_frame, width=resolution)
            width, height = resized.size
            ascii_image = image_to_ascii_grayscale(resized, resolution, chars)
            # Only resizing the terminal on the first iteration of the loop
            frame_pos = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            if frame_pos <= 2:
                os.system(f'mode con: cols={width} lines={height}')
            sys.stdout.write('\n'.join(ascii_image))
            time.sleep(1 / fps)
        except cv2.error:
            return


def main():
    parser = argparse.ArgumentParser()
    inputs = parser.add_mutually_exclusive_group()
    outputs = parser.add_mutually_exclusive_group()

    parser.add_argument('-r', '--resolution', type=int, default=100,
                        help='Width to resize the image to, in pixels. Higher value means more detail.')
    outputs.add_argument('-rt', '--realtime', action='store_true',
                         help='Get frame data and play video simultaneously. Will cause slowdown on larger resolutions')
    inputs.add_argument('-y', '--youtube', type=str,
                        help='Use a youtube video as input')
    inputs.add_argument('-f', '--file', type=str,
                        help='File to convert to ascii')
    inputs.add_argument('-w', '--webcam', action='store_true',
                        help='Use webcam as video input')
    outputs.add_argument('-j', '--json', action='store_true',
                         help='Output ASCII frame list and info to JSON. To be used for embedding in webpages.')
    args = parser.parse_args()

    if args.youtube:
        try:
            url = args.youtube[-11:]
            v_pafy = pafy.new(url)
            play = v_pafy.getbest(preftype="webm")
            cap = cv2.VideoCapture(play.url)
        except AttributeError:
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

    else:
        try:
            cap = cv2.VideoCapture(0)
            if cap.read() == (False, None):
                raise FileNotFoundError(f'Webcam not found.')
        except FileNotFoundError as e:
            sys.stdout.write(f'ERROR: {e}')
            sys.exit()

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps > 60:
        fps = 30

    if args.realtime or args.webcam:
        display_realtime(cap, fps, args.resolution)

    elif args.json:
        frame_list, width, height = get_video_data(cap, args.resolution)
        values_dict = {
            'width': width,
            'height': height,
            'frame_list': frame_list
        }
        with open('ascii_video.json', 'w') as outfile:
            json.dump(values_dict, outfile)
        print('JSON Exported')

    else:
        frame_list, _, _ = get_video_data(cap, args.resolution)
        display_terminal(frame_list, fps)


if __name__ == '__main__':
    main()
