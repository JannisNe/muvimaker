import tkinter as tk
import os
import pickle
from muvimaker.editor.dialogues.base_dialogue import OpenDirectoryDialoge
from muvimaker import main_logger, mv_scratch_key, get_editor
from muvimaker.core.project import ProjectHandler


logger = main_logger.getChild(__name__)


class OpenProjectDialogue(OpenDirectoryDialoge):

    def __init__(self, parent):

        super().__init__(parent,
                         title='Open Project',
                         def_msg='select project',
                         button_text='Open',
                         insert='enter project folder path')

    def _setup_xtra_widgets(self):
        frame = tk.LabelFrame(self, text='Projects in working directory', labelanchor='n')
        frame.pack(fill='both', expand=True)

        scr = os.environ[mv_scratch_key]
        directories_in_scr = os.listdir(scr)

        def ba(d):
            self.entry.delete(0, 'end')
            self.entry.insert(0, f'{scr}/{d}')

        for d in directories_in_scr:
            if '.' in d:
                continue
            button = tk.Button(frame, text=d, command=lambda s=d: ba(s))
            button.pack(fill='both', expand=True)

    def button_action(self):
        entry = self.entry.get()
        if os.path.isdir(entry):
            logger.info(f'opening {entry}.')
            editor = get_editor(self)
            editor.project_handler = ProjectHandler.get_project_handler(directory=entry)
            self.destroy()
        else:
            self.msg.set(f'{entry} is not a file!')