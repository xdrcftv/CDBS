import numpy as np
import glob
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from scipy import ndimage

from text_parser import *
from lmfit import Model
from lmfit.models import GaussianModel

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

width = 100
gmodel = Model(gaussian)

x, y, max_point = find_sudo_peak(Al_data, width=width)
params = gmodel.make_params(cen=max_point[1], amp=np.max(y)*(np.sqrt(2*np.pi)*width/2), wid= width/2)
result = gmodel.fit(y, params, x=x)

x_hr = np.linspace(np.min(x), np.max(x), 10*len(x))
# energy_bin = (661.7-511)/(502-266)
# x_energy = np.add(energy_bin*x_hr, 511)
y_hr = gaussian(x_hr, amp=result.best_values['amp'], cen=result.best_values['cen'], wid=result.best_values['wid'])
# AUC = integrate.simps(result.best_fit, x)
print(result.best_values['cen'])
plt.plot(x, y, 'o')
plt.plot(x_hr, y_hr, label='Al_sheet')
plt.yscale('log')
plt.xlabel('CHN')
plt.ylabel('Count')
plt.legend(loc='best')
plt.show()