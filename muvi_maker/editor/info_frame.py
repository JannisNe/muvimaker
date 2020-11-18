import tkinter as tk
from muvi_maker import main_logger


logger = main_logger.getChild(__name__)


class InfoFrame(tk.LabelFrame):

    def __init__(self, parent):
        tk.LabelFrame.__init__(self, parent.master, text='Info', labelanchor='n')

        self.parent = parent
        # self.audio_filename = tk.StringVar()
        # if self.parent.project_handler:
        #     self.audio_filename.set(str(self.parent.project_handler.sound_filename))
        #
        # self.video_output_filename = tk.StringVar()

        self._setup_widgets()

    def _setup_widgets(self):
        audio_file_label = tk.Label(self, text='Sound File: ')
        audio_file_label.grid(row=0, column=0)
        audio_filename_label = tk.Label(self, textvariable=self.parent.soundfile)
        audio_filename_label.grid(row=0, column=1)

        video_file_label = tk.Label(self, text='Video Output File: ')
        video_file_label.grid(row=1, column=0)
        video_filename_label = tk.Label(self, textvariable=self.parent.videofile)
        video_filename_label.grid(row=1, column=1)