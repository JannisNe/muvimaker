import os
import logging
import queue
import multiprocessing
import sys
import shutil

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


# def setup_logger(queue, level='INFO', logger=main_logger):
#     stream_handler = logging.StreamHandler()
#     stream_handler.setFormatter(logger_format)
#     logger.addHandler(stream_handler)
#
#     queue_handler = QueueHandler(queue)
#     queue_handler.setFormatter(logger_format)
#     logger.addHandler(queue_handler)
#
#     logger.setLevel(level)
#
#
# setup_logger(main_queue)

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

# indir = mv_scratch + '/input'
# outdir = mv_scratch + '/output'
# storage_dir = mv_scratch + '/storage'
#
# projects_dir = f'{indir}/projects'
#
# project_handler_dir = f'{storage_dir}/project_handler'
#
# for directory in [indir, outdir, storage_dir,
#                   projects_dir, project_handler_dir]:
#     if not os.path.exists(directory):
#         os.mkdir(directory)

