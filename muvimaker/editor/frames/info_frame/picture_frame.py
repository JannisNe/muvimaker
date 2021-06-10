import tkinter as tk
import numpy as np

from muvimaker import main_logger, get_editor
from muvimaker.editor.dialogues import AddPictureDialogue


logger = main_logger.getChild(__name__)


class PicturesFrame(tk.LabelFrame):

    def __init__(self, parent):
        super(PicturesFrame, self).__init__(parent, text='Pictures', labelanchor='n')

        self.pictures_listbox = None
        self._info_dict = dict()

        self._setup_widgets()

        self.columnconfigure((0, 1), weight=10)
        self.columnconfigure(2, weight=1)

    def _setup_widgets(self):

        # Listbox that will contain the files and names
        pictures_list = tk.Listbox(self)
        pictures_list.grid(row=0, column=0, rowspan=2, columnspan=2, sticky='nsew')
        pictures_list.bind('<Double-Button-1>', self._change_file)
        self.pictures_listbox = pictures_list

        # button to add files
        add_button = tk.Button(self, text='Add', command=self._add_file)
        add_button.grid(row=2, column=0)#, sticky='nsew')

        # add button to delete files
        delete_button = tk.Button(self, text='Delete', command=self._delete_file)
        delete_button.grid(row=2, column=1)#, sticky='nsew')

        # add buttons to move the items up and down
        up_button = tk.Button(self, text='UP', command=self._move_item_up)
        up_button.grid(row=0, column=2, sticky='nsew')
        down_button = tk.Button(self, text='DOWN', command=self._move_item_down)
        down_button.grid(row=1, column=2, sticky='nsew')

    def update_listbox(self):
        self.pictures_listbox.delete(0, tk.END)
        for name, info in self._info_dict.items():
            logger.debug(f'inserting {name} to {info[-1]}')
            self.pictures_listbox.insert(info[-1], name)

    def _parse_info_to_ph(self):
        logger.debug(f'parsing {self._info_dict} to ProjectHandler')
        get_editor(self).project_handler.pictures = self._info_dict

    @property
    def info(self):
        return self._info_dict

    @info.setter
    def info(self, value):
        name, picture_file, attributes_list, ind = value
        logger.debug(f'got {value}')

        l = self.pictures_listbox.get(0, tk.END)

        if name in l:
            indice = np.where(np.array(l) == name)[0]
        else:
            indice = np.atleast_1d(ind)[0]
            if indice == 'end':
                indice = len(l)
            self.pictures_listbox.insert(ind, name)

        self._info_dict[name] = [picture_file, attributes_list, str(indice)]
        self._parse_info_to_ph()

    def _add_file(self):
        AddPictureDialogue(self)

    def _change_file(self, event):
        indice = self.pictures_listbox.curselection()
        name = self.pictures_listbox.get(indice)
        pic_file, attributes_list, ind = self._info_dict[name]
        logger.debug(f'{pic_file} {attributes_list}, {indice}')

        if not int(indice[0]) == int(ind):
            raise ValueError(f'indice in listbox {indice[0]} is not indice from info {ind}')

        self.pictures_listbox.delete(indice)
        AddPictureDialogue(self,
                           def_list=attributes_list,
                           def_msg='Change sound file',
                           button_text='Change',
                           soundfile_insert=pic_file,
                           name_insert=name,
                           topmost=True,
                           listbox_indice=indice)

    def _delete_file(self):
        indice = self.pictures_listbox.curselection()
        name = self.pictures_listbox.get(indice)
        new_info = {
            k: v for k, v in self._info_dict.items() if k != name
        }
        self._info_dict = new_info
        self.pictures_listbox.delete(indice)
        self._parse_info_to_ph()

    def _move_item_up(self):
        self._move_item(-1)

    def _move_item_down(self):
        self._move_item(1)

    def _move_item(self, step):
        indice = self.pictures_listbox.curselection()[0]

        if indice <= 0:
            return

        new_indice = indice + step
        entry_to_be_moved = self.pictures_listbox.get(indice)
        logger.debug(f'moving {entry_to_be_moved} from {indice} to {new_indice}')
        self.pictures_listbox.delete(indice)
        self.pictures_listbox.insert(new_indice, entry_to_be_moved)

        # adjust all affected indices
        for name, info in self._info_dict.items():
            iind = int(info[-1])

            if indice < new_indice:
                if (iind > indice) and (iind <= new_indice):
                    self._info_dict[name][-1] = str(iind - 1)

            if indice > new_indice:
                if (iind < indice) and (iind >= new_indice):
                    self._info_dict[name][-1] = str(iind + 1)

        self._info_dict[entry_to_be_moved][-1] = str(new_indice)
        self._parse_info_to_ph()