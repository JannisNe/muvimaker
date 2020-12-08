import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from muvi_maker import main_logger


logger = main_logger.getChild(__name__)


def specptrogram_raw_to_image_arrays(x, y_array):
    """
    Takes one array of not changing x values and the corresponding arrays of y values and produces len(y_array) plots
    :param x: array-like, contains x values
    :param y_array: list of array-like, each entry must be of the same length as x
    :return: list of len(y_array)
    """
    # ensure same x- and y-axis for all graphs
    y_flat = np.array(y_array).flatten()
    logger.debug(f"x_shape: {np.shape(x)}, y_shape: {np.shape(y_array)}")
    xlim = (min(x), max(x))
    ylim = (max((1e-20, min(y_flat))), max(y_flat))
    xlabel = 'Frequency'
    ylabel = 'Volume'

    images = list()
    for y in tqdm(y_array, desc='making graphs'):
        mask = np.array(y) > 0
        this_x, this_y = np.array(x)[mask], np.array(y)[mask]
        fig, ax = plt.subplots()
        ax.plot(this_x, this_y, ls='-')
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

        fig.canvas.draw()

        # Now we can save it to a numpy array.
        data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))

        images.append(data)

    logger.debug(f'returning list of length {len(images)}')
    return images