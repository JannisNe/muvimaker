import os
import shutil
import pickle
from tqdm import tqdm
import numpy as np

from muvi_maker import main_logger, mv_scratch_key
from muvi_maker.core.sound import Sound, SoundError
from muvi_maker.core.pictures import BasePicture, PictureError
from muvi_maker.core.video import Video


logger = main_logger.getChild(__name__)
standard_hop_length = 512
standard_framerate = 24
standard_screen_size = (1280, 720)


class ProjectHandler:

    def __init__(self, filename, directory):

        self.name = filename.split(os.sep)[-1].split('.')[0]

        self.home_directory = directory
        self.indir = f'{self.home_directory}/input'
        self.outdir = f'{self.home_directory}/output'
        self.storage_dir = f'{self.home_directory}/storage'
        
        self.sound_dir = f'{self.indir}/sounds'
        self.picure_dir = f'{self.indir}/pictures'

        self.directories = [self.home_directory,
                            self.indir, self.outdir, self.storage_dir,
                            self.sound_dir, self.picure_dir]

        # setting up directory structure
        for directory in self.directories:
            if not os.path.exists(directory):
                logger.debug(f'making directory {directory}')
                os.mkdir(directory)

        self.pictures = dict()
        self.sound_files = dict()
        self.videos = dict()

        self._main_soundfile = None

        self.analyzer_results = None

        self.length = None

        self.save_me()

    @property
    def filename(self):
        return f'{self.home_directory}/{self.name}.pkl'

    def save_me(self):
        filename = self.filename
        logger.debug(f'saving ProjectHandler {self.name} to {filename}')
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def get_project_handler(name=None, filename=None, **kwargs):

        if isinstance(name, type(None)) and isinstance(filename, type(None)):
            raise ValueError('Either name or filename must be given!')

        if name and filename:
            raise ValueError('name and filename were given! Can only take one of them!')

        if name:
            mv_scratch = os.environ[mv_scratch_key]
            filename = f'{mv_scratch}/{name}/{name}.pkl'

        logger.debug(f'getting ProjectHandler {filename}')

        return ProjectHandler._load_project_handler_pkl(filename)

    @staticmethod
    def _load_project_handler_pkl(filename):
        with open(filename, 'rb') as f:
            ph = pickle.load(f)
        return ph

    # ===========================================  Sound  =========================================== #

    @property
    def main_sound_file(self):
        return self.sound_files.get('main')

    @main_sound_file.setter
    def main_sound_file(self, value):
        self.add_sound('main', value)

    def add_sound(self, name, filename):

        length = Sound(filename, hop_length=standard_hop_length).get_length()
        if self.length and not (length == self.length):
            raise SoundError(f'Length of {filename} is {length}s but should be {self.length}s!')

        self.length = length
        new_filename = f'{self.sound_dir}/{filename.split(os.path.sep)[-1]}'

        if not filename.startswith(os.path.abspath(self.indir) + os.path.sep):
            logger.debug(f'copying {filename} to {new_filename}')
            shutil.copy2(filename, new_filename)

        self.sound_files[name] = new_filename
        self.save_me()

    def get_sound(self, name, hop_length, framerate):
        return Sound(self.sound_files[name], hop_length=hop_length, sample_rate=framerate * hop_length)

    def sound_dictionary(self, framerate, hoplength):
        d = {
            name: self.get_sound(name, hoplength, framerate)
            for name in self.sound_files.keys()
        }
        return d

    # ==========================================  Pictures  ========================================== #

    def add_picture(self, filename):
        new_filename = f'{self.picure_dir}/{filename.split(os.sep)[-1]}'

        if not filename.startswith(os.path.abspath(self.indir) + os.path.sep):
            logger.debug(f'copying {filename} to {new_filename}')
            shutil.copy2(filename, new_filename)

        self.pictures[new_filename.split(os.sep)[-1].split('.')[0]] = new_filename

    def get_picture(self, name, screen_size, framerate, hoplength):
        logger.debug(f'getting picture with name {name}')
        picture_class, picture_params_list, ind = self.pictures[name]

        param_info = dict()
        for t in picture_params_list:
            attr, value = t.split(': ')
            param_info[attr] = value

        sound_dict = self.sound_dictionary(framerate, hoplength)
        return BasePicture.create(picture_class, sound_dict, param_info, screen_size), ind

    def get_pictures_list(self, screen_size, framerate, hoplength):
        l = np.empty(len(self.pictures.keys()), dtype=object)
        for n in self.pictures.keys():
            picture, ind = self.get_picture(n, screen_size, framerate, hoplength)
            logger.debug(f'adding picture of class {type(picture)} at indice {ind}')
            l[ind] = picture

        isnone = [isinstance(p, type(None)) for p in l]
        if np.any(isnone):
            ind = np.where(isnone)[0]
            raise PictureError(f'Indice {ind} does not contain any Picture!')

        return l

    # ==========================================  Video  ========================================== #

    def get_video(self, screen_size, hop_length, framerate):
        pictures = self.get_pictures_list(screen_size, framerate, hop_length)
        duration = self.get_sound('main', hop_length, framerate).get_length()
        self.length = duration
        video = Video(pictures, self.main_sound_file, framerate, duration, screen_size)
        return video

    def analyse(self, screen_size=standard_screen_size, hop_length=standard_hop_length, framerate=standard_framerate):
        video = self.get_video(screen_size, hop_length, framerate)
        low_res_video_frames = list()
        for i in tqdm(range(round(framerate * self.length)), desc='making low res frames'):
            low_res_video_frames.append(video.make_frame_per_frame(i))

        self.analyzer_results = low_res_video_frames, framerate
        self.save_me()

        return low_res_video_frames, framerate

    def make_video(self, hop_length=standard_hop_length, framerate=standard_framerate, codec='mp4',
                   screen_size=standard_screen_size):

        video = self.get_video(screen_size, hop_length, framerate)
        filename = f"{self.outdir}/{self.name}"

        if hop_length != standard_hop_length:
            filename += f'_hop{hop_length}'

        if framerate != standard_framerate:
            filename += f'_framerate{framerate}'
            
        filename += '.' + codec
        video.make_video(filename=filename)
        return filename

    @staticmethod
    def multiprocess_wrapping(fn, res):
        ph = ProjectHandler.get_project_handler(filename=fn)
        res['video_filename'] = ph.make_video()
