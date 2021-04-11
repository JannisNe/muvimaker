from PIL import Image
import gizeh
import numpy as np
import math
import moviepy.editor as mpy
import os
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from moviepy.video.io.bindings import mplfig_to_npimage
# import pyqtgraph as pg

from muvi_maker import main_logger


default_picture = f'{os.path.dirname(os.path.realpath(__file__))}/default/default.jpg'
logger = main_logger.getChild(__name__)


class Video:

    def __init__(self, pictures, soundfile, framerate, duration, screen_size):
        self.pictures = pictures
        self.soundfile = soundfile
        self.framerate = framerate
        self.duration = duration
        self.screen_size = screen_size

    def _ind(self, t):
        return int(math.floor(t * self.framerate))

    def _t(self, ind):
        return ind / self.framerate

    def make_frame_per_frame(self, ind):

        bg = Image.fromarray(self.pictures[0].get_frame(ind)).convert('RGBA')

        for p in self.pictures[1:]:
            frame = Image.fromarray(p.get_frame(ind)).convert('RGBA')
            bg.paste(frame, (0, 0), frame)

        return np.array(bg.convert('RGB'))

    def make_frame_per_time(self, t):
        ind = self._ind(t)
        return self.make_frame_per_frame(ind)

    def make_video(self, filename):
        clip = mpy.VideoClip(self.make_frame_per_time, duration=self.duration)
        logger.debug(f'clip size is {clip.size}')
        logger.debug(f'setting {self.soundfile} as audio')
        audio = mpy.AudioFileClip(self.soundfile)
        clip_with_audio = clip.set_audio(audio)
        clip_with_audio.write_videofile(filename, fps=self.framerate)
