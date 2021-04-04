import gizeh

from muvi_maker import main_logger
from .base_picture import BasePicture
from .base_form import BaseForm


logger = main_logger.getChild(__name__)


@BasePicture.register_subclass('star')
class Star(BaseForm):

    def __init__(self, sound_dict, param_info, screen_size):
        nbranches = int(param_info.pop('nbranches', '10'))
        super().__init__(sound_dict, param_info, screen_size)
        self.kwargs['nbranches'] = nbranches

    def draw(self, ind):
        star = gizeh.star(
            radius=self.radius[ind],
            xy=self.center,
            fill=self.color[ind],
            **self.kwargs
        )
        star.draw(self.surface)