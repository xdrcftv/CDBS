import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from text_parser import *
from lmfit.models import GaussianModel
from mpl_toolkits.mplot3d import Axes3D

#######################################################################################################
"""Parsing txt data to python"""
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

#######################################################################################################
"""Setting ROI"""
#######################################################################################################
hist, bin_edges = np.histogram(Al_data, bins=60)
bin_centers = 0.5*(bin_edges[:-1] + bin_edges[1:])

classif = GaussianMixture(n_components=7)
classif.fit(Al_data.reshape((Al_data.size, 1)))

threshold = np.sort(np.squeeze(classif.means_))[3]

binary_img = Al_data > threshold

mask_x = np.any(binary_img, axis=0)
mask_y = np.any(binary_img, axis=1)
x1 = np.argmax(mask_x)
y1 = np.argmax(mask_y)
x2 = len(mask_x) - np.argmax(mask_x[::-1])
y2 = len(mask_y) - np.argmax(mask_y[::-1])

Al_ROI = Al_data[y1:y2, x1:x2]

#######################################################################################################
"""Gaussian Fitting & Integral on E hat axis"""
#######################################################################################################
mod = Model(gaussian)

row, column = Al_ROI.shape

E_hat = np.arange(y1, y2)
F_AUC = np.zeros(column)
plt.figure()
for c in range(column):
    Ehat_proj = Al_ROI[:, c]
    pars = mod.make_params(amp=Ehat_proj[int(row/2)]*np.sqrt(2*np.pi), cen=E_hat[int(row/2)], wid=column)
    out = mod.fit(Ehat_proj, pars, x=E_hat)
    F_AUC[c] = integrate.simps(out.best_fit, E_hat)
    if (c % 5) == 0:
        print(c)
        plt.plot(E_hat, Ehat_proj, '.')
        plt.plot(E_hat, out.best_fit, '-')
        plt.title("dE: "+str(c))
        plt.show()




# plt.figure(figsize=(11,4))
#
# plt.subplot(131)
# plt.imshow(Al_data)
# plt.axis('off')
# plt.subplot(132)
# plt.plot(bin_centers, hist, lw=2)
# plt.axvline(threshold, color='r', ls='--', lw=2)
# plt.text(0.57, 0.8, 'histogram', fontsize=20, transform = plt.gca().transAxes)
# plt.yticks([])
# plt.subplot(133)
# plt.imshow(binary_img, cmap=plt.cm.gray, interpolation='nearest')
# plt.axis('off')
#
# plt.subplots_adjust(wspace=0.02, hspace=0.3, top=1, bottom=0.1, left=0, right=1)
# plt.show()
#