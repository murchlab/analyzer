import numpy as np
import matplotlib.pyplot as plt
import analyzer as az
import analyzer.measure as ms
import analyzer.trajectory as tj

pi = np.pi
delta_t = 20E-9
num_steps = 101

# Tomog_x data
path_x = "Directory/of/the/x_data"

# Tomog_z data
path_z = "Directory/of/the/z_data"

# Herald measurement parameters
t_range_herald = [[114 - i, 130 - i] for i in range(num_steps)]
threshold_herald = -188.38

# Final measurement parameters
t_range_final = [154, 164]
threshold_final = -182.50

# Weak measurement parameters
t_range_weak = [[150 - i, 150] for i in range(num_steps)]
offset = -175.485
delta_V = -3.72
Omega_R = + 0.8 * 2 * pi * 1E6
dt = 0.02 * 1E-6
eta = 0.4
k = 0.359375 * 1E6
gamma = 0.028625 * 1E6
x0 = 0
z0 = 1

# Calculate the target trajectory

seq_rec = az.load(path_x, num_steps=num_steps, num_files=3)
seq_rec = ms.select(seq_rec, 0, t_range_herald, threshold_herald)
seq_rec_rescaled = az.rescale(seq_rec, -offset, 2 / delta_V)
V = ms.crop(seq_rec_rescaled, t_range_weak)
x_target, z_target = tj.SME_solver(V[100][11], x0, z0, Omega_R, dt, eta, k, gamma)


# Calculate the tomographic verification for x

seq_rec = az.load(path_x, num_steps=num_steps, num_files=-1)
seq_rec = ms.select(seq_rec, 0, t_range_herald, threshold_herald)
seq_rec_rescaled = az.rescale(seq_rec, -offset, 2 / delta_V)
V = ms.crop(seq_rec_rescaled, t_range_weak)
seq_x_final, _ = tj.SME_solver(V, x0, z0, Omega_R, dt, eta, k, gamma, final_only=True)
seq_x_selected = tj.tomog_select(seq_rec, seq_x_final, x_target, tol=0.01)
pop_x = ms.population(seq_x_selected, t_range_final, threshold_final)
x_tomog = [step_pop[0] - step_pop[1] for step_pop in pop_x]


# Calculate the tomographic verification for z

seq_rec = az.load(path_z, num_steps=num_steps, num_files=-1)
seq_rec = ms.select(seq_rec, 0, t_range_herald, threshold_herald)
seq_rec_rescaled = az.rescale(seq_rec, -offset, 2 / delta_V)
V = ms.crop(seq_rec_rescaled, t_range_weak)
_, seq_z_final = tj.SME_solver(V, x0, z0, Omega_R, dt, eta, k, gamma, final_only=True)
seq_z_selected = tj.tomog_select(seq_rec, seq_z_final, z_target, tol=0.01)
pop_z = ms.population(seq_z_selected, t_range_final, threshold_final)
z_tomog = [step_pop[0] - step_pop[1] for step_pop in pop_z]

t_space = np.arange(0, delta_t * az.datatype(seq_rec)['num_steps'] , delta_t) * 1E6
plt.plot(t_space, x_target, 'b-', label=r'$X$')
plt.plot(t_space, z_target, 'k-', label=r'$Z$')
plt.plot(t_space, x_tomog, 'b:', label=r'$X_{tom}$')
plt.plot(t_space, z_tomog, 'k:', label=r'$Z_{tom}$')

plt.xlabel(r'Time ($\mu s$)')
plt.ylabel(r'$Z, X$')
plt.legend()

plt.show()


