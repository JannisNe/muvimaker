import tkinter as tk
from muvimaker import main_logger
from .sound_files_frame import SoundFilesFrame
from .picture_frame import PicturesFrame


logger = main_logger.getChild(__name__)


class InfoFrame(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent.master)
        self.parent = parent
        self.master = parent
        self.sound_files_frame = None
        self.pictures_frame = None
        self._setup_widgets()
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)

    def _setup_widgets(self):
        sound_files_frame = SoundFilesFrame(self)
        sound_files_frame.grid(row=0, column=0, sticky='nsew')
        self.sound_files_frame = sound_files_frame

        pictures_frame = PicturesFrame(self)
        pictures_frame.grid(row=0, column=1, sticky='nsew')
        self.pictures_frame = pictures_frame

        # audio_file_label = tk.Label(self, text='Sound File: ')
        # audio_file_label.grid(row=0, column=0)
        # audio_filename_label = tk.Label(self, textvariable=self.parent.soundfile)
        # audio_filename_label.grid(row=0, column=1)
        #
        # video_file_label = tk.Label(self, text='Video Output File: ')
        # video_file_label.grid(row=1, column=0)
        # video_filename_label = tk.Label(self, textvariable=self.parent.videofile)
        # video_filename_label.grid(row=1, column=1)