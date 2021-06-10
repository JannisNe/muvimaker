from muvimaker import main_logger
import tkinter as tk
from tkinter import filedialog as fd


logger = main_logger.getChild(__name__)


class BaseDialogue(tk.Toplevel):
    """base class for dialogues"""

    def __init__(self, parent, title, def_msg, button_text, insert='', topmost=True):
        tk.Toplevel.__init__(self, parent)

        self.parent = parent
        self.title = title
        self.msg = tk.StringVar()
        self.msg.set(def_msg)
        self.button_text = button_text
        self.insert = insert

        self.entry = None

        self._setup_standard_widgets()
        self._setup_xtra_widgets()
        self.attributes('-topmost', topmost)
        self.start_mainloop()

    def start_mainloop(self):
        self.mainloop()

    def _setup_standard_widgets(self):
        msg_label = tk.Label(self, textvariable=self.msg)
        msg_label.pack(fill='both', expand=True)

        e = tk.Entry(self, borderwidth=5)
        e.insert(0, self.insert)
        e.pack(fill='both', expand=True)
        self.entry = e

        button = tk.Button(self, text=self.button_text, command=self.button_action)
        button.pack(fill='both', expand=True)

    def _setup_xtra_widgets(self):
        pass

    def button_action(self):
        raise NotImplementedError('To be implemented in subclasses!')


class BrowseDialogue(BaseDialogue):

    def start_mainloop(self):
        self.entry.bind('<1>', self.browse)
        self.mainloop()

    def browse_function(self):
        raise NotImplementedError('To be implemented in subclasses')

    def browse(self, event):
        filename = self.browse_function()
        self.entry.delete(0, 'end')
        self.entry.insert(0, filename)

    def button_action(self):
        raise NotImplementedError('To be implemented in subclasses')


class OpenFileDialogue(BrowseDialogue):
    def browse_function(self):
        return fd.askopenfilename()


class OpenDirectoryDialoge(BrowseDialogue):
    def browse_function(self):
        return  fd.askdirectory()