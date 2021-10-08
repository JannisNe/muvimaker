from moviepy.editor import VideoFileClip
import PIL, collections
import numpy as np
from skimage import transform

from muvimaker import main_logger
from .base_picture import BasePicture, PictureError
from .simple_picture import SimplePicture


logger = main_logger.getChild(__name__)


@BasePicture.register_subclass('picture_from_video')
class PictureFromVideo(SimplePicture):

    def __init__(self, sound_dictionary, param_info, screen_size):
        filename = param_info['filename']
        self.scale = float(param_info.pop('scale', '1'))
        self.loop = bool(param_info.pop('loop', 'true'))

        # --------------------- Position ----------------------- #
        rel_center = param_info.get('center', '1, 1')

        # If center is given as string, determines the center for all frames
        if isinstance(rel_center, str):
            rel_center = np.array([float(i) for i in rel_center.split(', ')])

        # Center is given as a list-like object for each individual frame
        elif isinstance(rel_center, collections.Sequence):
            rel_center = np.array(rel_center)

        else:
            raise PictureError(f'Type of center is {type(rel_center)} but should be '
                               f'string or sequence!')

        self.center = np.array(screen_size) * rel_center

        self.video = VideoFileClip(filename, audio=False)
        self.fps = self.video.fps
        self._N_frames = int(round(self.video.duration * self.fps))
        super().__init__(sound_dictionary, param_info, screen_size)

    def t(self, ind):
        return ind / self.fps

    def _make_frame_per_frame(self, ind):
        frame = self.video.get_frame(self.t(ind % self._N_frames))
        image = PIL.Image.fromarray(frame)
        new_size = np.array(image.size) * self.scale
        image = image.resize(new_size.astype(int), PIL.Image.NEAREST)
        return np.array(self.postprocess(image, ind))

    @staticmethod
    def _bubble_warp(a, center, radius):
        b = a - center
        d = np.sqrt(np.sum(b ** 2, axis=1))
        mask = (d < radius) & (d > 0)
        direction = b[mask] / d[mask][:, None]
        a[mask] += -radius * (1 - d[mask][:, None] / radius) * direction
        return a.astype(int)

    def postprocess(self, frame, ind):
        frame = super().postprocess(frame, ind)
        args = {'center': self.center,
                'radius': self.radius[ind]}
        frame = transform.warp(image=np.array(frame), inverse_map=self._bubble_warp, map_args=args)
        frame = (frame * 255).astype(np.uint8)
        return frame