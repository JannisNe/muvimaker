import numpy as np
import abc, gizeh, math
from PIL import Image

from muvimaker import main_logger
from .base_picture import BasePicture, PictureError
from .base_form import BaseForm


logger = main_logger.getChild(__name__)


class MetaPicture(BasePicture, abc.ABC):

    name = 9

    def __init__(self, sound_dictionary, param_info, screen_size):

        self.pictures_class = param_info['pictures_class']
        self.meta_multiplicity = int(param_info.pop('meta_multiplicity', '5'))
        meta_center = param_info.pop('meta_center', '1, 1')
        self.meta_center = np.array([float(i) for i in meta_center.split(', ')]) * np.array(screen_size)
        self.meta_phase = float(param_info.get("meta_phase", '0'))

        # ------------------------------------------------------------------------------------------ #
        # ------------------------------ begin meta period ----------------------------------------- #
        # ------------------------------------------------------------------------------------------ #

        # meta period attributes determine how fast the meta shape spins
        # or how fast the pictures move on the meta shape
        # given in frames or attribute of sound that determines the period
        self.meta_period = self.meta_period_on_shape = None
        meta_period_params = ['meta_period', 'meta_period_on_shape']

        meta_period_mode = param_info.pop('meta_period_mode', 'manual')

        # set the period by manually giving the period in frames
        if meta_period_mode == 'manual':
            period_defaults = {p: '100' for p in meta_period_params}

            for attr in period_defaults.keys():
                meta_period = param_info.pop(attr, period_defaults[attr])

                if isinstance(meta_period, str):
                    length = len(list(sound_dictionary.values())[0].get_power())
                    self.__setattr__(attr, np.array([float(meta_period)] * length))
                else:
                    assert len(meta_period)  # this ensures that meta_period is list like
                    self.__setattr__(attr, meta_period)

        # estimate the period from the BPM estimation of sound
        # the periods will be calculated so he combined movement matches the BPM
        elif meta_period_mode == 'estimate_from_sound':
            sound = sound_dictionary[param_info[meta_period_params[0]]]
            meta_period_fraction = float(param_info.pop(meta_period_params[0] + '_fraction', '1'))
            meta_period_factor = float(param_info.pop('meta_period_factor', '1'))

            period = sound.get_period() * meta_period_factor
            pd = dict()
            pd[meta_period_params[0]] = 1 / meta_period_fraction
            pd[meta_period_params[1]] = pd[meta_period_params[0]] / (pd[meta_period_params[0]] - 1) if meta_period_fraction != 1 else np.inf
            length = len(list(sound_dictionary.values())[0].get_power())
            for attr, v in pd.items():
                val = v * period
                logger.debug(f'setting {attr} to {val}')
                self.__setattr__(attr, np.array([val] * length))

        # estimate the period from the BPM estimation from a sound
        # but do it separately for meta_period and meta_period_on_shape
        elif meta_period_mode == 'estimate_from_sound_single':
            raise NotImplementedError

        # ------------------------------------------------------------------------------------------ #
        # ------------------------------- end meta period ------------------------------------------ #
        # ------------------------------------------------------------------------------------------ #

        self.centers = self.calculate_centers()

        try:
            self.angles = self.calculate_angles()
        except NotImplementedError:
            self.angles = None

        super().__init__(sound_dictionary, param_info, screen_size)

        self._picture = BasePicture.create(
            self.pictures_class,
            self.sound_dict,
            self.param_info,
            self.screen_size
        )

    def _make_frame_per_frame(self, ind):

        if isinstance(self._picture, BaseForm):
            surface = gizeh.Surface(int(self.screen_size[0] * 2), int(self.screen_size[1] * 2))
            self._picture.surface = surface

            for i in range(self.meta_multiplicity):

                for attr in ['center', 'angle']:
                    if hasattr(self._picture, attr):
                        attr_list = self.__getattribute__(attr + 's')
                        if not isinstance(attr_list, type(None)):
                            self._picture.__setattr__(attr, attr_list[i][ind])

                self._picture.draw(ind)

            return self._picture.surface.get_npimage(transparent=True)

        else:
            pic = None

            for i in range(self.meta_multiplicity):
                self._picture.center = self.centers[i][ind]
                newpic = Image.fromarray(self._picture._make_frame_per_frame(ind)).convert('RGBA')
                if pic:
                    pic.paste(newpic, (0, 0), newpic)
                else:
                    pic = newpic

            return np.array(pic.convert('RGBA'))

    @abc.abstractmethod
    def calculate_centers(self):
        raise NotImplementedError

    def calculate_angles(self):
        raise NotImplementedError
