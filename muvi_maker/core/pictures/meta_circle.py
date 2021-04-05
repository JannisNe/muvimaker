import math
import numpy as np

from muvi_maker import main_logger
from .meta_picture import MetaPicture
from .base_picture import BasePicture


logger = main_logger.getChild(__name__)


@BasePicture.register_subclass('meta_circle')
class MetaCircle(MetaPicture):

    def __init__(self, sound_dictionary, param_info, screen_size):
        self.meta_radius = float(param_info.pop('meta_radius', '1')) * min(screen_size)
        super().__init__(sound_dictionary, param_info, screen_size)

    def calculate_centers(self):

        radial_velocity = 2 * math.pi / self.meta_period

        starting_positions_on_unit_circle = [
            2 * math.pi / self.meta_multiplicity * x
            for x in range(self.meta_multiplicity)
        ]

        logger.debug(f'shape of starting positions is {np.shape(starting_positions_on_unit_circle)}')

        positions_on_unity_circle = [
            [
                starting_positions_on_unit_circle[x] + sum(radial_velocity[:j])
                for j in range(len(radial_velocity))
            ]
            for x in range(self.meta_multiplicity)
        ]

        logger.debug(f'shape of positions on circle is {np.shape(positions_on_unity_circle)}')
        logger.debug(f'shape of position is {np.shape(positions_on_unity_circle[0])}')
        logger.debug(f'shape of angle is {np.shape(positions_on_unity_circle[0][0])}')

        centers = [
            [
                (np.cos(pos)*self.meta_radius + self.meta_center[0],
                 np.sin(pos)*self.meta_radius + self.meta_center[1])
                for pos in positions
            ]
            for positions in positions_on_unity_circle
        ]

        logger.debug(f'shape of centers is {np.shape(centers)}')

        return centers
