import gizeh, math

from muvi_maker import main_logger
from .base_picture import BasePicture
from .base_form import BaseForm


logger = main_logger.getChild(__name__)


@BasePicture.register_subclass('star')
class Star(BaseForm):

    def __init__(self, sound_dict, param_info, screen_size):
        self.nbranches = int(param_info.pop('nbranches', '10'))
        # self.angle = float(param_info.pop('angle', '0'))
        self.period = float(param_info.pop('period', 'inf'))
        super().__init__(sound_dict, param_info, screen_size)

    def draw(self, ind):
        omega = 2 * math.pi / self.period
        angle = self.angle + omega * float(ind)

        self.kwargs['nbranches'] = self.nbranches
        self.kwargs['angle'] = angle

        star = gizeh.star(
            radius=self.radius[ind],
            xy=self.center,
            fill=self.color[ind],
            **self.kwargs
        )
        star.draw(self.surface)