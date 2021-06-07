from PIL import Image
import numpy as np
import math, os
import moviepy.editor as mpy

from muvi_maker import main_logger


default_picture = f'{os.path.dirname(os.path.realpath(__file__))}/default/default.jpg'
logger = main_logger.getChild(__name__)


class Video:

    codec_extension_map = np.array([
        ('rawvideo', 'avi'),
        ('png', 'avi'),
        ('mp4', 'mpeg4')
    ],
        dtype={
            'names': ['codec', 'extension'],
            'format': ['<u30', '<u30']
        }
    )

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

    def make_video(self, filename, codec):
        clip = mpy.VideoClip(self.make_frame_per_time, duration=self.duration)
        logger.debug(f'clip size is {clip.size}')
        logger.debug(f'setting {self.soundfile} as audio')
        audio = mpy.AudioFileClip(self.soundfile)
        clip_with_audio = clip.set_audio(audio)

        logger.debug('guess codec from extension')
        codec_mask = Video.codec_extension_map['codec'] == codec
        if not np.any(codec_mask):
            raise VideoError(f'No file extension found for codec {codec}')
        extension = Video.codec_extension_map['extension'][codec_mask]
        filename += f'.{extension}'

        logger.debug(f'codec is {codec}')
        logger.debug(f'filename is {filename}')

        clip_with_audio.write_videofile(filename, fps=self.framerate, codec=codec, audio_codec='aac')


class VideoError(Exception):
    pass