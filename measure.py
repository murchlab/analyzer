import numpy as np
import matplotlib.pyplot as plt
from sklearn import mixture
# import toolbox.sequence as sq


def measurehist(seq, nmin=[], nmax=[], log=False):
    avg = sq.avg_time(seq, nmin=nmin, nmax=nmax, stack=True)
    plothist = plt.hist(avg, bins="auto", density=True)
    if log:
        plt.yscale("log")
    return plothist


def fit(seq, nmin=[], nmax=[]):
    gmm = mixture.GaussianMixture(n_components=3)
    # gmm.set_params(max_iter=100, tol=1E-10, verbose=1)
    avg = sq.avg_time(seq, nmin=nmin, nmax=nmax, stack=True)
    gmm.fit(avg.reshape(-1, 1))
    x_eval = np.histogram_bin_edges(avg, bins="auto")
    plt.plot(x_eval, np.exp(gmm.score_samples(x_eval.reshape(-1, 1))), 'g-')
    return (gmm.means_, gmm.covariances_)


def edge_filter(pulse):
    tau = 60 * 1E-9
    dt = 20 * 1E-9
    conv_len = int(2 * tau / dt)

    exp = np.exp(- dt / tau)
    kernel = np.array([exp ** i for i in range(conv_len)])
    kernel /= np.sum(kernel)
    # kernel = np.append([0.2, 0.8], -kernel)
    # pulse = np.pad(pulse, (conv_len, 1), "edge")
    kernel = np.append(1, -kernel)
    pulse = np.pad(pulse, (conv_len, 0), "edge")
    pulse = np.convolve(pulse, kernel, mode='valid')
    std = np.std(pulse)
    mean = np.mean(pulse)
    pulse[np.abs(pulse - mean) < 1 * std] = 0
    pulse = np.abs(pulse)
    return pulse


def separate(pulse, sep_list):
    out = np.zeros(pulse.shape)
    last_point = 0
    sep_list.append(len(pulse))
    pair_list = []
    pulse -= np.mean(pulse)
    pulse /= np.std(pulse)
    for point in sep_list:
        pair_list.append([last_point, point, np.mean(pulse[last_point:point])])
        last_point = point
    i = len(pair_list) - 2
    while i >= 0:
        # print(i)
        h = np.abs(pair_list[i + 1][2] - pair_list[i][2])
        if h * (pair_list[i][1] - pair_list[i][0]) < 5:
            pair_list[i + 1][0] = pair_list[i][0]
            pair_list[i + 1][2] = np.mean(pulse[pair_list[i][0]:pair_list[i + 1][1]])
            pair_list.pop(i)
        i -= 1
    i = len(pair_list) - 2
    while i > 0:
        if (pair_list[i][1] - pair_list[i][0]) < 10 and (pair_list[i][2] - pair_list[i - 1][2]) * (pair_list[i][2] - pair_list[i + 1][2]) > 0:
            pair_list[i + 1][0] = pair_list[i][0]
            # pair_list[i + 1][2] = np.mean(pulse[pair_list[i][0]:pair_list[i + 1][1]])
            pair_list.pop(i)
        i -= 1
    for a, b, value in pair_list:
        out[a:b] = value
    return out, pair_list


def projective(pulse, sensitivity=1.0, verbose=True, num=2):
    tau = 60 * 1E-9
    dt = 20 * 1E-9
    filtered = edge_filter(pulse)
    # plt.plot(pulse)
    # plt.show()
    pair_list = []
    last_idx = -1
    for idx in np.nonzero(filtered)[0]:
        if idx > last_idx + 1:
            pair_list.append(idx)
        last_idx = idx
    return pair_list


def projective2(seq, nmin=[], nmax=[]):
    avg = sq.avg_time(seq, nmin=nmin, nmax=nmax)
    avg_stack = np.hstack(avg)
    gmm = mixture.GaussianMixture(n_components=2)
    result = []
    gmm.fit(avg_stack.reshape(-1, 1))
    for pulse in avg:
        result.append(gmm.predict(pulse.reshape(-1, 1)))
    return result, gmm


def projective3(seq, threshold, nmin=[], nmax=[]):
    avg = sq.avg_time(seq, nmin=nmin, nmax=nmax)
    result = []
    for avg_pulse in avg:
        result_pulse = np.full(avg_pulse.shape, -1)
        state_index = 0
        for lower, upper in threshold:
            result_pulse[np.logical_and(avg_pulse >= lower, avg_pulse < upper)] = state_index
            state_index += 1
        result.append(result_pulse)
    return result


def selection(seq, measure_cond, return_num=False):
    result = []
    seq_cond = []
    if isinstance(measure_cond, tuple):
        measure_cond = [measure_cond]
    for pulse in seq:
        seq_cond.append(np.full(pulse.shape[0], True))
    for i in range(len(seq_cond)):
        for m_cond in measure_cond:
            seq_cond[i] = np.logical_and(seq_cond[i], m_cond[0][i] == m_cond[1])
    if return_num:
        for i in range(len(seq)):
            result.append(np.sum(seq_cond[i]))
        result = np.array(result)
    else:
        i = 0
        for pulse in seq:
            result.append(pulse[seq_cond[i]])
            i += 1
    return result
