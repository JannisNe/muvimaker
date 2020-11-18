import tkinter as tk
from muvi_maker import main_logger

from muvi_maker.editor.filemenu import Filemenu
from muvi_maker.editor.soundmenu import Soundmenu


logger = main_logger.getChild(__name__)


class Menubar(tk.Menu):

    def __init__(self, parent):
        logger.debug('setting up menubar')
        tk.Menu.__init__(self, parent)
        self._setup_cascades()

    def _setup_cascades(self):
        self.add_cascade(label='File', menu=Filemenu(self))
        self.add_cascade(label='Audio', menu=Soundmenu(self))

    # def get_project_handler(self):
    #     return self.master.get_project_handler()

    # def set_project_handler(self, project_handler):
    #     self.master.set_project_handler(project_handler)