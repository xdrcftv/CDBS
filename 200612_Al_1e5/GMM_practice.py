import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from text_parser import *


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

hist, bin_edges = np.histogram(Al_data, bins=100)
bin_centers = 0.5*(bin_edges[:-1] + bin_edges[1:])

classif = GaussianMixture(n_components=4)
classif.fit(Al_data.reshape((Al_data.size, 1)))

print(classif.means_)
threshold = np.mean(classif.means_)
print("Threshold: ",threshold)
binary_img = Al_data > threshold


plt.figure(figsize=(11,4))

plt.subplot(131)
plt.imshow(Al_data)
plt.axis('off')
plt.subplot(132)
plt.plot(bin_centers, hist, lw=2)
plt.axvline(threshold, color='r', ls='--', lw=2)
plt.text(0.57, 0.8, 'histogram', fontsize=20, transform = plt.gca().transAxes)
plt.yticks([])
plt.subplot(133)
plt.imshow(binary_img, cmap=plt.cm.gray, interpolation='nearest')
plt.axis('off')

plt.subplots_adjust(wspace=0.02, hspace=0.3, top=1, bottom=0.1, left=0, right=1)
plt.show()