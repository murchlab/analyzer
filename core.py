import numpy as np
import matplotlib.pyplot as plt
from os import listdir as os_loaddir
from os.path import isfile, join, exists, basename
from os import mkdir, stat
import re
import h5py


def load(path, num_steps=1, num_files=-1, verbose=True, rebuild_cache=True):
    """
    DESCRIPTION:  load the record data from .txt files
    INPUT:  path:  the directory of the measurement record
            num_steps:
            num-files:  the number of record files to read. num=-1 stands for reading all files in the directory.
                        rebuild_cache:
    OUTPUT:  returns a analyzer.Record object of type 'sequence'
    NOTES:  a binary cache (.npy) mechanism is implemented in this functioon
    """

    cache_folder_name = 'cache'

    def listdir(path):
        """
            DESCRIPTION:  list the valid .txt record files in a given directory
            INPUT:  path string to the directory
            OUTPUT:  a sorted list of path strings
        """
        files = [f for f in os_loaddir(path) if isfile(join(path, f))]
        index_p = re.compile(r"(?:.*?)(\d+)(?:\.txt)")
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

    files = listdir(path)
    if num_files == -1:
        num_files = len(files)
    data_list = []
    if not exists(join(path, cache_folder_name)):
        mkdir(join(path, cache_folder_name))
    for i in range(num_files):
        if verbose:
            print("Loading file #" + str(i) + " ...")
        file_name = join(path, cache_folder_name, basename(files[i])[:-4] + '.npy')
        if not rebuild_cache and exists(file_name):
            seq_rec_i = np.load(file_name, allow_pickle=True)
        else:
            record_raw = np.loadtxt(files[i], dtype=np.float32)
            pulse_len = len(record_raw)
            record = np.transpose(record_raw)
            seq_rec_i = [record[j::num_steps, :] for j in range(num_steps)]
            np.save(file_name, seq_rec_i)
        data_list.append(seq_rec_i)
    data = [np.vstack(pulse_list) for pulse_list in zip(*data_list)]
    seq_rec = Record('sequence', data=data)
    return seq_rec


def cache_clean():
    print(123)


class Record():
    """
    DESCRIPTION:  list the valid .txt record files in a given directory
    INPUT:  path string to the directory
    OUTPUT:  a sorted list of path strings
    """
    def __init__(self, type, data=None, num_steps=0):
        self.type = type
        self.data = data
        if type == 'pulse':

        if type == 'sequence':
            if data:
                self.num_steps = len(data)
                self.len = np.asarray([pulse_rec_data.shape[-1] for pulse_rec_data in data])

    def avg_pulse(self, nmin=None, nmax=None, length=0):
        avg = []
        for pulse_rec_data in self.data:
            avg.append(np.mean(pulse_rec_data, axis=0))
        return Record('sequence', data=avg)

    def show(self):
        len_max = np.max(self.len)
        avg_padded = np.zeros((self.num_steps, len_max))
        avg = self.avg_pulse()
        for pulse_avg, pulse_len in zip(avg.data, self.len):
            avg_padded[:pulse_len] = pulse_avg
        plt.imshow(avg_padded)
        plt.show()

