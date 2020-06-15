import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from text_parser import *
from lmfit.models import GaussianModel
from mpl_toolkits.mplot3d import Axes3D

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

width = 50
chn_num, photons, max_point = find_sudo_peak(Al_data, width=width)

Al_shape = Al_data.shape
fig = plt.figure()
ax = Axes3D(fig)
ax.zaxis.set_scale('log')

X = np.arange(max_point[1]-width, max_point[1]+width)
Y = np.arange(max_point[0]-width, max_point[0]+width)
XX, YY = np.meshgrid(X, Y)
ax.plot_surface(XX, YY, Al_data[XX,YY], rstride=1, cstride=1, cmap='jet')
plt.show()