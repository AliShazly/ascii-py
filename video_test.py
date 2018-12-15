from copy import deepcopy
import sys
from asciimatics.exceptions import ResizeScreenError
from asciimatics.paths import Path
from asciimatics.renderers import StaticRenderer, ColourImageFile, FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.effects import Print, Sprite, BannerText
import json

class Video(Sprite):
    def __init__(self, screen, path, start_frame=0, stop_frame=0):
        frames = json.loads(open('frame_list.json').read())
        images = []
        for image in frames:
            images.append(image)
        super(Video, self).__init__(
            screen,
            renderer_dict={
                "default": StaticRenderer(images=images),
            },
            path=path,
            start_frame=start_frame,
            stop_frame=stop_frame)


def display_screen(screen):
    scenes = []
    center = (screen.width // 2, screen.height // 2)
    path = Path()
    path.jump_to(center[0], center[1])
    effects = [Video(screen, path)]
    scenes.append(Scene(effects, 0,0))
    screen.play(scenes, stop_on_resize=True, repeat=False)


if __name__ == "__main__":
    while True:
        try:
            Screen.wrapper(display_screen)
            sys.exit(0)
        except ResizeScreenError:
            pass
