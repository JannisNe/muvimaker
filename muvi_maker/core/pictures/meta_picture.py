import numpy as np
import abc
from PIL import Image
import gizeh

from muvi_maker import main_logger
from .base_picture import BasePicture, PictureError
from .base_form import BaseForm


logger = main_logger.getChild(__name__)


@BasePicture.register_subclass('meta_circle')
class MetaPicture(BasePicture, abc.ABC):

    def __init__(self, sound_dictionary, param_info, screen_size):

        self.pictures_class = param_info['pictures_class']
        self.meta_multiplicity = int(param_info.pop('meta_multiplicity', '5'))
        self.meta_center = param_info.pop('meta_center', '1, 1')

        # given in seconds or attribute of sound that determines the period
        meta_period = param_info.pop('meta_period', '10')

        if isinstance(meta_period, str):

            if meta_period in self.sound_dict:
                # period will be determined by a Sound instance
                power = self.sound_dict[meta_period].get_power()
                meta_min_period = param_info.pop('meta_min_period')
                p = np.minimum(power / max(power), meta_min_period)
                self.meta_period = p

            else:
                self.meta_period = float(meta_period)

        else:
            self.meta_period = meta_period

        self.centers = self.calculate_centers()

        super().__init__(sound_dictionary, param_info, screen_size)

        self._picture = BasePicture.create(
            self.pictures_class,
            self.sound_dict,
            self.param_info,
            self.screen_size
        )

    def make_frame_per_frame(self, ind):

        if isinstance(self._picture, BaseForm):
            surface = gizeh.Surface(int(self.screen_size[0] * 2), int(self.screen_size[1] * 2))
            self._picture.surface = surface

            for i in range(self.meta_multiplicity):
                self._picture.center = self.centers[i][ind]
                self._picture.draw(ind)

            return self._picture.surface.get_npimage(transparent=True)

        else:

            self._picture.center = self.centers[0]
            pic = None

            for i in range(self.meta_multiplicity - 1):
                self._picture.center = self.centers[i+1][ind]
                newpic = Image.fromarray(self._picture.make_frame_per_frame(ind)).convert('RGBA')
                if pic:
                    pic = pic.paste(newpic, (0, 0), pic)
                else:
                    pic = newpic

            return np.array(pic.convert('RGB'))

    @abc.abstractmethod
    def calculate_centers(self):
        pass