from abc import ABC

from moviepy.editor import VideoFileClip
import numpy as np
import face_recognition
import tqdm, json, PIL, os, pickle, copy, math

from muvimaker import main_logger
from .base_picture import BasePicture


logger = main_logger.getChild(__name__)


@BasePicture.register_subclass('face_recognition_picture')
class MetaPictureFaceRecognition(BasePicture):

    needs_face_reco_cache = True

    def __init__(self, sound_dictionary, param_info, screen_size):

        self.pictures_class = param_info['pictures_class']

        if self.pictures_class != 'picture_from_video':
            raise NotImplementedError
        video_file = param_info['video_file']
        video_name = video_file.split(os.sep)[-1].split('.')[0]
        face_reco_file = param_info['face_reco_cache_file']
        face_reco_dir = os.path.dirname(face_reco_file)
        marks = ['left_eye', 'right_eye']

        # determine if there are cached results and if finding faces is necessary
        _prev_cache = None
        if not os.path.isfile(face_reco_file):
            _find_faces = True
        else:
            with open(face_reco_file, "rb") as f:
                logger.debug(f"loading {face_reco_file}")
                _prev_cache = pickle.load(f)

            if video_file not in _prev_cache:
                _find_faces = True
            else:
                _find_faces = False

        # ----------------------------------------------------------------------------------------------- #
        #               START find Faces                                                                  #
        # ----------------------------------------------------------------------------------------------- #

        if _find_faces:

            logger.debug(f"recognising faces")
            faces = list()
            landmark_total = list()
            video = VideoFileClip(video_file, audio=False)
            _video_size = np.array(PIL.Image.fromarray(video.get_frame(0)).size)
            _N_frames = int(math.ceil(video.fps * video.duration))
            _empty = [(np.nan, np.nan)] * _N_frames

            for iframe, frame in tqdm.tqdm(enumerate(video.iter_frames()), total=_N_frames):

                locations = face_recognition.face_locations(frame)
                encodings = face_recognition.face_encodings(frame, known_face_locations=locations)
                landmarks = face_recognition.face_landmarks(frame, face_locations=locations)

                for location, encoding, landmark in zip(locations, encodings, landmarks):
                    comparisons = face_recognition.compare_faces(faces, encoding)

                    if np.any(comparisons):
                        ind = np.where(comparisons)[0][0]
                    else:
                        logger.debug('new face!')
                        ind = len(faces)
                        faces.append(encoding)

                        top, right, bottom, left = location
                        face_fn = os.path.join(face_reco_dir, f'{video_name}_{ind}.png')
                        logger.debug(f'saving under {face_fn}')
                        PIL.Image.fromarray(frame[top:bottom, left:right]).save(face_fn)

                        default_dict = {k: list(_empty) for k in marks}
                        landmark_total.append(default_dict)

                    for m in marks:
                        try:
                            landmark_total[ind][m][iframe] = np.median(landmark[m], axis=0) / _video_size
                        except IndexError as e:
                            raise IndexError(f"{e}: {ind} {m} {iframe} \n\n{landmark} \n\n{len(landmark_total)}")

        # ----------------------------------------------------------------------------------------------- #
        #               END find Faces                                                                    #
        # ----------------------------------------------------------------------------------------------- #

            # cache results
            if not _prev_cache:
                _prev_cache = dict()
            _prev_cache[video_file] = landmark_total
            logger.debug(f"writing to {face_reco_file}")
            with open(face_reco_file, "wb") as f:
                pickle.dump(_prev_cache, f)

        # load cache results
        logger.debug(f"loading {face_reco_file}")
        landmark_total = _prev_cache[video_file]

        empty_landmark_centers = [np.array((np.nan, np.nan))] * (len(marks) * len(landmark_total))
        centers = [copy.deepcopy(empty_landmark_centers) for _ in range(len(landmark_total[0][marks[0]]))]
        for iface, lm_dict in enumerate(landmark_total):
            for imark, (m, mlist) in enumerate(lm_dict.items()):
                ilandmark = iface * len(marks) + imark
                for iframe, c in enumerate(mlist):
                    if not np.all(np.isnan(c)):
                        centers[iframe][ilandmark] = c

        param_info = dict(param_info)
        param_info['center'] = centers

        radii = [f'radius_{i}_{j}' for i in range(len(landmark_total)) for j in marks]
        param_info['radii'] = radii
        logger.debug(f'radii: {radii}')

        self._picture = BasePicture.create(
            self.pictures_class,
            sound_dictionary,
            param_info,
            screen_size
        )

        super().__init__(sound_dictionary, param_info, screen_size)
        self.cache_bool = False

    def _make_frame_per_frame(self, ind):
        return self._picture._make_frame_per_frame(ind)