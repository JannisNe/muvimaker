import os, shutil, pickle, json
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

    def __init__(self, name, directory):

        self.name = name

        self.home_directory = directory

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

    @property
    def indir(self):
        return f'{self.home_directory}/input'

    @property
    def outdir(self):
        return f'{self.home_directory}/output'

    @property
    def storage_dir(self):
        return f'{self.home_directory}/storage'

    @property
    def sound_dir(self):
        return f'{self.indir}/sounds'

    @property
    def picture_dir(self):
        return f'{self.indir}/pictures'

    @property
    def pictures_file(self):
        return f"{self.picture_dir}/pictures_dict.json"

    @property
    def sounds_file(self):
        return f"{self.sound_dir}/sound_dict.json"

    @property
    def analyser_results_file(self):
        return f"{self.storage_dir}/analyser_results.pkl"

    @property
    def directories(self):
        return [self.home_directory,
                self.indir, self.outdir, self.storage_dir,
                self.sound_dir, self.picture_dir]

    def save_me(self):
        for ff, attr in zip([self.pictures_file, self.sounds_file, self.analyser_results_file],
                            ['pictures', 'sound_files', 'analyzer_results']):

            if 'analyzer' in attr:
                saver = pickle
                mod = "wb"
                kw = dict()
            else:
                saver = json
                mod = "w"
                kw = {'indent': 4, 'sort_keys': True}

            try:
                logger.debug(f"saving {attr}, to {ff}")
                with open(ff, mod) as f:
                    saver.dump(self.__getattribute__(attr), f, **kw)
            except OSError as e:
                logger.warning(f"Could not save {attr} to {ff}: {e}")

    def load_me(self):

        for ff, attr in zip([self.pictures_file, self.sounds_file, self.analyser_results_file],
                            ['pictures', 'sound_files', 'analyzer_results']):

            if 'analyzer' in attr:
                loader = pickle
                mod = "rb"
            else:
                loader = json
                mod = "r"

            try:
                logger.debug(f"loading {attr} from {ff}")
                with open(ff, mod) as f:
                    self.__setattr__(attr, loader.load(f))
            except OSError as e:
                logger.warning(f"Could not load {attr} from {ff}: {e}")

    @staticmethod
    def get_project_handler(name=None, directory=None, **kwargs):
        mv_scratch = os.environ[mv_scratch_key]

        if not name and directory:
            name = directory.split(os.sep)[-1]
        elif name and not directory:
            directory = f"{mv_scratch}/{name}"

        logger.debug(f'loading project handler {name} from {directory}')
        ph = ProjectHandler(name, directory)
        ph.load_me()
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

    def get_picture(self, name, screen_size, framerate, hoplength):
        logger.debug(f'getting picture with name {name}')
        picture_class, picture_params_list, ind = self.pictures[name]

        param_info = dict()
        for t in picture_params_list:
            attr, value = t.split(': ')
            param_info[attr] = value

        sound_dict = self.sound_dictionary(framerate, hoplength)
        return BasePicture.create(picture_class, sound_dict, param_info, screen_size), int(ind)

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
