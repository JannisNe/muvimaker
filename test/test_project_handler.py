import unittest, os

from muvi_maker import main_logger, mv_scratch_key
from muvi_maker.core.project import ProjectHandler, standard_screen_size, standard_framerate, standard_hop_length
from muvi_maker.example_data import example_song
from muvi_maker.core.pictures.base_picture import BasePicture


main_logger.setLevel('DEBUG')
logger = main_logger.getChild(__name__)

sounds = {'main': example_song}

pictures = dict()
pictures['bg'] = [
    'background',
    ['colour: 0'],
    0
]

for i, pic_class in enumerate(BasePicture.subclasses.keys()):
    if pic_class == 'background':
        continue
    pictures[f'{i}'] = [
        pic_class,
        ['colour: main', 'radius: main'],
        i
    ]


class TestProjectHandler(unittest.TestCase):

    def test_project_handler(self):

        ph = ProjectHandler('test_ph_handler', os.environ[mv_scratch_key])
        ph.sound_files = sounds
        ph.pictures = pictures
        ph._main_sound_file = example_song
        video = ph.get_video(
            standard_screen_size,
            standard_hop_length,
            standard_framerate
        )
        video.make_frame_per_frame(0)


# if __name__ == '__main__':
#     main_logger.setLevel('DEBUG')
#     unittest.main()