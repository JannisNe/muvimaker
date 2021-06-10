import tkinter as tk
import numpy as np

from muvimaker import main_logger, get_editor
from muvimaker.editor.dialogues import SoundDialogue


logger = main_logger.getChild(__name__)


class SoundFilesFrame(tk.LabelFrame):

    def __init__(self, parent):
        super(SoundFilesFrame, self).__init__(parent, text='Soundfiles', labelanchor='n')

        self.soundfiles_listbox = None
        self._info_dict = dict()

        self._setup_widgets()
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(1, weight=1)

    def _setup_widgets(self):

        # Listbox that will contain the files and names
        soundfiles_list = tk.Listbox(self)
        soundfiles_list.grid(row=0, column=0, columnspan=2, sticky='nsew')
        soundfiles_list.bind('<Double-Button-1>', self._change_file)
        self.soundfiles_listbox = soundfiles_list

        # button to add files
        add_button = tk.Button(self, text='Add', command=self._add_file)
        add_button.grid(row=1, column=0)

        # add button to delete files
        delete_button = tk.Button(self, text='Delete', command=self._delete_file)
        delete_button.grid(row=1, column=1)

    def update_listbox(self):
        self.soundfiles_listbox.delete(0, tk.END)
        for name in self._info_dict.keys():
            self.soundfiles_listbox.insert(tk.END, name)

    @property
    def info(self):
        return self._info_dict

    @info.setter
    def info(self, value):
        name, soundfile = value
        logger.debug(f'got {value}')

        l = self.soundfiles_listbox.get(0, tk.END)
        if name in l:
            ind = np.where(np.array(l) == name)
        else:
            ind = len(l)
            self.soundfiles_listbox.insert(ind, name)

        self._info_dict[name] = soundfile
        get_editor(self).project_handler.sound_files = self._info_dict

    def _add_file(self):
        SoundDialogue(self)

    def _change_file(self, event):
        indice = self.soundfiles_listbox.curselection()
        name = self.soundfiles_listbox.get(indice)
        soundfile = self._info_dict[name]

        self.soundfiles_listbox.delete(indice)
        SoundDialogue(self,
                      def_msg='Change sound file',
                      button_text='Change',
                      soundfile_insert=soundfile,
                      name_insert=name,
                      topmost=True,
                      listbox_indice=indice)

    def _delete_file(self):
        indice = self.soundfiles_listbox.curselection()
        self.soundfiles_listbox.delete(indice)