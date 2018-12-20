# Ascii-py

Converts images or videos to ASCII in the terminal. Can take files, links, or use webcam for image/video input. Color is currently only supported for images, I hope to bring it to videos soon.


## Usage

### Installation
> $pip install -r requirements.txt

### **ascii_image.py**

```
usage: ascii_image.py [image_path] [-r RESOLUTION] [--html | -c] [-b]

arguments:
  -h, --help            show this help message and exit
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
> $python ascii_image.py .\tests\img.png --color 

**Input:**

![](https://github.com/AliShazly/ascii-py/blob/master/tests/img.png)

**Output:**

![](https://github.com/AliShazly/ascii-py/blob/master/tests/img_output_01.png)

### ascii_video.py
> $python ascii_video.py -file .\tests\vid_02.mp4 -realtime

**Input:**
`./tests/vid_02.mp4`

**Output:**

![Output](https://github.com/AliShazly/ascii-py/blob/master/tests/vid_output_01.gif)
