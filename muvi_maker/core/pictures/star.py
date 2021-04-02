import gizeh

from muvi_maker import main_logger
from .base_picture import BasePicture
from .base_form import BaseForm


logger = main_logger.getChild(__name__)


@BasePicture.register_subclass('star')
class Star(BaseForm):

    def __init__(self, sound_dict, param_info, screen_size):
        nbranches = int(param_info.pop('nbranches', '10'))
        self.kwargs = {'nbranches': nbranches}
        super(Star, self).__init__(sound_dict, param_info, screen_size)

    @property
    def form(self):
        return 'star'

    # def draw(self, ind):
    #     star = gizeh.star(
    #         radius=self.radius[ind],
    #         nbranches=self.nbranches,
    #         xy=self.center,
    #         fill=self.color[ind]
    #     )
    #     star.draw(self.surface)