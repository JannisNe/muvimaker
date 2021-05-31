import abc, collections
import numpy as np

from muvi_maker.core.pictures.base_picture import BasePicture, PictureError


class SimplePicture(BasePicture, abc.ABC):
    """A simple BaseClass that provides radius and position"""

    def __init__(self, sound_dictionary, param_info, screen_size):

        super().__init__(sound_dictionary, param_info, screen_size)
        self.angle = float(param_info.pop('angle', '0'))

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

        # ---------------------- Radius ------------------------ #
        radius_sound_name = param_info['radius']
        max_radius = float(param_info.get('max_radius', 0.5)) * min(self.screen_size)
        radius_smooth = int(param_info.get('radius_smooth', 1))
        radius_saturation_threshold = float(param_info.get('radius_saturation_threshold', 1))
        radius_sensitive_threshold = float(param_info.get('radius_sensitive_threshold', 0))

        radius_sound = self.sound_dict[radius_sound_name]
        radius = radius_sound.get_power()

        # if smooth is given select the maximum radius value
        # from the given number of frames
        if radius_smooth > 1:
            rl = list()
            for i in range(len(radius)):
                h, b = np.histogram(radius[i:i + radius_smooth])
                rl.append(b[np.argmax(h)])
            radius = np.array(rl)

        # all values below the sensitive threshold will be zero
        radius_sensitive_mask = radius <= max(radius) * radius_sensitive_threshold
        radius[radius_sensitive_mask] = 0.

        # all values above the saturation threshold will be equal to the maximum
        # of the values below this threshold
        radius_saturation_mask = radius >= max(radius) * radius_saturation_threshold
        radius[radius_saturation_mask] = max(radius[~radius_saturation_mask])

        # scale so the maximum of radius is the given value
        radius = radius / max(radius) * max_radius

        self.radius = radius