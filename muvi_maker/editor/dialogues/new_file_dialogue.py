import tkinter as tk
import os
from muvi_maker.editor.dialogues.base_dialogue import BaseDialogue
from muvi_maker import main_logger, mv_scratch_key, get_editor
from muvi_maker.core.project import ProjectHandler


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
