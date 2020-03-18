from text_parser import *
from lmfit import Model
import os

CDBS_path = 'C:/KAERI/CDBS/'
subdir_name = []
subdir_path = []
for root, dirs, files in os.walk('C:/KAERI/CDBS/'):
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

x, y, max_point = find_sudo_peak(CDBS_matrix[0], width=width)
params = gmodel.make_params(cen=max_point[1], amp=np.max(y)*(np.sqrt(2*np.pi)*width/2), wid= width/2)
result = gmodel.fit(y, params, x=x)

x_hr = np.linspace(np.min(x), np.max(x), 10*len(x))
# energy_bin = (661.7-511)/(502-266)
# x_energy = np.add(energy_bin*x_hr, 511)
y_hr = gaussian(x_hr, amp=result.best_values['amp'], cen=result.best_values['cen'], wid=result.best_values['wid'])
# AUC = integrate.simps(result.best_fit, x)
plt.plot(x, y, 'o')
plt.plot(x_hr, y_hr, label=subdir_name[0])
plt.yscale('log')
plt.xlabel('CHN')
plt.ylabel('Count')
plt.legend(loc='best')
plt.show()

