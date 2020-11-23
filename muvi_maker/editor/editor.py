import tkinter as tk
import tkinter.font as font
import _tkinter
import os
from multiprocessing import Process, Manager

from muvi_maker import main_logger, mv_scratch_key, main_queue
from muvi_maker.editor.dialogues import ScratchDirDialogue
from muvi_maker.editor.menubar import Menubar
from muvi_maker.editor.info_frame import InfoFrame
from muvi_maker.editor.logging_frame import LoggingFrame
from muvi_maker.editor.parameters_frame import ParametersFrame
from muvi_maker.core.project import ProjectHandler


logger = main_logger.getChild(__name__)


class Editor(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        logger.debug('setting up editor')
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.name = 'editor'
        self.parent = parent
        self.widgets = dict()
        self.master.title('Editor')

        self._soundfile = tk.StringVar()
        self._videofile = tk.StringVar()
        self._project_handler = None

        self.active = tk.StringVar()
        self.active.set('disabled')
        self.active.trace('w', lambda *_: self._set_widgets_attribute('state', self.active.get()))

        self._setup_widgets()
        self.check_scratch()

    # ------------------    properties   --------------------- #

    @property
    def soundfile(self):
        return self._soundfile

    @soundfile.setter
    def soundfile(self, value):
        self._soundfile.set(value)
        self.project_handler.add_sound(value)
        self.active.set('normal')

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
        self._soundfile.set(str(value.sound_filename))
        if value.sound_filename:
            self.active.set('normal')

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
        infoframe.grid(row=0, column=0)

        logging_frame = LoggingFrame(self.master)
        self.add_widget('logging_frame', logging_frame)
        logging_frame.grid(row=10, column=0)

        parameters_frame = ParametersFrame(self.master)
        self.add_widget('parameters_frame', parameters_frame)
        parameters_frame.grid(row=1, column=0)

        analyse_button = tk.Button(self.master, text='analyse', height=5, width=10, state=self.active.get(),
                                   command=self.analyse)
        analyse_button.grid(row=9, column=10)
        self.add_widget('analyse_button', analyse_button)

        make_video_button = tk.Button(self.master, text='make video', height=5, width=10, state=self.active.get(),
                                      command=self.make_video)
        make_video_button_font = font.Font(weight='bold')
        make_video_button['font'] = make_video_button_font
        make_video_button.grid(row=10, column=10)
        self.add_widget('make_video_button', make_video_button)

    # ---------------------------------    ProjectHandler calls    --------------------------------- #

    def make_video(self):
        if not self.project_handler.sound_filename:
            logger.error(f'No sound file!')

        else:
            vn = self.project_handler.make_video()
            self.videofile = vn

    def analyse(self):
        if not self.project_handler.sound_filename:
            logger.error(f'No sound file!')

        else:
            self.project_handler.analyse(framerate=self.widgets['parameters_frame'].fps)

    # def make_video_multiprocess(self):
    #     if not self.project_handler.sound_filename:
    #         logger.error(f'No sound file!')
    #
    #     else:
    #         with Manager() as manager:
    #
    #             p1 = Process(target=LoggingWindow.multiprocess_wrapping)
    #             p1.start()
    #
    #             logger.debug('started logging window')
    #
    #             res = manager.dict()
    #             self.project_handler.save_me()
    #             fn = self.project_handler.filename
    #             p2 = Process(target=ProjectHandler.multiprocess_wrapping,
    #                          args=(fn, res, main_queue, logger.getEffectiveLevel()))
    #             p2.start()
    #
    #             # p1.join()
    #             p2.join()
    #             # video_filename = self.project_handler.make_video()
    #             # self.videofile = video_filename
    #
    #             self.videofile = res['video_filename']

    def check_scratch(self):
        scr = os.environ.get(mv_scratch_key, "None")
        if not os.path.isdir(scr):
            logger.debug(f'{scr} is not a directory!')
            ScratchDirDialogue(self)
