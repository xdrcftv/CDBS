from text_parser import *
from lmfit import Model
import os

dir_path = './2020_03_18'
CDBS_files = glob.glob(os.path.join(dir_path, "*CDBS*.asc"))
file_name = []
CDBS_matrix = {}
label_list = ['sample A', 'sample B', 'sample 1', 'sample 2', 'sample 3']

width = 30
gmodel = Model(gaussian)


linestyle = ['s', '^', '>', 'o','-.', ':', '--']

file = CDBS_files[0]
basename = os.path.basename(file)
file_name.append(basename)
f = open(file, 'r')
lines = f.readlines()
CDBS_data = []
for i in range(1024):
    count = lines[i+23].split(",")
    count = list(map(int, count))
    del count[0]
    CDBS_data.append(count)
rot_matrix = ndimage.rotate(np.array(CDBS_data, dtype=float), -45)
CDBS_matrix[basename] = ndimage.zoom(rot_matrix, 1/np.sqrt(2))
x_CDBS, ROI_CDBS, max_point_CBDS = extract_ROI(CDBS_matrix[basename], width=width)
print("ROI_CDBS shape")
print(ROI_CDBS.shape)
# plt.plot(x, np.divide(y, AUC), '.', label=basename)
for i in range(1):
    y_CDBS = ROI_CDBS[i, :]
    params_CDBS = gmodel.make_params(cen=max_point_CBDS[1], amp=np.max(y_CDBS) * (np.sqrt(2 * np.pi) * width / 2), wid=width / 2)
    result_CDBS = gmodel.fit(y_CDBS, params_CDBS, x=x_CDBS)
    AUC_CDBS = integrate.simps(result_CDBS.best_fit, x_CDBS)

    x_adj_CDBS = np.add(0.134 * np.subtract(x_CDBS, max_point_CBDS[1]), 511)
    print(result_CDBS.best_values['wid']*2.354820)
    plt.plot(x_adj_CDBS, np.divide(y_CDBS, AUC_CDBS), linestyle[i], label="{}".format(i))
# x_hr = np.linspace(x[0], x[-1], 10*len(x))
# y_hr = gaussian(x_hr, cen=result.best_values['cen'], amp=result.best_values['amp'], wid=result.best_values['wid'])
# plt.plot(x_hr, y_hr, '-')

plt.yscale('log')
plt.xlabel("Energy (keV)")
plt.ylabel("A.U.")
plt.legend(loc='best')
plt.show()
