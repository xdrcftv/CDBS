import numpy as np
import matplotlib.pyplot as plt
# from scipy.optimize import curve_fit
from scipy import integrate
from text_parser import *
from lmfit import Model
import os

CDBS_path = 'C:/KAERI/CDBS/'
subdir_name = []
subdir_path = []
for root, dirs, files in os.walk(CDBS_path):
    if len(dirs) > 0:
        for dir_name in dirs:
            subdir_name.append(dir_name)
            subdir_path.append(CDBS_path+dir_name)
    break

CDBS_matrix = []
for subdir in subdir_path:
    CDBS_matrix.append(CDBS_parser(subdir))

width = 10
gmodel = Model(gaussian)

normal_curves = []
x_hr = np.linspace(-width, width, 10*width)

for i, matrix in enumerate(CDBS_matrix):
    x, y, max_point = find_sudo_peak(matrix, width=width)
    params = gmodel.make_params(cen=max_point[0], amp=np.max(y)*(np.sqrt(2*np.pi)*width/2), wid= width/2)
    result = gmodel.fit(y, params, x=x)
    # y_hr = gaussian(x_hr, 1, 0, wid=result.best_values['wid'])  # 가우시안 함수로 그리기
    AUC = integrate.simps(result.best_fit, x)

    plt.plot(result.best_fit, label=subdir_name[i])
    # plt.plot(np.divide(result.best_fit, AUC),'-', label='gmodel'+subdir_name[i])
    # normal_curves.append(np.divide(result.best_fit, AUC))
    # plt.plot(y_hr, label=subdir_name[i])

plt.legend(loc='best')
plt.show()

# plt.plot(x, y, 'bo')
# plt.plot(x, result.init_fit, 'k--', label='initial fit')
# plt.plot(x, result.best_fit, 'r-', label='best fit')
# plt.legend(loc='best')
# plt.show()
# plt.plot(x, y, 'bo')
# plt.plot(x, result.init_fit, 'k--', label='initial fit')
# plt.plot(x, n_curve, 'r-', label='n_curve')
# plt.legend(loc='best')
# plt.show()

