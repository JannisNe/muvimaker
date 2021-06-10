import tkinter as tk
from tkinter import scrolledtext as st
import logging
import queue
from muvimaker import main_logger, main_queue, logger_format


logger = main_logger.getChild(__name__)


class ConsoleUi:
    """Poll messages from a logging queue and display them in a scrolled text widget"""

    def __init__(self, frame, log_queue=main_queue):

        self.frame = frame

        # Create a ScrolledText wdiget
        self.scrolled_text = st.ScrolledText(frame, state='disabled', height=7)
        self.scrolled_text.grid(row=0, column=0, sticky='nsew')
        self.scrolled_text.configure(font=('TkFixedFont', 10))
        self.scrolled_text.tag_config('INFO', foreground='black')
        self.scrolled_text.tag_config('DEBUG', foreground='gray')
        self.scrolled_text.tag_config('WARNING', foreground='orange')
        self.scrolled_text.tag_config('ERROR', foreground='red')
        self.scrolled_text.tag_config('CRITICAL', foreground='red', underline=1)

        # Create a logging handler using a queue
        self.log_queue = log_queue

        # Start polling messages from the queue
        self.frame.after(100, self.poll_log_queue)

    def display(self, record):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logger_format)
        msg = stream_handler.format(record)
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(tk.END, msg + '\n', record.levelname)
        self.scrolled_text.configure(state='disabled')
        # Autoscroll to the bottom
        self.scrolled_text.yview(tk.END)

    def poll_log_queue(self):
        # Check every 100ms if there is a new message in the queue to display
        while True:
            try:
                record = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.display(record)
        self.frame.after(100, self.poll_log_queue)


class LoggingFrame(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        ConsoleUi(self)
