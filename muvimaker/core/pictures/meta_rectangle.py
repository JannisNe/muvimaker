import numpy as np

from muvimaker import main_logger
from .meta_polygon import MetaPolygon
from .base_picture import BasePicture


logger = main_logger.getChild(__name__)


@BasePicture.register_subclass('meta_rectangle')
class MetaRectangle(MetaPolygon):

    def __init__(self, sound_dictionary, param_info, screen_size):
        self.meta_length = float(param_info.pop('meta_length', '2')) * screen_size[0]
        self.meta_height = float(param_info.pop('meta_height', '2')) * screen_size[1]
        param_info['meta_N_sides'] = 4

        super().__init__(sound_dictionary, param_info, screen_size)

    @property
    def initial_corner_positions(self):
        corner = self.meta_center - np.array([self.meta_length, self.meta_height]) / 2
        starting_corner_positions = [corner]
        for i in range(self.N_sides - 1):
            toadd = self.side_lengths[i] * self.direction(i)
            corner = corner + toadd
            starting_corner_positions.append(corner)
        return starting_corner_positions

    @property
    def side_lengths(self):
        return np.array([self.meta_length, self.meta_height, self.meta_length, self.meta_height])

    # def calculate_angles(self):
    #     """
    #     Calculate angles so the objects always face the same way
    #     """
    #     _angles = [self._regular_angle * i for i in range(self.meta_multiplicity)]
    #     return _angles