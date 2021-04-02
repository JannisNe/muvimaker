import abc
from muvi_maker import main_logger


logger = main_logger.getChild(__name__)


class BasePicture(abc.ABC):

    subclasses = {}

    def __init__(self, sound_dictionary, param_info, screen_size):

        self.sound_dict = sound_dictionary
        self.param_info = param_info
        self.screen_size = screen_size

    @abc.abstractmethod
    def make_frame_per_frame(self, ind):
        pass

    @classmethod
    def register_subclass(cls, name):
        """Adds a new subclass of EnergyPDF, with class name equal to
        "energy_pdf_name".
        """

        def decorator(subclass):
            BasePicture.subclasses[name] = subclass
            return subclass

        return decorator

    @classmethod
    def create(cls, subclass, sound_dictionary, param_info, screen_size):
        picture_class = cls.subclasses[subclass]
        return picture_class(sound_dictionary, param_info, screen_size)


class PictureError(Exception):
    pass