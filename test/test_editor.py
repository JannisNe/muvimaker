import unittest, os
import tkinter as tk

from muvi_maker import main_logger, mv_scratch_key
from muvi_maker.editor import Editor


logger = main_logger.getChild(__name__)


class TestEditor(unittest.TestCase):
    """Tests the setup of the GUI"""

    def test_set_up(self):
        logger.info('testing set up of GUI')
        scratch = os.environ.get(mv_scratch_key, None)

        if (not scratch) or (not os.path.isdir(scratch)):
            home = os.path.expanduser('~')
            logger.debug(f'{scratch} was given as scratch! Setting to {home}')
            os.environ[mv_scratch_key] = home

        root = tk.Tk(className='MuviMaker')
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f'{round(screen_width / 2)}x{round(screen_height / 2)}')
        Editor(root)