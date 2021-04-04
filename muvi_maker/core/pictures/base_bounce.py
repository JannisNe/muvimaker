import gizeh, abc

from muvi_maker import main_logger
from .base_picture import BasePicture


logger = main_logger.getChild(__name__)


class BaseBounce(BasePicture, abc.ABC):

    def __init__(self, sound_dict, param_info, screen_size):

        self.multiplicity = int(param_info.pop('multiplicity', 3))
        self.radius_factor = float(param_info.pop('radius_factor', 1))
        self.radius_add = float(param_info.pop('radius_add', 2))
        self.max_stroke_width = float(param_info.pop('max_stroke_width', 8))
        self.min_stroke_width = float(param_info.pop('min_stroke_width', 1))
        self.stroke_width_decline_order = float(param_info.pop('stroke_width_decline_order', 2))

        self._b = (self.min_stroke_width - self.max_stroke_width * self.multiplicity ** self.stroke_width_decline_order) / \
                  (1 - self.multiplicity ** self.stroke_width_decline_order)
        self._a = self.max_stroke_width - self._b

        super().__init__(sound_dict, param_info, screen_size)

    def stroke_width(self, j):
        return self._a * j ** self.stroke_width_decline_order + self._b
