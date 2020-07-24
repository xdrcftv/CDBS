import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks, peak_widths

# dat = np.loadtxt('2020_03_18/HPGe A Ra-226.asc')
# chn = dat[:, 0]
# count = dat[:, 1]
#
# peaks, _ = find_peaks(count, height=1100)
# results_half = peak_widths(count, peaks, rel_height=0.5)
# plt.figure()
# plt.plot(count)
# plt.plot(peaks, count[peaks], 'x')
# plt.plot(np.add(np.zeros_like(count), 1100), '--', color='gray')
# plt.hlines(*results_half[1:], color='C2')
# plt.show()

# 0.134
# sigma = 13.776435/2.354820 = 5.850313

dat = np.loadtxt('2020_03_18/HPGe B Ra-226.asc')
chn = dat[:, 0]
count = dat[:, 1]

peaks, _ = find_peaks(count, height=1100)
results_half = peak_widths(count, peaks, rel_height=0.5)
plt.figure()
plt.plot(count)
plt.plot(peaks, count[peaks], 'x')
plt.plot(np.add(np.zeros_like(count), 1100), '--', color='gray')
plt.hlines(*results_half[1:], color='C2')
plt.show()