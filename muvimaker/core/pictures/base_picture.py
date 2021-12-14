import abc
from muvimaker import main_logger


logger = main_logger.getChild(__name__)


class BasePicture(abc.ABC):

    subclasses = {}
    needs_face_reco_cache = False

    def __init__(self, sound_dictionary, param_info, screen_size):

        self.sound_dict = sound_dictionary
        self.param_info = param_info
        self.screen_size = screen_size

        self._cached_frames = dict()
        self.cache_bool = True

    def get_frame(self, ind):
        if self.cache_bool:
            # store the frames as sparse matrices to save memory
            if ind not in self._cached_frames:
                self._cached_frames[ind] = self._make_frame_per_frame(ind)
            return self._cached_frames[ind]

        else:
            return self._make_frame_per_frame(ind)

    @abc.abstractmethod
    def _make_frame_per_frame(self, ind):
        """
        Return a numpy array that gives (R,G,B) values for every pixel
        :param ind: indice of the frame
        :return: np.array
        """
        pass

    @classmethod
    def register_subclass(cls, name):
        """
        Adds a new subclass of Picture, with class name equal to "name".
        """

        def decorator(subclass):
            BasePicture.subclasses[name] = subclass
            return subclass

        return decorator

    @classmethod
    def create(cls, subclass, sound_dictionary, param_info, screen_size):
        try:
            picture_class = cls.subclasses[subclass]
        except KeyError:
            raise PictureError(f"Unknown picture class {subclass}! Available are: {cls.subclasses.keys()}")

        try:
            picture = picture_class(sound_dictionary, param_info, screen_size)
        except KeyError as e:
            raise PictureError(e)

        return picture


class PictureError(Exception):
    pass