import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
import sys
import os
import math
import time

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import cv2
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

chn_num, photons, max_point = find_sudo_peak(Al_data, width=100)

print("CDBS data imported")
print(time.time()-start, "sec")
#######################################################################################################
"""Setting ROI"""
#######################################################################################################
# hist, bin_edges = np.histogram(Al_data, bins=60)
# bin_centers = 0.5*(bin_edges[:-1] + bin_edges[1:])

classif = GaussianMixture(n_components=7)
classif.fit(Al_data.reshape((Al_data.size, 1)))
print("Gaussian Mixture finished")
print(time.time()-start, "sec")

means_ = np.sort(np.squeeze(classif.means_))
threshold = means_[2]+2000
binary_img = Al_data > threshold

masked_Al = np.ma.masked_less_equal(Al_data, threshold)

mask_x = np.any(binary_img, axis=0)
mask_y = np.any(binary_img, axis=1)
x1 = np.argmax(mask_x)
y1 = np.argmax(mask_y)
x2 = len(mask_x) - np.argmax(mask_x[::-1])
y2 = len(mask_y) - np.argmax(mask_y[::-1])
Al_ROI = masked_Al[y1:y2, x1:x2]

# plt.figure()
# plt.imshow(Al_ROI)
# plt.show()

print("ROI masking completed")
print(time.time()-start, "sec")
#######################################################################################################
"""Gaussian Fitting & Integral on E hat axis"""
#######################################################################################################

row, column = Al_ROI.shape

E_hat = np.arange(y1, y2)
F_AUC = np.zeros(column)
plt.figure()
for c in range(column):
    Ehat_proj = Al_ROI[:, c]

    def gaussian_2(x, wid):
        """1-d gaussian: gaussian(x, amp, wid)"""
        return (np.max(Ehat_proj)) * np.exp(-(x - 513.5) ** 2 / (2 * wid ** 2))

    mod = Model(gaussian_2)
    pars = mod.make_params(wid=column)

    out = mod.fit(Ehat_proj, pars, x=E_hat)
    F_AUC[c] = integrate.simps(out.best_fit, E_hat)

    # print(c)
    # plt.plot(E_hat, Ehat_proj, '.')
    # plt.plot(E_hat, out.best_fit, '-')
    # plt.title("dE: "+str(c))
    # plt.show()
# ann_peak = max(F_AUC)
# F_AUC = np.divide(F_AUC, ann_peak)

plt.figure()
plt.plot(np.arange(x1,x2), F_AUC)
plt.yscale('log')
plt.show()

print("Gaussian fitting completed")
print(time.time()-start, "sec")