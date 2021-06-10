import os
import tkinter as tk
from tkinter import filedialog as fd
from muvimaker import main_logger


logger = main_logger.getChild(__name__)


class SoundDialogue(tk.Toplevel):
    """dialogue to add sound file and give it a name"""

    def __init__(self, parent, def_msg='Select sound file', button_text='Add',
                 soundfile_insert='enter path', name_insert='enter name',
                 topmost=True, listbox_indice=tk.END):
        tk.Toplevel.__init__(self, parent)

        self.parent = parent
        self.msg = tk.StringVar()
        self.msg.set(def_msg)
        self.button_text = button_text
        self.soundfile_insert = soundfile_insert
        self.name_insert = name_insert
        self.listbox_indice = listbox_indice

        self.soundfile_entry = None
        self.name_entry =None

        self._setup_widgets()
        # self._setup_xtra_widgets()
        self.attributes('-topmost', topmost)
        self.mainloop()

    def _setup_widgets(self):
        msg_label = tk.Label(self, textvariable=self.msg)
        msg_label.pack(fill='both', expand=True)

        soundfile_entry = tk.Entry(self, borderwidth=5)
        soundfile_entry.insert(0, self.soundfile_insert)
        soundfile_entry.pack(fill='both', expand=True)
        self.soundfile_entry = soundfile_entry
        self.soundfile_entry.bind('<1>', self._browse)

        name_entry = tk.Entry(self, borderwidth=5)
        name_entry.insert(0, self.name_insert)
        name_entry.pack(fill='both', expand=True)
        self.name_entry = name_entry

        button = tk.Button(self, text=self.button_text, command=self.button_action)
        button.pack(fill='both', expand=True)

    def _browse(self, event):
        filename = fd.askopenfilename()
        self.soundfile_entry.delete(0, 'end')
        self.soundfile_entry.insert(0, filename)

    def button_action(self):
        soundfile = self.soundfile_entry.get()
        name = self.name_entry.get()

        if os.path.isfile(soundfile):
            logger.debug(f'adding {soundfile}')
            self.parent.info = name, soundfile
            self.destroy()

        else:
            self.msg.set(f'{soundfile} is not a file!')



# class AddSoundDialogue(OpenFileDialogue):
#
#     def __init__(self, parent):
#
#         assert isinstance(parent, tk.Listbox)
#
#         OpenFileDialogue.__init__(self,
#                                   parent,
#                                   title='Add Sound File',
#                                   def_msg='Select sound file',
#                                   button_text='Add',
#                                   insert='enter path')
#
#     def button_action(self):
#         entry = self.entry.get()
#         if os.path.isfile(entry):
#             logger.debug(f'adding {entry}')
#
#             self.destroy()
#
#         else:
#             self.msg.set(f'{entry} is not a file!')