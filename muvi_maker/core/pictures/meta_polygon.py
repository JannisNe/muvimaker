import abc

import numpy as np

from muvi_maker import main_logger
from .meta_picture import MetaPicture


logger = main_logger.getChild(__name__)


class MetaPolygon(MetaPicture, abc.ABC):

    def __init__(self, sound_dictionary, param_info, screen_size):
        self.N_sides = param_info['N_sides']
        self._regular_angle = 2 * np.pi / self.N_sides
        super().__init__(sound_dictionary, param_info, screen_size)

    @property
    @abc.abstractmethod
    def initial_corner_positions(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def side_lengths(self):
        raise NotImplementedError

    def direction(self, N_side):
        N_side = np.array(N_side)
        angle = np.array([
            np.cos(self._regular_angle * N_side),
            np.sin(self._regular_angle * N_side)
        ])
        axes = list(range(1, len(N_side.shape) + 1)) + [0]
        angle = np.transpose(angle, axes=axes)
        return angle

    def calculate_centers(self):

        logger.debug(f'initial corner positions are {self.initial_corner_positions}, center is {self.meta_center}')

        # calculate the rectlen
        start_rectlens = [1 / self.meta_multiplicity * i for i in range(self.meta_multiplicity)]
        rectlen_velocity = 1 / self.meta_period_on_shape
        rectlens = np.array([
            [
                (start_rectlens[x] + sum(rectlen_velocity[:j])) % 1
                for j in range(len(rectlen_velocity))
            ]
            for x in range(self.meta_multiplicity)
        ])

        # calculate the position from the rectlen
        N_side = np.floor(rectlens * self.N_sides).astype(int)
        perc_of_side = rectlens * self.N_sides - np.floor(N_side)
        logger.debug(f'first entries of perc_of_side: {perc_of_side[:,0]}')

        # for o in [
        #     np.array(starting_corner_positions)[N_side],
        #     N_side,
        #     perc_of_side,
        #     self.side_lengths[N_side],
        #     self.direction(N_side)
        # ]:
        #     logger.debug(f'shape is {np.shape(o)}')

        side_evol = perc_of_side * self.side_lengths[N_side]
        position = np.array(self.initial_corner_positions)[N_side] + side_evol[:,:,None] * self.direction(N_side)
        logger.debug(f'shape of position is {np.shape(position)}, first entries {position[:,0,:]}')
        logger.debug(f'shape of position minus center is {np.shape(position - self.meta_center)}')

        # rotate each position around the meta center with 2*pi/meta_period
        radial_velocity = 2 * math.pi / self.meta_period
        p = position - self.meta_center
        logger.debug(f'NaN in p: {np.any(np.isnan(p))}')
        positions_on_unity_circle = np.arctan2(p[:,:,1], p[:,:,0])
        logger.debug(f'first positions on unity circle are {positions_on_unity_circle[:,0]/np.pi}')
        logger.debug(f'NaN in positions on unity circle: {np.any(np.isnan(positions_on_unity_circle))}')
        positions_on_unity_circle += np.cumsum(radial_velocity)
        logger.debug(f'after adding radial velocity {positions_on_unity_circle[:, 0]/np.pi}')

        # add the radius to the center at the calculated angle
        radius_from_meta_center = np.sqrt(p[:,:,0]**2 + p[:,:,1]**2)
        vector_from_meta_center = np.transpose(
            np.array((
                np.cos(positions_on_unity_circle),
                np.sin(positions_on_unity_circle)
            )) * radius_from_meta_center,
            axes=(1, 2, 0)
        )
        new_positions = self.meta_center + vector_from_meta_center

        logger.debug(f'shape of new positions is {np.shape(new_positions)}')
        logger.debug(f'first positions are {new_positions[:,0,:]}')

        return new_positions