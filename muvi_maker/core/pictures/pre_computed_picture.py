from .base_picture import BasePicture


@BasePicture.register_subclass('pre_computed_picture')
class PreComputedPicture(BasePicture):

    def __init__(self, sound_dictionary, param_info, screen_size):
        self._frames = param_info['frames']
        super().__init__(sound_dictionary, param_info, screen_size)

    def _make_frame_per_frame(self, ind):
        return self._frames[ind]