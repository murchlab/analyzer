import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from os import listdir as os_loaddir
from os.path import isfile, join, exists, split
from os import mkdir, stat
from shutil import rmtree
import re

#####################
# Basic mathematics #
#####################

# Pauli algebra

sigma_x = [[0, 1], [1, 0]]
sigma_y = [[0, -1j], [1j, 0]]
sigma_z = [[1, 0], [0, -1]]

sigma_x = np.asarray(sigma_x)
sigma_y = np.asarray(sigma_y)
sigma_z = np.asarray(sigma_z)

sigma = [sigma_x, sigma_y, sigma_z]
sigma4 = [np.eye(2), sigma_x, sigma_y, sigma_z]


def pauli_decomp(rho):
    """
        DESCRIPTION:  Calculate the pauli matrix decomposition of the density matrix rho
        INPUT:  2x2 density matrix rho
        OUTPUT:  The coefficients
    """
    vector4 = [np.trace(rho @ E) / 2 for E in sigma4]
    return np.asarray(vector4)


def bloch_vector(rho):
    """
        DESCRIPTION:  Translate the density matrix representation into bloch vector form
        INPUT:  2x2 density matrix rho
        OUTPUT:  The bloch vector components
    """
    vector = [np.trace(rho @ E) for E in sigma4[1:]]
    return np.asarray(vector)

###################
# Data structures #
###################


def broadcast(f, *seq_inputs):
    """
        DESCRIPTION:  For broadcasting a function over a sequence object
        INPUT:  f:  A function object
                seq_inputs:  A tuple of sequence data inputs
        OUTPUT:  A list of outputs
    """
    return [f(*inputs) for inputs in zip(*seq_inputs)]


def datatype(data):
    """
        DESCRIPTION:  To determine the type of the input data.
        INPUT:  data:  A sequence or step or repetition object
        OUTPUT:  A string 'seq' or 'step' or 'rep' or 'unknown'
    """
    if isinstance(data, list):
        return 'seq'
    elif isinstance(data, np.ndarray):
        if data.ndim == 1:
            return 'rep'
        else:
            return 'step'
    return False


def t_range_parser(data, t_range):

    def step_t_range_parser(step_data, t_range):
        if t_range:
            return t_range
        else:
            return [0, step_data.shape[-1]]

    def seq_t_range_parser(seq_data, t_range):
        if not(t_range and hasattr(t_range[0], "__getitem__")):
            t_range = [t_range] * len(seq_data)
        t_range = broadcast(step_t_range_parser, seq_data, t_range)
        return t_range

    data_type = datatype(data)

    funcs = {
        'seq': seq_t_range_parser,
        'step': step_t_range_parser,
    }

    return funcs[data_type](data, t_range)


def avg_time(data, t_range=None, stack=False):

    t_range = t_range_parser(data, t_range)

    def step_avg_time(step_data, t_range):
        """
            DESCRIPTION:  Calculate the time average of a step data
            INPUT:  step_data:  2D numpy array
                    t_range: numpy array [min, max]
            OUTPUT:  1D numpy array
        """
        return np.mean(step_data[:, t_range[0]:t_range[1]], axis=1)

    def seq_avg_time(seq_data, t_range):
        avg = broadcast(step_avg_time, seq_data, t_range)
        if stack:
            avg = np.hstack(avg)
        return avg

    data_type = datatype(data)

    avg_funcs = {
        'seq': seq_avg_time,
        'step': step_avg_time,
    }

    return avg_funcs[data_type](data, t_range)


def avg_rep(data, t_range=None, stack=True):

    t_range = t_range_parser(data, t_range)

    def step_avg_rep(step_data, t_range):
        """
            DESCRIPTION:  Calculate the repetition average of a step data
            INPUT:  step_data:  2D numpy array
                    t_range: numpy array [min, max]
            OUTPUT:  1D numpy array
        """
        return np.mean(step_data[:, t_range[0]:t_range[1]], axis=0)

    def seq_avg_rep(seq_data, t_range):
        avg = broadcast(step_avg_rep, seq_data, t_range)
        if stack:
            avg = np.vstack(avg)
        return avg

    data_type = datatype(data)

    avg_funcs = {
        'seq': seq_avg_rep,
        'step': step_avg_rep,
    }

    return avg_funcs[data_type](data, t_range)


# def avg_rep(seq_data, nmin=None, nmax=None, length=0):
#     avg = np.vstack(tuple(np.mean(step_data, axis=0) for step_data in seq_data))
#     return avg


def show(data, mode='sample', delta_t = 20E-9):
    mpl.rcParams['figure.dpi'] = 300

    def seq_show(seq_data):
        def plot_data_full():
            plot_data = np.vstack([step_data for step_data in seq_data])
            return plot_data

        def plot_data_sample():
            plot_data = np.vstack([step_data[1] for step_data in seq_data])
            return plot_data

        def plot_data_average():
            plot_data = avg_rep(seq_data)
            return plot_data

        plot_data_funcs = {
            'full': plot_data_full,
            'sample': plot_data_sample,
            'average': plot_data_average
        }
        plot_data = plot_data_funcs[mode]()
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax2 = ax1.twiny()
        ax1.imshow(plot_data)
        ax1.set_xlabel('Time (ns)')
        ax1.set_ylabel('Steps')
        ax2.set_xlabel('Time index')
        ax1.axis('auto')
        ax1.set_xticklabels(ax1.get_xticks() * delta_t * 1E9)
        ax2.set_xlim(ax1.get_xlim())
        plt.show()

    seq_show(data)

#####################
# File IO functions #
#####################

def load(path, num_steps=1, num_files=-1, verbose=True, rebuild_cache=False):
    """
    DESCRIPTION:  Load the record data from .txt files
    INPUT:  path:  the directory of the measurement record
            num_steps:
            num_files:  the number of record files to read. num=-1 stands for reading all files in the directory.
                        rebuild_cache:
    OUTPUT:  Returns a analyzer.Record object of type 'sequence'
    NOTES:  A binary cache (.npy) mechanism is implemented in this functioon
    """

    cache_folder_name = 'cache'

    def clean_cache():
        try:
            rmtree(join(path, cache_folder_name))
        except:
            pass

    ##END clean_cache

    def listdir(path, appendix='txt'):
        """
            DESCRIPTION:  List the valid .txt record files in a given directory
            INPUT:  Path string to the directory
            OUTPUT:  A sorted list of path strings
        """
        files = [f for f in os_loaddir(path) if isfile(join(path, f))]
        index_p = re.compile(r"(?:.*?)(\d+)(?:\.{})".format(appendix))
        index = []
        i = 0
        while i < len(files):
            match = index_p.match(files[i])
            if match and stat(join(path, files[i])).st_size:
                index.append(int(match.group(1)))
                i += 1
            else:
                files.pop(i)
        files = [join(path, f) for _, f in sorted(zip(index, files))]
        return files

    ##END listdir

    def loadfile(file_name):
        """
            DESCRIPTION:  Load the data from a single file
            INPUT:  Path string to the file
            OUTPUT:  A list of numpy arrays (one for each pattern)
        """
        if verbose:
            print("Loading file #" + str(i) + " ...")
        head, tail = split(file_name)
        file_name_npy = join(head, cache_folder_name, tail[:-4] + '.npy')
        if not rebuild_cache and exists(file_name_npy):
            seq_rec_file = np.load(file_name_npy, allow_pickle=True)
        else:
            record = np.loadtxt(file_name, dtype=np.float32)
            record = np.transpose(record)
            seq_rec_file = [record[j::num_steps, :] for j in range(num_steps)]
            np.save(file_name_npy, seq_rec_file)
        return seq_rec_file

    files = listdir(path)
    if num_files == -1:
        num_files = len(files)
    data_list = []
    if rebuild_cache:
        clean_cache()
    if rebuild_cache or (not exists(join(path, cache_folder_name))):
        mkdir(join(path, cache_folder_name))
    for i in range(num_files):
        seq_rec_i = loadfile(files[i])
        data_list.append(seq_rec_i)
    seq_rec = [np.vstack(seq_rec_i) for seq_rec_i in zip(*data_list)]
    return seq_rec

    ##END loadfile
##END load


