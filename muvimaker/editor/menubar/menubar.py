import tkinter as tk
from muvimaker import main_logger

from muvimaker.editor.menubar.filemenu import Filemenu
# from muvimaker.editor.menubar.soundmenu import Soundmenu


logger = main_logger.getChild(__name__)


class Menubar(tk.Menu):

    def __init__(self, parent):
        logger.debug('setting up menubar')
        tk.Menu.__init__(self, parent)
        self._setup_cascades()

    def _setup_cascades(self):
        self.add_cascade(label='File', menu=Filemenu(self))
        # self.add_cascade(label='Audio', menu=Soundmenu(self))