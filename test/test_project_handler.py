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

    j += 1

ph_name = 'test_ph_handler'


class TestProjectHandler(unittest.TestCase):

    def test_project_handler(self):
        logger.info('\n\n   testing project handler\n\n')
        ph = ProjectHandler.get_project_handler(ph_name)
        ph.sound_files = sounds
        classes = [l[0] for l in pictures.values()]
        logger.debug(f'testing classes {classes}')
        ph.pictures = pictures
        ph._main_sound_file = example_song
        video = ph.get_video(
            standard_screen_size,
            standard_hop_length,
            standard_framerate
        )
        video.get_frame(10)
        ph.save_me()

    def test_zload_project_handler(self):
        logger.info('\n\n    testing a loaded project handler\n\n')
        ph = ProjectHandler.get_project_handler(ph_name)
        video = ph.get_video(
            standard_screen_size,
            standard_hop_length,
            standard_framerate
        )
        video.get_frame(11)
