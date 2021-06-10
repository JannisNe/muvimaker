import numpy as np

from muvimaker import main_logger
from .meta_polygon import MetaPolygon
from .base_picture import BasePicture


logger = main_logger.getChild(__name__)


@BasePicture.register_subclass('meta_regular_polygon')
class MetaRegularPolygon(MetaPolygon):

    def __init__(self, sound_dictionary, param_info, screen_size):
        self.meta_length = float(param_info.pop('meta_length', '2')) * min(screen_size)
        param_info.setdefault('meta_N_sides', '4')
        super().__init__(sound_dictionary, param_info, screen_size)

    @property
    def initial_corner_positions(self):
        L = self.meta_length / (2 * np.sin(self._regular_angle / 2))
        initial_vec = -L * np.array([np.sin(self._regular_angle/2), np.cos(self._regular_angle/2)])
        corner = self.meta_center + initial_vec
        starting_corner_positions = [corner]
        for i in range(self.N_sides - 1):
            toadd = self.side_lengths[i] * self.direction(i)
            corner = corner + toadd
            starting_corner_positions.append(corner)
        return starting_corner_positions

    @property
    def side_lengths(self):
        return np.array([self.meta_length] * self.N_sides)