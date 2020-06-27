import analyzer as az

path = "Directory/of/the/data"
num_steps = 101

seq_rec = az.load(path, num_steps=num_steps, num_files=5)

delta_t = 20E-9
t_range_herald = [[109 - i + 5, 134 - i] for i in range(num_steps)]
t_range_final = [150 + 5, 200]

az.show(seq_rec, mode='sample', delta_t=delta_t)
# Showing the t_range_herald
# az.show(seq_rec, t_range_herald, mode='sample', delta_t=delta_t)
