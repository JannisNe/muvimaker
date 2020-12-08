import tkinter as tk
from tkinter import scrolledtext as st
import logging
import queue
from muvi_maker import main_logger, main_queue, logger_format


logger = main_logger.getChild(__name__)


# class QueueHandler(logging.Handler):
#     """Class to send logging records to a queue
#
#     It can be used from different threads
#     """
#
#     def __init__(self, log_queue):
#         super().__init__()
#         self.log_queue = log_queue
#
#     def emit(self, record):
#         self.log_queue.put(record)


class ConsoleUi:
    """Poll messages from a logging queue and display them in a scrolled text widget"""

    def __init__(self, frame, log_queue=main_queue):

        self.frame = frame

        # Create a ScrolledText wdiget
        self.scrolled_text = st.ScrolledText(frame, state='disabled', height=6)
        self.scrolled_text.grid(row=0, column=0)#, sticky=(N, S, W, E))
        self.scrolled_text.configure(font='TkFixedFont')
        self.scrolled_text.tag_config('INFO', foreground='black')
        self.scrolled_text.tag_config('DEBUG', foreground='gray')
        self.scrolled_text.tag_config('WARNING', foreground='orange')
        self.scrolled_text.tag_config('ERROR', foreground='red')
        self.scrolled_text.tag_config('CRITICAL', foreground='red', underline=1)

        # Create a logging handler using a queue
        self.log_queue = log_queue
        # self.queue_handler = QueueHandler(self.log_queue)
        # self.queue_handler.setFormatter(logger_format)
        # main_logger.addHandler(self.queue_handler)

        # Start polling messages from the queue
        self.frame.after(100, self.poll_log_queue)
        # process = Process(target=multiprocess_wrapping, args=(self, ))
        # process.start()
        # process.join()
        # start_new_thread(self.frame.after, (100, self.poll_log_queue,))
        # self.frame.after(100, self.poll_log_queue)

    def display(self, record):
        # msg = self.queue_handler.format(record)
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


# class LoggingWindow(tk.Tk):
#
#     def __init__(self):
#         tk.Tk.__init__(self)
#         logging_frame = LoggingFrame(self)
#         logging_frame.grid()
#         self.mainloop()
#
#     @staticmethod
#     def multiprocess_wrapping(queue, level):
#         setup_logger(queue, level, logger)
#         LoggingWindow()
