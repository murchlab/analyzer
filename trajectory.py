import numpy as np


def SMEupdate(V, z0, x0, OmegaR, dt, eta, k, gamma, just_final=False):
    cos = np.cos
    sin = np.sin

    def SMEupdate_pulse(V, z0, x0, OmegaR, dt, eta, k, gamma, just_final=False):
        transpose = False
        if len(V.shape) == 1:
            V = V.reshape((1, -1))
            transpose = True
        num = V.shape[0]
        length = V.shape[1]
        z = np.zeros((num, length + 1))
        x = np.zeros((num, length + 1))
        z[:, 0] = z0
        x[:, 0] = x0
        for i in range(0, length):
            zd = z[:, i] * cos(OmegaR * dt) + x[:, i] * sin(OmegaR * dt)
            xd = x[:, i] * cos(OmegaR * dt) - z[:, i] * sin(OmegaR * dt)
            z[:, i + 1] = zd + 4 * eta * k * (1 - zd ** 2) * (V[:, i] - zd) * dt
            x[:, i + 1] = xd - (2 * k + gamma) * xd * dt - 4 * eta * k * xd * zd * (V[:, i] - zd) * dt
        if just_final:
            return z[:, -1], x[:, -1]
        elif transpose:
            return z.reshape((-1, )), x.reshape((-1, ))
        else:
            return z, x
    if isinstance(V, list):
        z = []
        x = []
        for V_pulse in V:
            z_pulse, x_pulse = SMEupdate_pulse(V_pulse, z0, x0, OmegaR, dt, eta, k, gamma, just_final=just_final)
            z.append(z_pulse)
            x.append(x_pulse)
    else:
        z, x = SMEupdate_pulse(V, z0, x0, OmegaR, dt, eta, k, gamma, just_final=just_final)
    return z, x


def SMEupdate2(V, ue0, ze0, xe0, z, x, OmegaR, dt, eta, k, gamma):
    cos = np.cos
    sin = np.sin
    length = len(V)
    ue = np.zeros(length)
    ze = np.zeros(length)
    xe = np.zeros(length)
    ue[0] = ue0
    ze[0] = ze0
    xe[0] = xe0
    for i in range(0, length - 1):
        zed = ze[i] * cos(OmegaR * dt) + xe[i] * sin(OmegaR * dt)
        xed = xe[i] * cos(OmegaR * dt) - ze[i] * sin(OmegaR * dt)
        ue[i + 1] = ue[i] + 4 * eta * k * (zed - z[i] * ue[i]) * (V[i] - z[i]) * dt
        ze[i + 1] = zed + 4 * eta * k * (ue[i] - z[i] * zed) * (V[i] - z[i]) * dt
        xe[i + 1] = xed - (2 * k + gamma) * xed * dt - 4 * eta * k * z[i] * xed * (V[i] - z[i]) * dt
    return ue, ze, xe


def tomog_selection(seq,target_z, z, x, tol=0.01):
    length = target_z.shape[0]
    z_sel = []
    for i in range(length):
        z_cond = np.abs(z[i][:, -1] - target_z[i]) < tol
        z_sel.append(seq[i][z_cond])
    return z_sel
