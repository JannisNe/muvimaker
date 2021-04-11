import unittest

from muvi_maker import main_logger
from muvi_maker.core.pictures import BasePicture
from muvi_maker.core.project import ProjectHandler, standard_screen_size, standard_framerate, standard_hop_length
from muvi_maker.core.video import Video
from muvi_maker.example_data import example_song


logger = main_logger.getChild(__name__)
ph_name = 'test_ph_handler'


class TestPreComputedPicture(unittest.TestCase):

    def test_picture(self):
        logger.info('\n\n    test PreComputedPicture\n\n')
        ph = ProjectHandler.get_project_handler(ph_name)
        video = ph.get_video(
            standard_screen_size,
            standard_hop_length,
            standard_framerate
        )
        frames = [video.get_frame(10)]

        pre_computed_picture = BasePicture.create(
            'pre_computed_picture',
            None,
            {'frames': frames},
            None
        )

        analyser_video = Video(
            [pre_computed_picture],
            ph.main_sound_file,
            standard_framerate,
            ph.length,
            standard_screen_size
        )

        analyser_video.make_frame_per_frame(0)