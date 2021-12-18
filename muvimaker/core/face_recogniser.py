from moviepy.editor import VideoFileClip
import numpy as np
import face_recognition
import tqdm, PIL, os, pickle, math

from muvimaker import main_logger


logger = main_logger.getChild(__name__)


class FaceRecogniser:
    marks = ['left_eye', 'right_eye']

    def __init__(self, cache_dir):
        self.cache_dir = cache_dir
        self.cache_file = os.path.join(self.cache_dir, 'face_reco_cache.pkl')

        if os.path.isfile(self.cache_file):
            logger.debug(f'loading {self.cache_file}')
            with open(self.cache_file, 'rb') as f:
                self.cache = pickle.load(f)
        else:
            self.cache = dict()
            logger.debug(f'creating empty cache at {self.cache_file}')

            d = os.path.dirname(self.cache_file)
            if not os.path.isdir(d):
                os.mkdir(d)

            with open(self.cache_file, 'wb') as f:
                pickle.dump(self.cache, f)

    def recognise_faces(self, video_file, video_nickname):
        # ----------------------------------------------------------------------------------------------- #
        #               START find Faces                                                                  #
        # ----------------------------------------------------------------------------------------------- #

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
                    face_fn = os.path.join(self.cache_dir, f'{video_nickname}_face{ind}.png')
                    logger.debug(f'saving under {face_fn}')
                    PIL.Image.fromarray(frame[top:bottom, left:right]).save(face_fn)

                    default_dict = {k: list(_empty) for k in self.marks}
                    landmark_total.append(default_dict)

                for m in self.marks:
                    try:
                        landmark_total[ind][m][iframe] = np.median(landmark[m], axis=0) / _video_size
                    except IndexError as e:
                        raise IndexError(f"{e}: {ind} {m} {iframe} \n\n{landmark} \n\n{len(landmark_total)}")

        # ----------------------------------------------------------------------------------------------- #
        #               END find Faces                                                                    #
        # ----------------------------------------------------------------------------------------------- #

        self.cache[video_nickname] = landmark_total
        logger.debug(f'saving under {self.cache_file}')
        with open(self.cache_file, 'wb') as f:
            pickle.dump(self.cache, f)
