import PIL
import numpy as np

from .base_picture import BasePicture
from .simple_picture import SimplePicture


@BasePicture.register_subclass('picture_from_file')
class PictureFromFile(SimplePicture):

    def __init__(self, sound_dictionary, param_info, screen_size):

        filename = param_info['filename']
        scale = float(param_info.pop('scale', '1'))
        image = PIL.Image.open(filename)
        new_size = np.array(image.size) * scale
        self._image = image.resize(new_size.astype(int), PIL.Image.NEAREST)

        super().__init__(sound_dictionary, param_info, screen_size)

    def _make_frame_per_frame(self, ind):
        size = np.array(self.screen_size) * 2
        frame = PIL.Image.new('RGBA', tuple(size.astype(int)), (0, 0, 0, 0))
        center = self.center
        angle = self.angle
        radius = self.radius[ind]

        new_size = np.array(self._image.size) * radius
        # only paste the image into the empty frame if the size is bigger than 0 pixels in both dimensions
        if np.all(new_size.astype(int) >= 0.1):
            image = self._image.resize(new_size.astype(int), PIL.Image.NEAREST)
            image = image.rotate(angle, expand=True)
            image_center = np.array(image.size) / 2
            image_upper_left_corner = np.array(center) + image_center * np.array([-1, -1])
            frame.paste(image, box=tuple(image_upper_left_corner.astype(int)))

        return np.array(frame)