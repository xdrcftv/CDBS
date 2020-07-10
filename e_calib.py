import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

dat = np.loadtxt('2020_03_18/HPGe A Ra-226.asc')
x = dat[:, 0]
y = dat[:, 1]

peaks, _ = find_peaks(y, height=1100)
plt.figure()
plt.plot(y)
plt.plot(peaks, y[peaks], 'x')
plt.plot(np.add(np.ones_like(y),1100), '--', color='gray')
plt.show()