import os
from tkinter import filedialog as fd
from muvi_maker.editor.dialogues.base_dialogue import OpenFileDialogue
from muvi_maker import main_logger, get_editor

logger = main_logger.getChild(__name__)


class AddSoundDialogue(OpenFileDialogue):

    def __init__(self, parent):

        OpenFileDialogue.__init__(self,
                                  parent,
                                  title='Add Sound File',
                                  def_msg='Select sound file',
                                  button_text='Add',
                                  insert='enter path')

    def button_action(self):
        entry = self.entry.get()
        if os.path.isfile(entry):
            logger.debug(f'adding {entry}')
            editor = get_editor(self)
            editor.soundfile = entry
            self.destroy()

        else:
            self.msg.set(f'{entry} is not a file!')