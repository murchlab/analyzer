import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
from sklearn import mixture
from analyzer import *
from scipy import constants


def measurehist(data, t_range, fit=True, n_components=3, log_scale=True, show_plot=True, calc_temp=False, qubit_freq=None):

    fit_color = '#16817a'
    thresholds_color = '#035aa6'
    T_color = '#8566aa'
    plot_bottom = 1E-4
    thresholds_dashline_y = 0.73
    thresholds_text_y = 0.75
    T_text_x = 0.9
    T_text_y = 0.95
    # For performance considerations, here I am not sampling the whole data set while calculating the min & max and
    # performing the first step fittinig.
    sample_num = 100000

    avg = avg_time(data, t_range, stack=True)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.hist(avg, bins="auto", density=True, color=barplot_color)

    def gmm_fit():

        min = np.min(avg[:sample_num])
        max = np.max(avg[:sample_num])
        mean_init = np.linspace(min, max, n_components)
        gmm_tied = mixture.GaussianMixture(n_components, means_init=mean_init.reshape(-1, 1),
                                           covariance_type='tied', tol=1E-10, n_init=5)
        gmm_tied.fit(avg[:sample_num].reshape(-1, 1))
        print(gmm_tied.means_)
        gmm = mixture.GaussianMixture(n_components, weights_init=gmm_tied.weights_, means_init=gmm_tied.means_,
                                      max_iter=100, tol=1E-100, warm_start=False)
        gmm.fit(avg.reshape(-1, 1))
        # gmm = gmm_tied
        x_eval = np.histogram_bin_edges(avg, bins="auto")

        plt.plot(x_eval, np.exp(gmm.score_samples(x_eval.reshape(-1, 1))), color=fit_color)
        plt.ylim(bottom=plot_bottom)
        return gmm.weights_, gmm.means_, gmm.covariances_

    plt.xlabel('Signal $V$')
    plt.ylabel('Probability distribution $f(V)$')

    if fit:
        weights, means, covariances = gmm_fit()
        weights = weights.flatten()
        means = means.flatten()
        covariances = covariances.flatten()
        fit_params = np.asarray([[w, m, c] for w, m, c in sorted(zip(weights, means, covariances), reverse=True)])
        weights, means, covariances = fit_params.transpose()
        # print(fit_params)
        thresholds = gaussian2thresholds(means, covariances)
        print("Thresholds:")
        print(thresholds)
        trans = transforms.blended_transform_factory(ax.transData, ax.transAxes)
        for threshold in thresholds:
            plt.axvline(threshold, plot_bottom, thresholds_dashline_y, linestyle='--', color=thresholds_color)
            plt.text(threshold, thresholds_text_y, '{:.2f}'.format(threshold), horizontalalignment='center',
                     color=thresholds_color, transform=trans)
        if calc_temp:
            h = constants.h
            k = constants.k
            T = h * qubit_freq / k / (np.log(weights[0]) - np.log(weights[1]))
            print("T = {} mK".format(T * 1E3))
            plt.text(T_text_x, T_text_y, 'T = {:.2f} mK'.format(T * 1E3), horizontalalignment='center',
                     color=T_color, transform=ax.transAxes)
    if log_scale:
        plt.yscale("log")
    if show_plot:
        plt.show()


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
