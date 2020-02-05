import numpy as np
import matplotlib.pyplot as plt
from os import listdir as os_loaddir
from os.path import isfile, join, exists, basename
from os import mkdir, stat
import re
import h5py




def load(path, pulse_num, num=-1, verbose=True, rebuild=False, format="npy", compressed=False):

    def listdir(path):
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
    if num == -1:
        num = len(files)
    data_list = []
    pulse_len = 0
    seq_num = 0
    if not exists(join(path, "python")):
        mkdir(join(path, "python"))
    appen = {"h5f": ".h5f", "npz": ".npz", "npy": ".npy"}
    for i in range(num):
        if verbose:
            print("Loading file #" + str(i) + " ...")
        file_name = join(path, "python", basename(files[i])[:-4] + appen[format])
        # if False:
        if not rebuild and exists(file_name):
            # pulses = np.fromfile(file_name)
            # pulses = np.load(file_name)
            pulses = [None] * pulse_num
            if format == "h5f":
                h5f = h5py.File(file_name, 'r')
                for idx in list(h5f.keys()):
                    pulses[int(idx)] = h5f[idx][:]
                h5f.close()
            elif format == "npz":
                npzfile = np.load(file_name)
                for idx in npzfile.files:
                    pulses[int(idx)] = npzfile[idx]
            else:
                pulses = np.load(file_name, allow_pickle=True)
        else:
            record = np.loadtxt(files[i], dtype=np.float32)
            if not pulse_len:
                pulse_len = record.shape[0]
                seq_num = int(record.shape[1] / pulse_num)
            record = np.transpose(record)
            pulses = [record[j::pulse_num, :] for j in range(pulse_num)]
            if format == "h5f":
                h5f = h5py.File(file_name, 'w', libver='latest')
                for idx, pulse in enumerate(pulses):
                    if compressed:
                        h5f.create_dataset(str(idx), data=pulse, compression='gzip', compression_opts=9)
                    else:
                        h5f.create_dataset(str(idx), data=pulse)
                h5f.close()
            elif format == "npz":
                if compressed:
                    np.savez_compressed(file_name, **{str(idx): pulse for idx, pulse in enumerate(pulses)})
                else:
                    np.savez(file_name, **{str(idx): pulse for idx, pulse in enumerate(pulses)})
            else:
                np.save(file_name, pulses)
        data_list.append(pulses)
    data = [np.vstack(pulse_list) for pulse_list in zip(*data_list)]
    return data


class Record(np.ndarray):

    def __init__(self, shape):
        super().__init__(shape)
        print('123')
