import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from text_parser import *
from lmfit.models import GaussianModel
import time

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

x_width = 100
chn_num, photons, max_point = find_sudo_peak(Al_data, width=x_width)

########################################################################################################################
def gauss_2(x, amp, wid):
    """1-d gaussian: gaussian(x, amp, cen, wid)"""
    return (amp / (np.sqrt(2 * np.pi) * wid)) * np.exp(-(x - max_point[0]) ** 2 / (2 * wid ** 2))

########################################################################################################################
"""Gaussian fitting on E hat projection"""
########################################################################################################################
mod = Model(gauss_2)

y_width = 100

e_hat = np.arange(max_point[0]-y_width, max_point[0]+y_width)
# e_hat = np.arange(504, 521)
F_AUC = np.zeros(y_width*2)

# e_hat_proj = Al_data[e_hat, 511]  # CBDS projection on e_hat
# pars = mod.guess(e_hat_proj, x=e_hat)
# out = mod.fit(e_hat_proj, pars, x=e_hat)
# print(out.best_values)

for n, chn in enumerate(chn_num):
    e_hat_proj = Al_data[e_hat, chn]  # CBDS projection on e_hat
    pars = mod.make_params(amp=e_hat_proj[y_width]*np.sqrt(2*np.pi), wid=y_width/2)
    out = mod.fit(e_hat_proj, pars, x=e_hat)
    F_AUC[n] = integrate.simps(out.best_fit, e_hat)
    if (n % 5) == 0:
        print(n)
        plt.figure()
        plt.plot(e_hat, e_hat_proj, '.')
        plt.plot(e_hat, out.best_fit, '-')
        plt.title(str(n))
        plt.show()
        time.sleep(0.2)


# x_adj_CDBS = np.add(0.134 * np.subtract(chn_num, max_point[1]), 511)
#
# plt.plot(x_adj_CDBS, photons)
# plt.plot(x_adj_CDBS, F_AUC)
# plt.yscale('log')
# plt.show()












# gmodel = Model(gaussian)
# params = gmodel.make_params(cen=max_point[1], amp=np.max(photons)*(np.sqrt(2*np.pi)*width/2), wid= width/2)
# result = gmodel.fit(photons, params, x=chn_num)
#
# x_hr = np.linspace(np.min(chn_num), np.max(chn_num), 10 * len(chn_num))
## energy_bin = (661.7-511)/(502-266)
## x_energy = np.add(energy_bin*x_hr, 511)
# y_hr = gaussian(x_hr, amp=result.best_values['amp'], cen=result.best_values['cen'], wid=result.best_values['wid'])
## AUC = integrate.simps(result.best_fit, chn_num)
# print(result.best_values['cen'])
# plt.plot(chn_num, photons, 'o')
# plt.plot(x_hr, y_hr, label='Al_sheet')
# plt.yscale('log')
# plt.xlabel('CHN')
# plt.ylabel('Count')
# plt.legend(loc='best')
# plt.show()