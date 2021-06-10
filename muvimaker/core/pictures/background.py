import gizeh
import matplotlib.cm as cm
import numpy as np

from .base_picture import BasePicture


@BasePicture.register_subclass('background')
class Background(BasePicture):

    def __init__(self, sound_dictionary, param_info, screen_size):
        super().__init__(sound_dictionary, param_info, screen_size)

        colour = param_info['colour']

        try:
            c = float(colour)
            cmap_name = param_info.get('cmap_name', 'magma')
            cmap = cm.get_cmap(cmap_name)
            self.colour = cmap(c)

        except ValueError:

            if colour in ['none', 'None', 'transparent']:
                self.colour = None

            elif ',' in colour and len(colour.split(',')) == 3:
                self.colour = tuple(np.array(colour.split(',')).astype(int))

            else:
                raise ValueError(f'Value {colour} for parameter colour not understood!')

        cmap_name = param_info.get('cmap_name', 'magma')
        self.cmap = cm.get_cmap(cmap_name)

    def _make_frame_per_frame(self, ind):
        surface = gizeh.Surface(int(self.screen_size[0] * 2), int(self.screen_size[1] * 2),
                                bg_color=self.colour)
        return surface.get_npimage(transparent=True)