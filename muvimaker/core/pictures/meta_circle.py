import math
import numpy as np

from muvimaker import main_logger
from .meta_picture import MetaPicture
from .base_picture import BasePicture


logger = main_logger.getChild(__name__)


@BasePicture.register_subclass('meta_circle')
class MetaCircle(MetaPicture):

    def __init__(self, sound_dictionary, param_info, screen_size):
        self._cached_postitions_on_unity_circle = None
        self.meta_radius = float(param_info.pop('meta_radius', '1')) * min(screen_size)
        super().__init__(sound_dictionary, param_info, screen_size)

    @property
    def positions_on_unity_circle(self):
        if isinstance(self._cached_postitions_on_unity_circle, type(None)):
            radial_velocity = 2 * math.pi / self.meta_period

            starting_positions_on_unit_circle = [
                2 * math.pi / self.meta_multiplicity * x + self.meta_phase * 2 * math.pi
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

            self._cached_postitions_on_unity_circle = positions_on_unity_circle

        return self._cached_postitions_on_unity_circle

    def calculate_centers(self):
        centers = [
            [
                (np.cos(pos)*self.meta_radius + self.meta_center[0],
                 np.sin(pos)*self.meta_radius + self.meta_center[1])
                for pos in positions
            ]
            for positions in self.positions_on_unity_circle
        ]

        logger.debug(f'shape of centers is {np.shape(centers)}')

        return centers

    def calculate_angles(self):
        """
        Calculate angles so the objects always face the same way
        """
        return np.array(self.positions_on_unity_circle)