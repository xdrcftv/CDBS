import numpy as np
import glob
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from scipy import ndimage

from text_parser import *
from lmfit import Model
from lmfit.models import GaussianModel
from model_function import *

Al_path = 'C:/Users/admin\PycharmProjects\CDBS\Al_0514/200506 CDBS Al.asc'
f = open(Al_path, 'r')
lines = f.readlines()
CDBS_data = []
for i in range(1024):
    count = lines[i+23].split(",")
    count = list(map(int, count))
    del count[0]
    CDBS_data.append(count)

Al_data = ndimage.rotate(np.array(CDBS_data, dtype=float), -45, reshape=False)

# Al_matrix = []
# Al_matrix.append(CDBS_parser(Al_path))

width = 50
x, y, max_point = find_sudo_peak(Al_data, width=width)

def gauss_2(x, amp, wid):
    """1-d gaussian: gaussian(x, amp, cen, wid)"""
    return (amp / (np.sqrt(2 * np.pi) * wid)) * np.exp(-(x - max_point[0]) ** 2 / (2 * wid ** 2))

gauss1 = Model(gaussian_1)
gauss2 = Model(gaussian_2)
gauss3 = Model(gaussian_3)

pars = gauss1.make_params()
pars.update(gauss2.make_params())
pars.update(gauss3.make_params())


# pars['g1_center'].set(value=509)
# pars['g2_center'].set(value=509)
# pars['g3_center'].set(value=509)

print(pars)

mod = gauss1 + gauss2 + gauss3

out = mod.fit(y, pars, x=x)
dely = out.eval_uncertainty(sigma=4)
print(dely)
print(out.fit_report(min_correl=0.5))

fig, axes = plt.subplots(1, 2, figsize=(12.8, 4.8))
axes[0].plot(x, y, 'b')
axes[0].plot(x, out.best_fit, 'r-', label='best fit')
axes[0].fill_between(x, out.best_fit-dely, out.best_fit+dely, color='#ABABAB', label = '2-$\sigma$ uncertainty band')
axes[0].legend(loc='best')

comps = out.eval_components(x=x)
axes[1].plot(x, y, 'b')
axes[1].plot(x, comps['g1_'], 'g--', label='Gaussian component 1')
axes[1].plot(x, comps['g2_'], 'm--', label='Gaussian component 2')
axes[1].plot(x, comps['g3_'], 'k--', label='Gaussian component 3')
axes[1].legend(loc='best')

plt.xlabel('CHN')
plt.ylabel('Count')
plt.yscale('log')
plt.show()


# plt.plot(x, y, 'o')
# plt.yscale('log')
# plt.show()
