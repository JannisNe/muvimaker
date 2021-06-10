import tkinter as tk
from muvimaker import main_logger


logger = main_logger.getChild(__name__)


class ParametersFrame(tk.LabelFrame):

    def __init__(self, parent, **kw):
        tk.LabelFrame.__init__(self, parent.master, text='Parameters', labelanchor='n', **kw)
        self.parent = parent
        self._entries = dict()
        self._setup_widgets()
        self['state'] = 'disabled'

    def __setitem__(self, key, value):
        if key == 'state':
            for entry in self._entries.values():
                entry['state'] = value
        else:
            raise KeyError(f"\'ParameterFrame\' object has no key \'{key}\'")

    @property
    def fps(self):
        return int(self._entries['fps'].get())

    @property
    def size(self):
        return int(self._entries['size_x'].get()), int(self._entries['size_y'].get())

    def _setup_widgets(self):
        width = 5
        # --------   FPS  ------------ #
        fps_row = 0
        fps_label = tk.Label(self, text='FPS: ')
        fps_label.grid(row=fps_row, column=0)

        fps_entry = tk.Entry(self, width=width)
        fps_entry.insert(0, '25')
        fps_entry.grid(row=fps_row, column=1)
        self._entries['fps'] = fps_entry

        # ---------- Size -------------- #
        size_row = 1
        size_label = tk.Label(self, text='Size [px]: ')
        size_label.grid(row=size_row, column=0)

        size_x_entry = tk.Entry(self, width=width)
        size_x_entry.insert(0, '1280')
        size_x_entry.grid(row=size_row, column=1)
        self._entries['size_x'] = size_x_entry

        size_times_label = tk.Label(self, text='x')
        size_times_label.grid(row=size_row, column=2)

        size_y_entry = tk.Entry(self, width=width)
        size_y_entry.insert(0, '720')
        size_y_entry.grid(row=size_row, column=3)
        self._entries['size_y'] = size_y_entry