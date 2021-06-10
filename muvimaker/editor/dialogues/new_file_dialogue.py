import tkinter as tk
import os
from muvimaker.editor.dialogues.base_dialogue import BaseDialogue
from muvimaker import main_logger, mv_scratch_key, get_editor
from muvimaker.core.project import ProjectHandler


logger = main_logger.getChild(__name__)


class NewFileDialogue(BaseDialogue):

    def __init__(self, parent):

        BaseDialogue.__init__(self,
                              parent,
                              title='New Project',
                              def_msg='Select name',
                              button_text='Create',
                              insert='enter project name')

    def button_action(self):
        try:
            entry = self.entry.get()
            scr = os.environ[mv_scratch_key]
            project_dir = f'{scr}/{entry}'
            logger.info(f'creating {project_dir}')
            os.mkdir(project_dir)
            editor = get_editor(self)
            editor.project_handler = ProjectHandler(entry, project_dir)
            self.destroy()

        except OSError as e:
            self.msg.set(e)
