import abc, collections, PIL
import numpy as np

from muvi_maker import main_logger
from muvi_maker.core.pictures.base_picture import BasePicture, PictureError


logger = main_logger.getChild(__name__)


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
        radii = ['radius', 'radius_spread']
        self.radius = self.radius_spread = None

        defaults = {
            # Radius of shape
            'radius': None,
            'max_radius': 0.5,
            'radius_smooth': 1,
            'radius_saturation_threshold': 1,
            'radius_sensitive_threshold': 0,
            # Radius of pixel spread
            'radius_spread': None,
            'max_radius_spread': 0.5,
            'radius_spread_smooth': 1,
            'radius_spread_saturation_threshold': 1,
            'radius_spread_sensitive_threshold': 0
        }

        for attr in radii:
            radius_sound_name = param_info.get(attr, defaults[attr])
            # exit when sound not given
            if not radius_sound_name:
                continue

            # maximum radius
            max_r_key = f'max_{attr}'
            max_radius = float(param_info.get(max_r_key, defaults[max_r_key])) * min(self.screen_size)

            # smoothing the radius
            smooth_key = f'{attr}_smooth'
            radius_smooth = int(param_info.get(smooth_key, defaults[smooth_key]))

            # thresholds
            sat_key = f'{attr}_saturation_threshold'
            sens_key = f'{attr}_sensitive_threshold'
            radius_saturation_threshold = float(param_info.get(sat_key, defaults[sat_key]))
            radius_sensitive_threshold = float(param_info.get(sens_key, defaults[sens_key]))

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
            if np.all(radius_sensitive_mask):
                logger.warning(f'All values below radius_sensitive_threshold '
                               f'{radius_sensitive_threshold*max(radius)}!')
            radius[radius_sensitive_mask] = 0.

            # all values above the saturation threshold will be equal to the maximum
            # of the values below this threshold
            radius_saturation_mask = radius >= max(radius) * radius_saturation_threshold
            if np.any(~radius_saturation_mask):
                radius[radius_saturation_mask] = max(radius[~radius_saturation_mask])
            else:
                logger.warning(f'All values above saturation threshold '
                               f'{max(radius)*radius_saturation_threshold}!')

            # scale so the maximum of radius is the given value
            radius = radius / max(radius) * max_radius

            self.__setattr__(attr, radius)

    def postprocess(self, frame, ind):
        """
        Adds effects to the frame
        :param frame: PIL.Image in mode RGBA or nd.array
        :param ind: index of frame
        :return: PIL.Image
        """

        if not isinstance(frame, PIL.Image.Image):
            frame = PIL.Image.fromarray(frame)

        if not isinstance(self.radius_spread, type(None)):
            frame = frame.effect_spread(self.radius_spread[ind])

        return frame
