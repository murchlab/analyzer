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


def broadcast(f, seq_inputs):
    """
        DESCRIPTION:  For broadcasting a function over a sequence object
        INPUT:  f:  A function object
                seq_inputs:  A tuple of sequence data inputs
        OUTPUT:  A list of outputs
    """
    return [f(*inputs) for inputs in zip(seq_inputs)]


def avg_time(seq_data, nmin=[], nmax=[], length=0, stack=False):
    avg = []
    i = 0
    for pulse in seq_data:
        if length:
            nmax_i = nmin[i] + length - 1
        else:
            nmax_i = nmax[i]
        avg.append(np.mean(pulse[:, nmin[i]:nmax_i], axis=1))
        i += 1
    if stack:
        avg = np.hstack(avg)
    return avg


def average_step(seq_data, nmin=None, nmax=None, length=0):
    avg = np.vstack(tuple(np.mean(step_data, axis=0) for step_data in seq_data))
    return avg


def show(seq_data, mode='sample', delta_t = 20E-9):

    mpl.rcParams['figure.dpi'] = 300
    def show_full():
        stacked_data = np.vstack(tuple(pattern for pattern in seq_data))
        plt.imshow(stacked_data)
        plt.xlabel('Time index')
        plt.ylabel('Pattern')
        plt.show()

    def show_sample():
        stacked_data = np.vstack(tuple(pattern[1] for pattern in seq_data))
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax2 = ax1.twiny()
        ax1.imshow(stacked_data)
        ax1.set_xlabel('Time (ns)')
        ax1.set_ylabel('Steps')
        ax2.set_xlabel('Time index')
        ax1.axis('auto')
        ax1.set_xticklabels(ax1.get_xticks() * delta_t * 1E9)
        ax2.set_xlim(ax1.get_xlim())
        plt.show()

    def show_average():
        avg_data = average_step(seq_data)
        plt.imshow(avg_data)
        plt.xlabel('Time index')
        plt.ylabel('Pattern')
        plt.show()

    show_funcs = {
        'full': show_full,
        'sample': show_sample,
        'average': show_average
    }
    show_funcs[mode]()


class Record():
    """
    DESCRIPTION:  The class for record data.
    FUNCTIONS:
    """

    def __init__(self, dtype, data=None, delta_t=None):
        self.dtype = dtype
        self.data = data
        self.delta_t = delta_t

        def pattern_init():
            pass

        def sequence_init():
            if data:
                self.num_steps = len(data)
                self.shapes = np.asarray([pattern_rec_data.shape for pattern_rec_data in data])

        init_funcs = {
            'pattern': pattern_init,
            'sequence': sequence_init
        }
        init_funcs[dtype]()

    # Average can be evaluated along two axes

    def avg_time(self, nmin=[], nmax=[], length=0, stack=False):
        avg = []
        i = 0
        for pulse in self.data:
            if length:
                nmax_i = nmin[i] + length - 1
            else:
                nmax_i = nmax[i]
            avg.append(np.mean(pulse[:, nmin[i]:nmax_i], axis=1))
            i += 1
        if stack:
            avg = np.hstack(avg)
        return avg

    def average_step(self, nmin=None, nmax=None, length=0):
        avg = np.vstack(tuple(np.mean(step_data, axis=0) for step_data in self.data))
        return avg

    def show(self, mode='sample'):
        def show_full():
            stacked_data = np.vstack(tuple(pattern for pattern in self.data))
            plt.imshow(stacked_data)
            plt.xlabel('Time index')
            plt.ylabel('Pattern')
            plt.show()

        def show_sample():
            stacked_data = np.vstack(tuple(pattern[1] for pattern in self.data))
            fig = plt.figure()
            ax1 = fig.add_subplot(111)
            ax2 = ax1.twiny()
            ax1.imshow(stacked_data)
            ax1.set_xlabel('Time (ns)')
            ax1.set_ylabel('Steps')
            ax2.set_xlabel('Time index')
            ax1.axis('auto')
            ax1.set_xticklabels(ax1.get_xticks() * self.delta_t * 1E9)
            ax2.set_xlim(ax1.get_xlim())
            plt.show()

        def show_average():
            avg_data = self.average_step()
            plt.imshow(avg_data)
            plt.xlabel('Time index')
            plt.ylabel('Pattern')
            plt.show()

        show_funcs = {
            'full': show_full,
            'sample': show_sample,
            'average': show_average
        }
        show_funcs[mode]()

    # def show(self):
    #     len_max = np.max(self.len)
    #     avg_padded = np.zeros((self.num_steps, len_max))
    #     avg = self.avg_pattern()
    #     for pattern_avg, pattern_len in zip(avg.data, self.len):
    #         avg_padded[:pulse_len] = pulse_avg
    #     plt.imshow(avg_padded)
    #     plt.show()


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


