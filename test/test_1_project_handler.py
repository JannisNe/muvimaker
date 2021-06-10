import unittest

from muvimaker import main_logger
from muvimaker.core.project import ProjectHandler, standard_screen_size, standard_framerate, standard_hop_length
from muvimaker.example_data import example_song, example_pic
from muvimaker.core.pictures.base_picture import BasePicture


main_logger.setLevel('DEBUG')
logger = main_logger.getChild(__name__)

sounds = {'main': example_song}

pictures = dict()
pictures['bg'] = [
    'background',
    ['colour: 0'],
    '0'
]

j = 1

for pic_class in BasePicture.subclasses.keys():

    if pic_class in ['background', 'pre_computed_picture']:
        continue

    n = f'{j}: {pic_class}'
    pictures[n] = [
        pic_class,
        ['colour: main', 'radius: main'],
        f'{j}'
    ]

    if 'meta' in pic_class:
        pictures[n][1].append('pictures_class: star')

    if 'picture_from_file' in pic_class:
        pictures[n][1].append(f'filename: {example_pic}')
        pictures[n][1].append('scale: 0.01')

    j += 1

ph_name = 'test_ph_handler'
ph = ProjectHandler.get_project_handler(ph_name)
ph.pictures = pictures
ph._main_sound_file = example_song
ph.sound_files = sounds
ph.save_me()


class TestProjectHandler(unittest.TestCase):

    def test_a_project_handler(self):
        logger.info('\n\n   testing project handler\n\n')
        classes = [l[0] for l in pictures.values()]
        logger.debug(f'testing classes {classes}')
        video = ph.get_video(
            standard_screen_size,
            standard_hop_length,
            standard_framerate
        )
        video.make_frame_per_frame(10)

    def test_b_load_project_handler(self):
        logger.info('\n\n    testing a loaded project handler\n\n')
        ph_loaded = ProjectHandler.get_project_handler(ph_name)
        video = ph_loaded.get_video(
            standard_screen_size,
            standard_hop_length,
            standard_framerate
        )
        video.make_frame_per_frame(11)

    def test_c_test_analyse(self):
        logger.info('\n\n   test analyse function \n\n')
        ph.analyse((200, 100), standard_hop_length, 20)

    def test_d_test_make_video(self):
        logger.info('\n\n   testing making video \n\n')
        ph.make_video(screen_size=(100, 100), hop_length=standard_hop_length, framerate=20)