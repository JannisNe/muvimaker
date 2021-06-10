import os
import tkinter as tk
from tkinter import filedialog as fd

from muvimaker import main_logger
from muvimaker.core.pictures.base_picture import BasePicture


logger = main_logger.getChild(__name__)


class AddPictureDialogue(tk.Toplevel):
    """dialogue to add sound file and give it a name"""

    def __init__(self, picture_frame, def_list=None, def_msg='Select picture file', button_text='Add',
                 soundfile_insert='enter picture class', name_insert='enter name',
                 topmost=True, listbox_indice=tk.END):

        super(AddPictureDialogue, self).__init__()

        self.picture_frame = picture_frame
        self.msg = tk.StringVar()
        self.msg.set(def_msg)
        self.button_text = button_text
        self.picture_insert = soundfile_insert
        self.name_insert = name_insert
        self.listbox_indice = listbox_indice

        try:
            _ = len(def_list)
            logger.debug('No default list')
            self.list = def_list
        except TypeError:
            logger.debug('generating empty list')
            self.list = list()

        self.picture_entry = None
        self.name_entry =None
        self.listbox = None

        self._setup_widgets()
        self.attributes('-topmost', topmost)
        self.mainloop()

    def _setup_widgets(self):
        msg_label = tk.Label(self, textvariable=self.msg)
        msg_label.pack(fill='both', expand=True)

        soundfile_entry = tk.Entry(self, borderwidth=5)
        soundfile_entry.insert(0, self.picture_insert)
        soundfile_entry.pack(fill='both', expand=True)
        self.picture_entry = soundfile_entry

        name_entry = tk.Entry(self, borderwidth=5)
        name_entry.insert(0, self.name_insert)
        name_entry.pack(fill='both', expand=True)
        self.name_entry = name_entry

        listbox = tk.Listbox(self)

        for i, l in enumerate(self.list):
            logger.debug(f"adding {l}")
            listbox.insert(i, l)

        listbox.pack(fill='both', expand=True)
        self.listbox = listbox
        self.listbox.bind('<BackSpace>', self._delete_item)

        item_entry = tk.Entry(self, borderwidth=5)
        item_entry.pack(fill='both', expand=True)
        self.item_entry = item_entry

        add_item_button = tk.Button(self, text='add attribute', command=self._add_attribute)
        add_item_button.pack(fill='both', expand=True)

        button = tk.Button(self, text=self.button_text, command=self.button_action)
        button.pack(fill='both', expand=True)

    def _delete_item(self, event):
        indice = self.listbox.curselection()
        self.listbox.delete(indice)

    def _add_attribute(self):
        self.listbox.insert(tk.END, self.item_entry.get())
        self.item_entry.delete(0, tk.END)

    def button_action(self):
        picture_class = self.picture_entry.get()

        if picture_class in BasePicture.subclasses.keys():
            self.picture_frame.info = self.parse_info()
            self.destroy()

        else:
            self.msg.set(f'{picture_class} not recognised! Available: {BasePicture.subclasses.keys()}')

    def parse_info(self):
        return self.name_entry.get(), self.picture_entry.get(), self.listbox.get(0, tk.END), self.listbox_indice
