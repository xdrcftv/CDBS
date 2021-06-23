import matplotlib.pyplot as plt
from lmfit import Model

from text_parser import *

####################################### plt control ################################################
SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 15

plt.rc('font', size=MEDIUM_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=15)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=12)    # fontsize of the tick labels
plt.rc('ytick', labelsize=12)    # fontsize of the tick labels
plt.rc('legend', fontsize=MEDIUM_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
####################################### plt control ################################################

dir_path = 'C:/Users/user/PycharmProjects/CDBS/ARAA_analysis/ARAA_October'
CDBS_files = glob.glob(os.path.join(dir_path, "*.asc"))
file_name = []
CDBS_matrix = {}

width = 77
gmodel = Model(gaussian)

linestyle = ['s--', '^--', '>--', 'o--', 'h--', 'd--', '+--']

s_window = 6
w_window = [7, 9]
s_parameter = np.zeros(len(CDBS_files))
w_parameter = np.zeros(len(CDBS_files))


for n, file in enumerate(CDBS_files):
    basename = os.path.splitext(os.path.basename(file))[0]
    file_name.append(basename)
    f = open(file, 'r')
    lines = f.readlines()
    CDBS_data = []
    for i in range(1024):
        count = lines[i + 23].split(",")
        count = list(map(int, count))
        del count[0]
        CDBS_data.append(count)
    rot_matrix = ndimage.rotate(np.array(CDBS_data, dtype=float), -45)
    CDBS_matrix[basename] = ndimage.zoom(rot_matrix, 1 / np.sqrt(2))

    if n == 0:
        matrix = CDBS_matrix[basename]
        max_point = np.squeeze(np.array(np.where(matrix == np.amax(matrix))))
        x_CDBS = np.arange(max_point[1] - width, max_point[1] + width + 1)
        ROI_matrix_1 = matrix[max_point[0] - 1:max_point[0] + 1, x_CDBS]
        ROI_matrix_3 = matrix[max_point[0] - 3:max_point[0] + 3, x_CDBS]
        ROI_matrix_5 = matrix[max_point[0] - 5:max_point[0] + 5, x_CDBS]

        ROI_count_1 = ROI_matrix_1.sum(axis=0)
        count_1, count_1_err = count_normalize(ROI_count_1)
        ROI_count_3 = ROI_matrix_3.sum(axis=0)
        count_3, count_3_err = count_normalize(ROI_count_3)
        ROI_count_5 = ROI_matrix_5.sum(axis=0)
        count_5, count_5_err = count_normalize(ROI_count_5)

        x_adj_CDBS = (0.134) * np.subtract(x_CDBS, max_point[1]) * 2000 / 511

    else:
        break

plt.title('ROI Thickness')
plt.yscale('log')
plt.errorbar(x_adj_CDBS, count_1, yerr=count_1_err, fmt=linestyle[1], label='chn_num:1', capsize=2)
plt.errorbar(x_adj_CDBS, count_3, yerr=count_3_err, fmt=linestyle[2], label='chn_num:3', capsize=2)
plt.errorbar(x_adj_CDBS, count_5, yerr=count_5_err, fmt=linestyle[3], label='chn_num:5', capsize=2)
plt.xlabel("P")
plt.ylabel("Normalized Intensity")
plt.legend(loc='best')
plt.show()
