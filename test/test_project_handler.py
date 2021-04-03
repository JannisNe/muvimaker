import unittest, os

from muvi_maker import main_logger, mv_scratch_key
from muvi_maker.core.project import ProjectHandler, standard_screen_size, standard_framerate, standard_hop_length
from muvi_maker.example_data import example_song
from muvi_maker.core.pictures.base_picture import BasePicture


logger = main_logger.getChild(__name__)

sounds = {'main': example_song}

pictures = dict()
pictures['bg'] = [
    'background',
    ['colour: 0'],
    '0'
]

for i, pic_class in enumerate(BasePicture.subclasses()):

    pictures[f'{i}'] = [
        pic_class,
        ['colour: main', 'radius: main'],
        f'{i}'
    ]

filename = os.path.join(os.environ[mv_scratch_key], 'test_ph_handler.pkl')


class TestProjectHandler(unittest.TestCase):

    def test_project_handler(self):

        ph = ProjectHandler.get_project_handler(filename=filename)
        ph.sound_files = sounds
        ph.pictures = pictures
        ph._main_sound_file = example_song
        video = ph.get_video(
            standard_screen_size,
            standard_hop_length,
            standard_framerate
        )
        video.make_frame_per_frame(0)