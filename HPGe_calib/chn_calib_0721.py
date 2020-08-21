import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks, peak_widths

# file_list=[]
# for subdir, dirs, files in os.walk('C:/Users/admin/PycharmProjects/CDBS/HPGe_calib/'):
#     file_list.append(glob.glob(os.path.join(subdir,'*.asc')))

# datA = np.loadtxt('./detectorA_Cs137.asc')
# chn = datA[:, 0]
# count = datA[:, 1]
#
# peaks, _ = find_peaks(count, height=20000)
# result_half = peak_widths(count, peaks, rel_height=0.5)
# plt.plot(chn, count)
# plt.plot(peaks, count[peaks], 'x')
# plt.plot(np.add(np.zeros_like(count),20000), '--', color='gray')
# plt.show()
#
# 283.53keV = 348
# 511keV = 2495
# 661.657keV = 3236

# resolution 0.20331578947368426
# FWHM = 2*sqrt(2ln(2))*sigma

datB = np.loadtxt('C:/Users/user/PycharmProjects/CDBS/HPGe_calib/detectorB_Cs137.asc')
chn = datB[:, 0]
count = datB[:, 1]

peaks, _ = find_peaks(count, height=20000)
result_half = peak_widths(count, peaks, rel_height=0.5)
plt.plot(chn, count)
plt.plot(peaks, count[peaks], 'x')
plt.plot(np.add(np.zeros_like(count),20000), '--', color='gray')
plt.show()