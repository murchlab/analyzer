import numpy as np
import matplotlib.pyplot as plt
from os import listdir as os_loaddir
from os.path import isfile, join, exists, split
from os import mkdir, stat
from shutil import rmtree
import re

cache_folder_name = 'cache'


def load(path, num_steps=1, num_files=-1, verbose=True, rebuild_cache=False):
    """
    DESCRIPTION:  load the record data from .txt files
    INPUT:  path:  the directory of the measurement record
            num_steps:
            num_files:  the number of record files to read. num=-1 stands for reading all files in the directory.
                        rebuild_cache:
    OUTPUT:  returns a analyzer.Record object of type 'sequence'
    NOTES:  a binary cache (.npy) mechanism is implemented in this functioon
    """

    def clean_cache():
        try:
            rmtree(join(path, cache_folder_name))
        except:
            pass

    def listdir(path, appendix='txt'):
        """
            DESCRIPTION:  list the valid .txt record files in a given directory
            INPUT:  path string to the directory
            OUTPUT:  a sorted list of path strings
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

    def loadfile(file_name):
        """
            DESCRIPTION:  load the data from a single file
            INPUT:  path string to the file
            OUTPUT:  a list of numpy arrays (one for each pattern)
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
    data = [np.vstack(seq_rec_i) for seq_rec_i in zip(*data_list)]
    seq_rec = Record('sequence', data=data)
    return seq_rec


class Record():
    """
    DESCRIPTION:  The class for record data
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
            'sequence':sequence_init
        }
        init_funcs[dtype]()

    def average_pattern(self, nmin=None, nmax=None, length=0):
        avg = np.vstack(tuple(np.mean(pattern, axis=0) for pattern in self.data))
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
            ax1.set_ylabel('Pattern')
            ax2.set_xlabel('Time index')
            ax1.axis('auto')
            ax1.set_xticklabels(ax1.get_xticks() * self.delta_t * 1E9)
            ax2.set_xlim(ax1.get_xlim())
            plt.show()

        def show_average():
            avg_data = self.average_pattern()
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
