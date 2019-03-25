# Ascii-py

Converts images or videos to ASCII in the terminal. Can take files, links, or use webcam for image/video input.

## Usage

### Installation

> pip install -r requirements.txt

### **ascii_image.py**

```
usage: ascii_image.py [-r RESOLUTION] [--html] [-c] [-b]
                      [-f FILE | -u URL]

arguments:
  -h, --help            show this help message and exit
  -f, --file            Specify an image file to turn into ASCII.
  -u, --url             Specify an image URL to turn into ASCII.
  -r, --resolution      Width to resize the image to, in pixels. Higher value
                        means more detail. Default=100
  --html                Output an HTML file containing the result to the
                        current directory.
  -c, --color           Print the ascii charecters to the console in color.
  -b, --background      Print the ascii charecters to the console with colored
                        backgrounds
```

### **ascii_video.py**

```
usage: ascii_video.py [-r RESOLUTION] [-rt] [-y YOUTUBE | -f FILE | -w]

arguments:
  -h, --help            show this help message and exit 
  -r, --resolution      Width to resize the image to, in pixels. Higher value
                        means more detail. Default = 100
  -rt, --realtime       Get frame data and play video simultaneously. Will
                        cause slowdown on larger resolutions
  -y, --youtube         Use a youtube video as input
  -f, --file            Use a video file as input
  -w, --webcam          Use webcam as video input
```

## Examples

### ascii_image.py

> python ascii_image.py --file .\tests\img.png --resolution 200 --color

![Output](https://github.com/AliShazly/ascii-py/blob/master/tests/img_output_01.png)

> python ascii_image.py --file .\tests\img.png --resolution 200 --color --background

![Output](https://github.com/AliShazly/ascii-py/blob/master/tests/img_output_02.PNG)

### ascii_video.py

> python ascii_video.py --file .\tests\vid.mp4 --realtime

![Output](https://github.com/AliShazly/ascii-py/blob/master/tests/vid_output_01.gif)

## Limitations

- Color palette is limited to  due to 8 colors due to Windows terminal limitations
- Color only works on images, planning to bring to videos soon
