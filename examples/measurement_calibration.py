import analyzer as az
import analyzer.measure as ms

path = "Directory/of/the/data"
num_steps = 101

seq_rec = az.load(path, num_steps=num_steps, num_files=20)

delta_t = 20E-9

t_range_herald = [[114 - i, 130 - i] for i in range(num_steps)]

t_range_final = [154, 164]

az.show(seq_rec, t_range_herald, mode='sample', delta_t=delta_t)
thresholds = ms.measurehist(seq_rec, t_range_herald, calc_temp=True, qubit_freq=4.48E9)
# ms.measurehist(seq_rec, t_range_final)
