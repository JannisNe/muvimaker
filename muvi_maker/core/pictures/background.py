import gizeh
import matplotlib.cm as cm

from .base_picture import BasePicture


@BasePicture.register_subclass('background')
class Background(BasePicture):

    def __init__(self, sound_dictionary, param_info, screen_size):
        super().__init__(sound_dictionary, param_info, screen_size)

        colour = param_info['colour']
        try:
            self.colour = float(colour)
        except ValueError:
            if colour in ['none', 'None', 'transparent']:
                self.colour = param_info['colour']
            else:
                raise ValueError(f'Value {colour} for parameter colour not understood!')

        cmap_name = param_info.get('cmap_name', 'magma')
        self.cmap = cm.get_cmap(cmap_name)

    def _make_frame_per_frame(self, ind):
        bg_color = self.cmap(self.colour) if isinstance(self.colour, float) else None
        surface = gizeh.Surface(int(self.screen_size[0] * 2), int(self.screen_size[1] * 2),
                                bg_color=bg_color)
        return surface.get_npimage()