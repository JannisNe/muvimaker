import gizeh
import matplotlib.cm as cm

from .base_picture import BasePicture


@BasePicture.register_subclass('background')
class Background(BasePicture):


    def __init__(self, sound_dictionary, param_info, screen_size):
        super().__init__(sound_dictionary, param_info, screen_size)

        self.colour = float(param_info['colour'])
        cmap_name = param_info.get('cmap_name', 'magma')
        self.cmap = cm.get_cmap(cmap_name)

    def make_frame_per_frame(self, ind):
        surface = gizeh.Surface(int(self.screen_size[0] * 2), int(self.screen_size[1] * 2),
                                bg_color=self.cmap(self.colour))
        return surface.get_npimage()