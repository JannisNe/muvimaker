import os
import logging
import queue

# ======================== #
# ==  customize logger  == #
# ======================== #


class QueueHandler(logging.Handler):
    """Class to send logging records to a queue

    It can be used from different threads
    """

    def __init__(self, queue):
        super().__init__()
        self.log_queue = queue

    def emit(self, record):
        self.log_queue.put(record)


main_logger_name = 'main'
main_logger = logging.getLogger(main_logger_name)
logger_format = logging.Formatter('%(levelname)s - %(name)s: %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logger_format)
main_logger.addHandler(stream_handler)

main_queue = queue.Queue(-1)
queue_handler = QueueHandler(main_queue)
queue_handler.setFormatter(logger_format)
main_logger.addHandler(queue_handler)

# ====================================== #
# ==  setting up directory structure  == #
# ====================================== #

mv_scratch_key = 'MUVI_SCRATCH'


def set_scratch_dir(directory):
    main_logger.info(f'Setting scratch to {directory}')
    os.environ[mv_scratch_key] = directory


def get_editor(self):
    master = self.master
    while not (hasattr(master, 'name') and (master.name == 'editor')):
        master = master.master
    return master


# ====================================== #
# ==          initialise              == #
# ====================================== #

from muvimaker.core.project import ProjectHandler
from muvimaker.core.video import Video
from muvimaker.core.sound import Sound
from muvimaker.core.pictures import *
