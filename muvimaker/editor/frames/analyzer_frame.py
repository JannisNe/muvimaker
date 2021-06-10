import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
import time
import threading
from muvimaker import main_logger
from muvimaker.images import baby_file


logger = main_logger.getChild(__name__)


class AnalyzerFrame(tk.LabelFrame):

    def __init__(self, parent):
        logger.debug('creating AnalyzerFrame')
        tk.LabelFrame.__init__(self, parent.master, text='File Info', labelanchor='n')
        self.parent = parent

        self._low_res_video_images = [np.asarray(Image.open(baby_file))]
        self._fps = None
        self._pic_size = (1000, 1000)
        self._img = None
        self._entries = dict()
        self._frame_ind = None
        self._stop = False
        self._queue = parent.analyzer_frame_queue
        self._playing_thread = None

        self.scale = None
        self.preview_label = None

        self._setup_widgets()
        self['state'] = 'disabled'
        self._entries['preview_label']['state'] = 'normal'
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0,1,2,3), weight=1)
        
    def __setitem__(self, key, value):
        if key == 'state':
            for w, entry in self._entries.items():
                if w != 'preview_label':
                    entry['state'] = value
        else:
            raise KeyError(f"\'AnalyzerFrame\' object has no key \'{key}\'")

    @property
    def pic_size(self):
        return self._pic_size

    @property
    def c_s_lrvf(self):
        return self._low_res_video_images, self._fps

    @c_s_lrvf.setter
    def c_s_lrvf(self, tup):
        logger.debug('analyzer frame got results')
        self._low_res_video_images, self._fps = tup
        self.scale.configure(to=len(self._low_res_video_images)-1)
        self.frame_ind = 0

    @property
    def frame_ind(self):
        return self._frame_ind

    @frame_ind.setter
    def frame_ind(self, value):
        self._frame_ind = value
        self._update_preview_label(value)
        # self._update_spectrogram_label(value)

    def _setup_widgets(self):

        # slider to select which frame to display
        self.scale = tk.Scale(self, from_=0, to=1, orient="horizontal",
                              command=self._change_frame)
        self.scale.grid(row=3, column=0, sticky='nsew', columnspan=2)
        self._entries['scale'] = self.scale

        # setting up the label that displays the frame from the low res preview
        logger.debug(f'Ind is {self.scale.get()}')
        preview_label = tk.Label(self, image=self._img)
        preview_label.grid(row=0, column=0, columnspan=2, sticky='nsew')
        self._entries['preview_label'] = preview_label
        self.preview_label = preview_label

        # setting up play button
        play_button = tk.Button(self, text='PLAY', fg='green', command=self.play)
        play_button.grid(row=4, column=0)

        # setting up stop button
        stop_button = tk.Button(self, text='STOP', fg='red', command=self.stop)
        stop_button.grid(row=4, column=1)

    def _get_pil_image_from_array(self, frame_ind, array):
        img_array = array[frame_ind]
        pil_img = Image.fromarray(img_array)
        pil_img.resize(self._pic_size)
        img = ImageTk.PhotoImage(image=pil_img)
        return img

    def _get_image(self, frame_ind):
        if not isinstance(self._low_res_video_images, type(None)):
            return self._get_pil_image_from_array(frame_ind, self._low_res_video_images)
        else:
            logger.warning('No video images analysed!')

    def _update_preview_label(self, frame_ind):
        self._img = self._get_image(frame_ind)
        self.preview_label.configure(image=self._img)

    def _change_frame(self, frame_ind_str):
        self.frame_ind = int(frame_ind_str)

    def play(self):
        self._playing_thread = threading.Thread(target=self._play_thread)
        self._playing_thread.start()

    def _play_thread(self):
        self._stop = False
        logger.debug('play')
        while True:

            logger.debug(f'frame ind is {self._frame_ind}')
            self.scale.set(self._frame_ind + 1)
            self.frame_ind = self._frame_ind + 1
            time.sleep(1 / self._fps)

            if self._frame_ind >= len(self._low_res_video_images) - 1:
                self._stop = True

            if self._stop:
                break

    def stop(self):
        logger.debug('stop')
        self._stop = True
        self._playing_thread.join()
        logger.debug(f"play thread is alive: {self._playing_thread.is_alive()}")

    def collect(self):
        it = self._queue.get()
        if 'c_s_lrvf' in it:
            self.c_s_lrvf = it['c_s_lrvf']
        else:
            logger.error(f"'c_s_lrvf' not in queue item! "
                         f"Item {it} is of type {type(it)}")