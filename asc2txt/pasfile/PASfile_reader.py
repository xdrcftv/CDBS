import matplotlib.pyplot as plt
from lmfit import Model

from text_parser import *

dir_path = 'asc2txt/pasfile'
pas_files = glob.glob(os.path.join(dir_path, "*.pas"))
file_name = []
CDBS_matrix = {}

width = 55
gmodel = Model(gaussian)

linestyle = ['s-', '^-', '>-', 'o-', '-.', ':', '--', 'o-', 'o-']

s_window = 5
w_window = [7, 9]
s_parameter = np.zeros(len(pas_files))
w_parameter = np.zeros(len(pas_files))

scaling_factor = 0.993
x_pas = np.arange(511-scaling_factor*250, 511+scaling_factor*250, scaling_factor)

for n, file in enumerate(pas_files[:1]):
    basename = os.path.splitext(os.path.basename(file))[0]
    file_name.append(basename)
    f = open(file, 'r')
    lines = f.readlines()
    count = lines[0].split()
    y_pas = list(map(float, count))
    y_flip = np.flip(y_pas)
    y_avg = np.divide(np.add(y_pas, y_flip), 2)
    y_err = np.sqrt(y_avg)
    y_normal = np.divide(y_avg, np.max(y_avg))
    y_normal_err = np.divide(y_err, np.max(y_avg))

    # plt.plot(y_normal)
    plt.errorbar(x_pas, y_normal, yerr=y_err, fmt=linestyle[n], label=basename, capsize=2)
    plt.show()

"""
    CDBS_data = []
    for i in range(1024):
        count = lines[i+23].split(",")
        count = list(map(int, count))
        del count[0]
        CDBS_data.append(count)
    rot_matrix = ndimage.rotate(np.array(CDBS_data, dtype=float), -45)
    CDBS_matrix[basename] = ndimage.zoom(rot_matrix, 1/np.sqrt(2))
    x_CDBS, y_CDBS, max_point_CBDS = find_sudo_peak(CDBS_matrix[basename], width=width)
    y_flip = np.flip(y_CDBS)
    y_avg = np.divide(np.add(y_CDBS, y_flip), 2)
    y_err = np.sqrt(y_avg)
    y_normal = np.divide(y_avg, np.max(y_avg))
    y_normal_err = np.divide(y_err, np.max(y_avg))
    # plt.plot(x, np.divide(y, AUC), '.', label=basename)

    params_CDBS = gmodel.make_params(cen=max_point_CBDS[1], amp=np.max(y_CDBS) * (np.sqrt(2 * np.pi) * width / 2), wid=width / 2)
    result_CDBS = gmodel.fit(y_CDBS, params_CDBS, x=x_CDBS)

    ####################################################################################################################
    # s window calculation
    ####################################################################################################################
    AUC_total = integrate.simps(y_CDBS, x_CDBS)
    AUC_center = integrate.simps(y_CDBS[width-s_window:width+s_window], x_CDBS[width-s_window:width+s_window])
    s_value = AUC_center/AUC_total
    s_parameter[n] = s_value
    print("S_parameter of "+basename+": ", s_value)
    ####################################################################################################################
    # w window calculation
    ####################################################################################################################
    AUC_wing = integrate.simps(y_CDBS[width+w_window[0]:width+w_window[1]], x_CDBS[width+w_window[0]:width+w_window[1]])
    w_value = 2*AUC_wing/AUC_center
    w_parameter[n] = w_value
    print("W_parameter of " + basename + ": ", w_value)
    #x_adj_CDBS = np.add((0.134*np.sqrt(2)) * np.subtract(x_CDBS, max_point_CBDS[1]), 511.1) #  Incident Photon Energy [keV]
    x_adj_CDBS = (0.134) * np.subtract(x_CDBS, max_point_CBDS[1]) *2000/511
    # plt.plot(x_adj_CDBS, np.divide(y_CDBS, np.max(y_CDBS)), linestyle[n], label=label_list[n])

    # x_hr = np.linspace(x[0], x[-1], 10*len(x))
    # y_hr = gaussian(x_hr, cen=result.best_values['cen'], amp=result.best_values['amp'], wid=result.best_values['wid'])
    # plt.plot(x_hr, y_hr, '-')

    # plt.plot(x_adj_CDBS, y_avg, linestyle[n], label=label_list[n])
    plt.errorbar(x_adj_CDBS, y_normal, yerr=y_normal_err, fmt=linestyle[n], label=basename, capsize=2)
plt.title('ARAA CDBS')
plt.yscale('log')
plt.xlabel("P(10e-3mc)")
plt.ylabel("Normalized Intensity [A.U.]")
plt.legend(loc='best')
plt.show()
"""