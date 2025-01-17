import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
import sys
import os
import math
import time

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from text_parser import *
from lmfit.models import GaussianModel
from mpl_toolkits.mplot3d import Axes3D

#######################################################################################################
"""Parsing txt data to python"""
start = time.time()
#######################################################################################################
Al_path = "./200604 CDBS Al.asc"
f = open(Al_path, 'r')
lines = f.readlines()
CDBS_data = []
for i in range(1024):
    count = lines[i+23].split(",")
    count = list(map(int, count))
    del count[0]
    CDBS_data.append(count)

Al_data = ndimage.rotate(np.array(CDBS_data, dtype=float), -45, reshape=False)
width = 20
chn_num, photons, max_point = find_sudo_peak(Al_data, width=width)

print("CDBS data imported")
print(time.time()-start, "sec")
#######################################################################################################
"""Setting ROI"""
#######################################################################################################
# hist, bin_edges = np.histogram(Al_data, bins=60)
# bin_centers = 0.5*(bin_edges[:-1] + bin_edges[1:])

Al_ROI = Al_data[506:522, chn_num]
#######################################################################################################
"""Gaussian Fitting & Integral on E hat axis"""
#######################################################################################################

row, column = Al_ROI.shape

e_hat = np.add(np.divide(np.subtract(np.arange(16), 8), np.sqrt(2)), 1022)

F_AUC = np.zeros(column)

for n, c in enumerate(chn_num):
    e_hat_proj = Al_ROI[:, n]

    def gaussian_2(x, wid):
        """1-d gaussian: gaussian(x, amp, wid)"""
        return (np.max(e_hat_proj)) * np.exp(-(x - 514) ** 2 / (2 * wid ** 2))

    mod = Model(gaussian_2)
    pars = mod.make_params(wid=column)

    out = mod.fit(e_hat_proj, pars, x=np.arange(506, 522))
    F_AUC[n] = integrate.simps(out.best_fit, np.arange(506, 522))
    # if n % 2 == 0:
    #     plt.figure()
    #     plt.plot(e_hat, e_hat_proj, '.', label='Raw Data')
    #     plt.plot(np.subtract(e_hat, 0.3), out.best_fit, '-', label='')
    #     plt.title("dE= "+str(round(np.divide(n-width, np.sqrt(2)),1)))
    #     plt.legend(loc='best')
    #     plt.xlabel("E1+E2 [keV]")
    #     plt.ylabel("Intensity")
    #     plt.yscale('log')
    #     plt.show()
    #     time.sleep(0.2)

    # print(c)
    # plt.plot(E_hat, Ehat_proj, '.')
    # plt.plot(E_hat, out.best_fit, '-')
    # plt.title("dE: "+str(c))
    # plt.show()

x_adj_CDBS = np.add(0.134 * np.subtract(chn_num, max_point[1]), 511)

plt.figure()
plt.plot(x_adj_CDBS, np.divide(F_AUC, np.max(F_AUC)))
plt.ylabel('Normalized Intensity [A.U.]')
plt.xlabel('Energy [KeV]')
plt.yscale('log')
plt.show()



#
# ROI_chn = np.arange(column)
# normal_count = np.divide(F_AUC, np.max(F_AUC))
# x_adj_CDBS = np.add(0.134 * np.subtract(ROI_chn, np.mean(ROI_chn)), 511)
#
# plt.figure()
# plt.plot(x_adj_CDBS, normal_count)
# plt.yscale('log')
# plt.xlabel("keV")
# plt.ylabel("Normalized Intensity")
# plt.show()

print("Gaussian fitting completed")
print(time.time()-start, "sec")