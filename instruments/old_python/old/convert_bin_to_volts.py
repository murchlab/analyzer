#
# P. M. Harrington, 30 April 2019
import numpy as np
import matplotlib.pyplot as plt
from struct import *

fileName0 = r'''C:\Users\crow104e3\Documents\pmharrington\python\instruments\alazar_samples_python\ATS9870\NPT\data.bin'''

buffersPerAcquisition = 2
recordsPerBuffer = 2
channelsPerAcquisition = 2


with open(fileName0, mode='rb') as file: # b is important -> binary
    fileContent = file.read()
    file.close()

num_blocks = len(fileContent)//2
bin_format = ">"+"BB"*num_blocks
fileContent_int8_tuple = unpack(bin_format,fileContent)
fileContent_int8 = np.asarray([*fileContent_int8_tuple], dtype=np.int8)

num_samples = len(fileContent)
samples_per_record_per_channel = num_samples//(buffersPerAcquisition*recordsPerBuffer*channelsPerAcquisition)
channel_A_int8 = fileContent[samples_per_record_per_channel]

channel_A_index = []
channel_B_index = []
for i in np.arange(0,num_samples,channelsPerAcquisition*samples_per_record_per_channel):
    for j in np.arange(0,samples_per_record_per_channel):
        channel_A_index.append(i+j)
        channel_B_index.append(i+j+samples_per_record_per_channel)

channel_A_samples = fileContent_int8[channel_A_index]
channel_B_samples = fileContent_int8[channel_B_index]

plt.figure(0)
plt.plot(fileContent_int8)
plt.show()

plt.figure(1)
plt.plot(channel_A_samples)
plt.show()

plt.figure(2)
plt.plot(channel_B_samples)
plt.show()

fig = plt.gcf()
fig.canvas.manager.window.raise_()