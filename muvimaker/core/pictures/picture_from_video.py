from moviepy.editor import VideoFileClip

from .base_picture import BasePicture


@BasePicture.register_subclass('picture_from_video')
class PictureFromVideo(BasePicture):

    def __init__(self, sound_dictionary, param_info, screen_size):
        filename = param_info['filename']
        scale = float(param_info.pop('scale', '1'))
        video = VideoFileClip(filename, audio=False)
        super().__init__(sound_dictionary, param_info, screen_size)

    def _make_frame_per_frame(self, ind):
        pass