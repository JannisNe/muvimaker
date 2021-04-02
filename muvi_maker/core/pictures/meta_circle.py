from muvi_maker import main_logger
from .meta_picture import MetaPicture


logger = main_logger.getChild(__name__)


class MetaCircle(MetaPicture):

    def __init__(self, sound_dictionary, param_info, screen_size):
        self.meta_radius = param_info.pop('meta_radius', '1')
        super().__init__(sound_dictionary, param_info, screen_size)

    def calculate_centers(self):
        pass