import gizeh

from muvi_maker import main_logger
from .base_picture import BasePicture
from .base_form import BaseForm


logger = main_logger.getChild(__name__)


@BasePicture.register_subclass('star')
class Star(BaseForm):

    def __init__(self, sound_dict, param_info, screen_size):
        super(Star, self).__init__(sound_dict, param_info, screen_size)

    def draw(self, ind):
        star = gizeh.star(
            radius=self.radius[ind] * 2,
            nbranches=10, xy=self.center, fill=self.color[ind]
        )
        star.draw(self.surface)