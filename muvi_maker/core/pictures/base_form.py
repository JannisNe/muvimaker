import abc

import gizeh
import numpy as np
import matplotlib.cm as cm
import collections

from muvi_maker import main_logger
from .base_picture import PictureError
from .simple_picture import SimplePicture

logger = main_logger.getChild(__name__)


class BaseForm(SimplePicture, abc.ABC):

    def __init__(self, sound_dict, param_info, screen_size):
        super().__init__(sound_dict, param_info, screen_size)

        self.surface = None
        self.kwargs = dict()

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

        # ---------------------- Colour ------------------------ #
        colour_sound_name = param_info['colour']
        colour_cmap = param_info.get('cmap', 'plasma')
        colour_mode = param_info.get('colour_mode', 'level')
        colour_sound = self.sound_dict[colour_sound_name]
        cmap = cm.get_cmap(colour_cmap)

        # get the colour based on the volume level of the sound
        if colour_mode == 'level':
            colour_smooth = int(param_info.get('colour_smooth', 1))
            colour_chroma = colour_sound.get_chroma()
            max_inds = [np.argmax(c) / len(c) for c in colour_chroma]

            if colour_smooth > 1:
                cl = list()
                for i in range(len(max_inds)):
                    h, b = np.histogram(max_inds[i:i + colour_smooth])
                    cl.append(b[np.argmax(h)])
                color = [cmap(cli) for cli in cl]

            else:
                color = [cmap(imi) for imi in max_inds]

        # get the colour based on a trigger recieved from the sound
        # every time a trigger is recieved change the colour randomly
        elif colour_mode == 'trigger':
            trigger_source = param_info.get('colour_trigger_source', 'get_percussive_power')
            threshold = float(param_info.get('colour_trigger_threshold', 0.5))
            seed = int(param_info.get('colour_trigger_seed', 666))
            rng = np.random.default_rng(seed=seed)

            trigger_values = colour_sound.__getattribute__(trigger_source)()
            normed_trigger = trigger_values / max(trigger_values)
            trigger = normed_trigger >= threshold

            ic = cmap(rng.uniform())
            color = list()
            for trigger_now in trigger:
                if trigger_now:
                    ic = cmap(rng.uniform())
                color.append(ic)

        else:
            raise ValueError(f"Value {colour_mode} for parameter 'colour_mode' not understood!")

        self.color = color

    def create_surface(self):
        self.surface = gizeh.Surface(int(self.screen_size[0] * 2), int(self.screen_size[1] * 2))

    def _make_frame_per_frame(self, ind):
        self.create_surface()
        self.draw(ind)
        np_frame = self.surface.get_npimage(transparent=True)
        frame = self.postprocess(np_frame, ind)
        return np.array(frame)

    @abc.abstractmethod
    def draw(self, ind):
        pass
