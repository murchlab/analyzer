import analyzer as az

path = "Directory/of/the/data"
num_steps = 101

seq_rec = az.load(path, num_steps=num_steps, num_files=5)

delta_t = 20E-9
az.show(seq_rec, mode='sample', delta_t=delta_t)