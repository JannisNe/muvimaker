import tkinter as tk
import tkinter.font as font
import tkinter.ttk as ttk
import _tkinter
import time
import os
import numpy as np
import threading
import queue
from multiprocessing import Process, Manager

from muvimaker import main_logger, mv_scratch_key, main_queue
from muvimaker.editor.dialogues import ScratchDirDialogue
from muvimaker.editor.menubar import Menubar
from muvimaker.editor.frames import InfoFrame, LoggingFrame, ParametersFrame, AnalyzerFrame
from muvimaker.core.pictures import PictureError


logger = main_logger.getChild(__name__)


class Editor(tk.Frame):
    def __init__(self, parent):
        logger.debug('setting up editor')
        self.screen_width = parent.winfo_screenwidth()
        self.screen_height = parent.winfo_screenheight()
        tk.Frame.__init__(self, parent, height=self.screen_height, width=self.screen_width, bg='darkgrey')

        self.name = 'editor'
        self.parent = parent
        self.widgets = dict()
        self.master.title('Editor')

        self.progress_bar_queue = queue.Queue()
        self.analyzer_frame_queue = queue.Queue()

        # self._soundfile = tk.StringVar()
        self._pictures = dict()
        self._soundfiles = dict()
        self._videofile = tk.StringVar()
        self._project_handler = None
        self._ongoing_progress = None
        self._progress_bar_thread = None
        self._analysing_thread = None
        self._make_video_thread = None

        self.active = tk.StringVar()
        self.active.set('disabled')
        self.active.trace('w', lambda *_: self._set_widgets_attribute('state', self.active.get()))

        self._setup_widgets()

        self.parent.columnconfigure(1, weight=1)
        self.parent.columnconfigure(0, weight=10)
        self.parent.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.check_scratch()

    # ------------------    properties   --------------------- #

    @property
    def videofile(self):
        return self._videofile

    @videofile.setter
    def videofile(self, value):
        self._videofile.set(value)

    @property
    def project_handler(self):
        return self._project_handler

    @project_handler.setter
    def project_handler(self, value):
        logger.debug('got ProjectHandler')
        self._project_handler = value
        # self._soundfile.set(str(value.sound_filename))

        self.widgets['info_frame'].sound_files_frame._info_dict = value.sound_files
        self.widgets['info_frame'].sound_files_frame.update_listbox()
        self.widgets['info_frame'].pictures_frame._info_dict = value.pictures
        self.widgets['info_frame'].pictures_frame.update_listbox()

        self.active.set('normal')
        logger.debug("activated")
        if not isinstance(value.analyzer_results, type(None)):
            logger.debug(f'passing saved analyzer results to analyzer frame')
            self.widgets['analyzer_frame'].c_s_lrvf = value.analyzer_results

    # --------------------   Widgets   ------------------------ #

    def add_widget(self, name, widget):
        if name not in self.widgets:
            self.widgets[name] = widget
        else:
            logger.warning(f'{name} already exists! Not adding widget!')

    def _set_widgets_attribute(self, key, state):
        for n, w in self.widgets.items():
            try:
                w[key] = state
            except _tkinter.TclError as e:
                logger.debug(f"{n} does not have option {key}: {e}")

    def _setup_widgets(self):
        menubar = Menubar(self)
        self.add_widget('menu', menubar)
        self.master.config(menu=menubar)

        infoframe = InfoFrame(self)
        self.add_widget('info_frame', infoframe)
        infoframe.grid(row=0, column=0, columnspan=2, sticky='nsew')

        logging_frame = LoggingFrame(self.master)
        self.add_widget('logging_frame', logging_frame)
        logging_frame.grid(row=4, column=0, columnspan=2, sticky='nsew')

        parameters_frame = ParametersFrame(self.master, width=10)
        self.add_widget('parameters_frame', parameters_frame)
        parameters_frame.grid(row=1, column=1, sticky='nsew')

        analyzer_frame = AnalyzerFrame(self)
        self.add_widget('analyzer_frame', analyzer_frame)
        analyzer_frame.grid(row=1, column=0, columnspan=1, rowspan=3, sticky='nsew')

        progress_bar = ttk.Progressbar(self.master, orient='horizontal', mode='indeterminate', length=100)
        progress_bar.grid(row=5, column=0, columnspan=2, sticky='nsew')
        self.add_widget('progress_bar', progress_bar)

        analyse_button = tk.Button(self.master, text='analyse',
                                   height=5, width=10,
                                   state=self.active.get(),
                                   command=self.analyse)
        analyse_button.grid(row=2, column=1)#, sticky='nsew')
        self.add_widget('analyse_button', analyse_button)

        make_video_button = tk.Button(self.master, text='make video',
                                      height=5, width=10,
                                      state=self.active.get(),
                                      command=self.make_video)
        make_video_button['font'] = font.Font(weight='bold')
        make_video_button.grid(row=3, column=1)#, sticky='nsew')
        self.add_widget('make_video_button', make_video_button)

    # ----------------------------------   Functions  ---------------------------------------------- #

    def _start_progress_bar(self):
        self.active.set('disabled')
        self._ongoing_progress = True
        self._progress_bar_thread = threading.Thread(target=self._running_progress_bar)
        self._progress_bar_thread.start()

    def _running_progress_bar(self):
        logger.debug('running progress bar')
        progress_bar = self.widgets['progress_bar']
        progress_bar['value'] = 0
        sgn = 1
        while True:
            try:
                cont = self.progress_bar_queue.get(block=False)
                if not cont:
                    logger.debug('stopping progress bar')
                    break
            except queue.Empty:
                pass

            progress_bar['value'] += 1 * sgn
            if progress_bar['value'] >= 100:
                sgn *= -1
            time.sleep(1 / 10)

    def _stop_progress_bar(self):
        self.active.set('normal')
        self.progress_bar_queue.put(False)
        logger.debug('Put False into queue, waiting for termination')
        self._progress_bar_thread.join()
        self.widgets['progress_bar']['value'] = 0

        # ---------------------------------    ProjectHandler calls    --------------------------------- #

    def make_video(self):
        self.active.set('disabled')
        # threading.Thread(target=self._start_progress_bar).start()
        if not self.project_handler.main_sound_file:
            logger.error(f'No main sound file!')

        else:
            self._start_progress_bar()
            self._make_video_thread = threading.Thread(target=self._make_video)
            self._make_video_thread.start()

    def _make_video(self):
        logger.debug('making video')
        screen_size = np.array(self.widgets['parameters_frame'].size, dtype=float)
        fps = self.widgets['parameters_frame'].fps

        try:
            self.videofile = self.project_handler.make_video(framerate=fps, screen_size=screen_size)
        except PictureError as e:
            logger.error(e)
        finally:
            self._stop_progress_bar()

    def analyse(self):
        self._start_progress_bar()
        self._analysing_thread = threading.Thread(target=self._analyse)
        self._analysing_thread.start()

    def _analyse(self):
        logger.debug('analysing')
        screen_size = np.array(self.widgets['parameters_frame'].size, dtype=float)
        f = 200 / screen_size[0]
        screen_size *= f
        fps = self.widgets['parameters_frame'].fps

        try:
            low_res_video_frames, fps = self.project_handler.analyse(
                screen_size,
                framerate=fps)
            logger.debug('passing results to analyzer frame')
            self.analyzer_frame_queue.put({'c_s_lrvf': (low_res_video_frames, fps)})
            self.widgets['analyzer_frame'].collect()
        except PictureError as e:
            logger.error(e)
        finally:
            self._stop_progress_bar()

    def check_scratch(self):
        scr = os.environ.get(mv_scratch_key, "None")
        if not os.path.isdir(scr):
            logger.debug(f'{scr} is not a directory!')
            ScratchDirDialogue(self)
