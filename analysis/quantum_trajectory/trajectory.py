import numpy as np
from analyzer import *


def SME_solver(V, x0, z0, OmegaR, dt, eta, k, gamma, final_only=False):
    cos = np.cos
    sin = np.sin

    def step_SME_solver(V):
        """
            DESCRIPTION:
            INPUT:
            OUTPUT: x_data, z_data
        """
        transpose = False
        if len(V.shape) == 1:
            V = V.reshape((1, -1))
            transpose = True
        num_reps = V.shape[0]
        t_max = V.shape[1]
        z = np.zeros((num_reps, t_max + 1))
        x = np.zeros((num_reps, t_max + 1))
        z[:, 0] = z0
        x[:, 0] = x0
        for i in range(t_max):
            zd = z[:, i] * cos(OmegaR * dt) + x[:, i] * sin(OmegaR * dt)
            xd = x[:, i] * cos(OmegaR * dt) - z[:, i] * sin(OmegaR * dt)
            z[:, i + 1] = zd + 4 * eta * k * (1 - zd ** 2) * (V[:, i] - zd) * dt
            x[:, i + 1] = xd - (2 * k + gamma) * xd * dt - 4 * eta * k * xd * zd * (V[:, i] - zd) * dt
        if final_only:
            return x[:, -1], z[:, -1]
        else:
            return x, z

    def rep_SME_solver(V):
        """
            DESCRIPTION:
            INPUT:
            OUTPUT: shape = (2, t_max)
        """
        V = V.reshape((1, -1))
        x, z = step_SME_solver(V)
        return np.squeeze(x), np.squeeze(z)

    def seq_SME_solver(V):
        """
            DESCRIPTION:
            INPUT:
            OUTPUT: A list of step_SME_solver outputs
        """
        xz_seq = broadcast(step_SME_solver, V)
        x = [xz_step[0] for xz_step in xz_seq]
        z = [xz_step[1] for xz_step in xz_seq]
        return x, z

    data_type = datatype(V)['type']

    solver_funcs = {
        'seq': seq_SME_solver,
        'step': step_SME_solver,
        'rep': rep_SME_solver
    }

    return solver_funcs[data_type](V)


def tomog_select(seq_data, seq_x_final, x_target, tol=0.01):
    num_steps = datatype(seq_data)['num_steps']
    seq_selected = []
    for i in range(num_steps):
        x_cond = np.abs(seq_x_final[i] - x_target[i]) < tol
        seq_selected.append(seq_data[i][x_cond])
    return seq_selected
