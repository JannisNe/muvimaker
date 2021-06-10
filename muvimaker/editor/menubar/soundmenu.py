import tkinter as tk
from muvimaker import main_logger, mv_scratch_key

logger = main_logger.getChild(__name__)


class Soundmenu(tk.Menu):

    def __init__(self, menubar):
        logger.debug('setting up soundmenu')
        tk.Menu.__init__(self, menubar)
        self._setup_commands()
        self.commands = dict()

    def _setup_commands(self):
        logger.debug('setting up commands')
        self.add_command(label='Add Sound', command=self._add_sound)

    def _add_sound(self):
        AddSoundDialogue(self)

    # def get_project_handler(self):
    #     return self.master.get_project_handler()