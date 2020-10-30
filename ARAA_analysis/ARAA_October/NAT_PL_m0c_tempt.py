import matplotlib.pyplot as plt
import scipy.integrate as integrate
from lmfit import Model

from text_parser import *

dir_path = 'C:/Users/user/PycharmProjects/CDBS/ARAA_analysis/ARAA_October'
CDBS_files = glob.glob(os.path.join(dir_path, "*.asc"))
file_name = []
CDBS_matrix = {}

width = 55
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
        x_CDBS, y_CDBS, max_point_CBDS = find_sudo_peak(CDBS_matrix[basename], width=width)
        y_flip = np.flip(y_CDBS)
        y_avg_ref = np.divide(np.add(y_CDBS, y_flip), 2)

        AUC_total = integrate.simps(y_avg_ref, x_CDBS)
        AUC_sqrt = integrate.simps(np.sqrt(y_avg_ref), x_CDBS)

        y_normal_ref = np.divide(y_avg_ref, AUC_total)[width:]

        # err_plus_ref = (y_avg_ref + np.divide(np.sqrt(y_avg_ref), AUC_total + AUC_sqrt))[width:]
        # err_minus_ref = (y_avg_ref - np.divide(np.sqrt(y_avg_ref), AUC_total - AUC_sqrt))[width:]

    else:
        x_CDBS, y_CDBS, max_point_CBDS = find_sudo_peak(CDBS_matrix[basename], width=width)
        y_flip = np.flip(y_CDBS)
        y_avg = np.divide(np.add(y_CDBS, y_flip), 2)

        AUC_total = integrate.simps(y_avg, x_CDBS)
        AUC_sqrt = integrate.simps(np.sqrt(y_avg), x_CDBS)

        y_normal = np.divide(y_avg, AUC_total)[width:]
        y_ratio = np.divide(y_normal, y_normal_ref)

        # err_plus = (y_avg + np.divide(np.sqrt(y_avg), AUC_total + AUC_sqrt))[width:]
        # err_minus = (y_avg - np.divide(np.sqrt(y_avg), AUC_total - AUC_sqrt))[width:]
        # err_1 = np.abs(np.subtract(np.divide(err_plus, err_minus_ref), y_ratio))
        # err_2 = np.abs(np.subtract(np.divide(err_minus, err_plus_ref), y_ratio))
        # error = np.add(err_1, err_2)*0.005

        #x_adj_CDBS = np.add((0.134*np.sqrt(2)) * np.subtract(x_CDBS, max_point_CBDS[1]), 511.1) #  Incident Photon Energy [keV]
        x_adj_CDBS = ((0.134) * np.subtract(x_CDBS, max_point_CBDS[1]) * 2000/511)[width:]
        # plt.plot(x_adj_CDBS, np.divide(y_CDBS, np.max(y_CDBS)), linestyle[n], label=label_list[n])

        plt.plot(x_adj_CDBS, y_ratio, linestyle[n-1], label=basename)
        # plt.errorbar(x_adj_CDBS, y_ratio, yerr=error, fmt=linestyle[n], label=basename, capsize=2)

plt.plot(np.add(np.zeros_like(x_adj_CDBS), 1), '-', color='gray')
plt.title('Ratio to Reference Bulk')
plt.xlim(0, 7)
plt.ylim(0.95, 1.11)
plt.xlabel("$P_L $[10$^{-3}m_0c$]")
plt.ylabel("Ratio [A.U.]")
plt.legend(loc='best')
plt.show()
