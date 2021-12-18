from moviepy.editor import VideoFileClip
import PIL, collections
import numpy as np
from skimage import transform

from muvimaker import main_logger
from muvimaker.core.pictures.base_picture import BasePicture, PictureError
from muvimaker.core.pictures.simple_picture import SimplePicture


logger = main_logger.getChild(__name__)


@BasePicture.register_subclass('picture_from_video')
class PictureFromVideo(SimplePicture):

    def __init__(self, sound_dictionary, param_info, screen_size):
        filename = param_info['video_file']

        self.loop = bool(param_info.pop('loop', 'true'))

        # --------------------- Position ----------------------- #
        rel_center = param_info.get('center', '1, 1')

        # If center is given as string, determines the center for all frames
        if isinstance(rel_center, str):
            rel_center = np.array([float(i) for i in rel_center.split(', ')])
            self._static_center = True

        # Center is given as a list-like object for each individual frame
        elif isinstance(rel_center, collections.Sequence):
            rel_center = np.array(rel_center)
            self._static_center = False

        else:
            raise PictureError(f'Type of center is {type(rel_center)} but should be '
                               f'string or sequence!')

        self.center = np.array(screen_size) * rel_center

        self.video = VideoFileClip(filename, audio=False)
        self.fps = self.video.fps
        self._N_frames = int(round(self.video.duration * self.fps))
        super(PictureFromVideo, self).__init__(sound_dictionary, param_info, screen_size)

    def t(self, ind):
        return ind / self.fps

    def _make_frame_per_frame(self, ind):
        frame = self.video.get_frame(self.t(ind % self._N_frames))
        image = PIL.Image.fromarray(frame)
        image = image.resize(self.screen_size.astype(int)*2, PIL.Image.NEAREST)
        return np.array(self.postprocess(image, ind))

    @staticmethod
    def _bubble_warp(a, centers, radius):
        bs = np.array([a - center * 2 for center in centers if not np.all(np.isnan(centers))])

        if len(bs) == 0:
            return a

        ds = np.array([np.sqrt(np.sum(b ** 2, axis=1)) for b in bs])
        r = radius[:, None]
        ds_minus_r = ds - r
        mask = ds_minus_r < 0
        mask_r = np.any(mask, axis=0)

        if not np.any(mask_r):
            return a

        dmask = ds[:, mask_r, None]
        dminusrmask = ds_minus_r[:, mask_r, None]
        bmask = bs[:, mask_r]

        direction = bmask / dmask
        new = dmask / (dmask - dminusrmask) * dminusrmask * direction
        a[mask_r] += np.sum(new, axis=0, where=mask[:,mask_r, None])

        return a.astype(int)

    def postprocess(self, frame, ind):
        frame = super().postprocess(frame, ind)
        centers = self.center if self._static_center else self.center[ind % self._N_frames]
        radii = np.array([self.__getattribute__(r)[ind] for r in self.radii])
        args = {'centers': np.atleast_1d(centers),
                'radius': radii}
        frame = transform.warp(image=np.array(frame), inverse_map=self._bubble_warp, map_args=args)
        frame = (frame * 255).astype(np.uint8)
        return frame