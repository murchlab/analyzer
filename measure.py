import matplotlib.transforms as transforms
from sklearn import mixture
from analyzer import *


def measurehist(data, t_range, fit=True, n_components=3, log_scale=True, show_plot=True, calc_temp=False, qubit_freq=None):

    fit_color = '#16817a'
    thresholds_color = '#035aa6'
    T_color = '#8566aa'
    plot_bottom = 1E-4
    thresholds_dashline_y = 0.73
    thresholds_text_y = 0.75
    T_text_x = 0.98
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

    thresholds = None
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
            T = qubit_temp(weights[0], weights[1], qubit_freq)
            print("T = {} mK".format(T * 1E3))
            plt.text(T_text_x, T_text_y, 'T = {:.2f} mK'.format(T * 1E3), horizontalalignment='right',
                     color=T_color, transform=ax.transAxes)
    if log_scale:
        plt.yscale("log")
    if show_plot:
        plt.show()
    return thresholds


def crop(data, t_range):

    t_range = t_range_parser(data, t_range)

    def step_crop(step_data, step_t_range):
        return step_data[:, step_t_range[0]:step_t_range[1]]

    def seq_crop(seq_data, t_range):
        return broadcast(step_crop, seq_data, t_range)

    data_type = datatype(data)['type']

    crop_funcs = {
        'seq': seq_crop,
        'step': step_crop,
    }

    return crop_funcs[data_type](data, t_range)


def select(data, state, t_range, thresholds, num_only=False):

    t_range = t_range_parser(data, t_range)

    avg = avg_time(data, t_range)

    if not hasattr(thresholds, '__getitem__'):
        thresholds = [thresholds]

    thresholds = np.insert(thresholds, 0, -np.inf)
    thresholds = np.append(thresholds, np.inf)

    def step_select(step_data, step_avg):
        selected = step_data[np.logical_and(step_avg > thresholds[state], step_avg < thresholds[state + 1]), :]
        if num_only:
            return len(selected)
        return selected

    def seq_select(seq_data, avg):
        selected = broadcast(step_select, seq_data, avg)
        return selected

    data_type = datatype(data)['type']

    select_funcs = {
        'seq': seq_select,
        'step': step_select,
    }

    return select_funcs[data_type](data, avg)


def population(data, t_range, thresholds, normalized=True):

    t_range = t_range_parser(data, t_range)

    avg = avg_time(data, t_range)

    if not hasattr(thresholds, '__getitem__'):
        thresholds = [thresholds]

    thresholds = np.insert(thresholds, 0, -np.inf)
    thresholds = np.append(thresholds, np.inf)

    def step_select(step_data, step_avg):
        N_tot = datatype(step_data)['num_reps']
        N_states = []
        for state in range(len(thresholds) - 1):
            N_state = np.sum(np.logical_and(step_avg > thresholds[state], step_avg < thresholds[state + 1]))
            N_states.append(N_state)
        N_states = np.asarray(N_states)
        if normalized:
            return N_states / N_tot
        else:
            return N_states

    def seq_select(seq_data, avg):
        selected = broadcast(step_select, seq_data, avg)
        return selected

    data_type = datatype(data)['type']

    select_funcs = {
        'seq': seq_select,
        'step': step_select,
    }

    return select_funcs[data_type](data, avg)
