import os
import shutil
import pickle
from muvi_maker import main_logger, mv_scratch_key
from muvi_maker.core.sound import Sound
from muvi_maker.core.picture import Picture
from muvi_maker.core.video import Video


logger = main_logger.getChild(__name__)
standard_hop_length = 512
standard_framerate = 24


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

        self.sound_filename = None
        self.pictures = {}
        self.videos = {}

        self.length = None
        # self.add_sound(filename)

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

    def add_sound(self, filename):

        new_filename = f'{self.sound_dir}/{filename.split(os.path.sep)[-1]}'

        if filename != self.sound_filename:

            if not self.sound_filename:
                self.sound_filename = new_filename
            else:
                raise FileExistsError('Already have a sound file!')

            if not filename.startswith(os.path.abspath(self.indir) + os.path.sep):
                logger.debug(f'copying {filename} to {new_filename}')
                shutil.copy2(filename, new_filename)

        self.length = Sound(self.sound_filename, hop_length=standard_hop_length).get_length()
        self.save_me()

    def get_sound(self, hop_length=standard_hop_length, framerate=standard_framerate):
        return Sound(self.sound_filename, hop_length=hop_length, sample_rate=framerate * hop_length)

    # ==========================================  Pictures  ========================================== #

    def add_picture(self, filename):
        new_filename = f'{self.picure_dir}/{filename.split(os.sep)[-1]}'

        if not filename.startswith(os.path.abspath(self.indir) + os.path.sep):
            logger.debug(f'copying {filename} to {new_filename}')
            shutil.copy2(filename, new_filename)

        self.pictures[new_filename.split(os.sep)[-1].split('.')[0]] = new_filename

    def get_picture(self, name):
        return Picture(self.pictures[name])

    # ==========================================  Video  ========================================== #

    def analyse(self, hop_length=standard_hop_length, framerate=standard_framerate, test_ind=None, codec='mp4'):
        """
        TODO:
            make_colorbar()
            make_spectrogramm()
            make_low_res_video()
        """

        video = Video(self.get_sound(hop_length, framerate), framerate=framerate, duration=self.length)

        # raise NotImplementedError

        # filename = f"{self.outdir}/{self.name}_params.{codec}"
        # video = Video(self.get_sound(hop_length, framerate), framerate=framerate, duration=self.length)
        # clip = video.make_param_video(storage=self.storage_dir, filename=filename, test_ind=test_ind)
        # return clip
    
    def make_video(self, hop_length=standard_hop_length, framerate=standard_framerate, codec='mp4'):
        video = Video(self.get_sound(hop_length, framerate), framerate=framerate, duration=self.length)
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