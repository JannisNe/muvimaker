import tkinter as tk
import argparse

from muvi_maker.editor import Editor
from muvi_maker import main_logger


logger = main_logger.getChild(__name__)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--log_level', '-l', type=str, default='DEBUG', const='DEBUG', nargs='?')
    args = parser.parse_args()
    main_logger.setLevel(args.log_level)

    root = tk.Tk(className='MuviMaker')
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f'{round(screen_width/2)}x{round(screen_height/2)}')
    app = Editor(root)
    root.mainloop()