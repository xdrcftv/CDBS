import matplotlib.pyplot as plt
from scipy import integrate

from text_parser import *

dir_path = 'C:/Users/user/Desktop/DBS/GaN4'
DBS_files = glob.glob(os.path.join(dir_path, '*.Spe'))
file_name = []
s_parameter = np.zeros(len(DBS_files))
linestyle = ['s-', '^-', '>-', 'o-', '-.', ':', '--', 'o-', 'o-']

for n, file in enumerate(DBS_files):
    basename = os.path.splitext(os.path.basename(file))[0]
    file_name.append(basename)
    f = open(file, 'r')
    lines = f.readlines()
    DBS_data = []
    # starts at 13, ends at 16397
    for i in range(16397 - 13):
        count = int(lines[i + 12])
        DBS_data.append(count)
    energy_fit = float(lines[16403].strip()[-8:])
    width = round(10 / energy_fit)
    s_width = round(1 / energy_fit)

    ann_peak = round(511 / energy_fit)
    chn_num = np.arange(ann_peak - width, ann_peak + width + 1)  # np.arange는 마지막 성분-1 까지 만듬
    x_DBS = np.multiply(energy_fit, chn_num)
    photon_count = np.array(DBS_data[chn_num[0]:chn_num[-1] + 1])
    y_flip = np.flip(photon_count)
    y_avg = np.divide(np.add(photon_count, y_flip), 2)
    y_err = np.sqrt(y_avg / 2)
#    y_normal = np.divide(y_avg, np.max(y_avg))
#    y_normal_err = np.divide(y_err, np.max(y_avg))

    photon_energy = np.multiply(chn_num, energy_fit)

    peak_idx = np.where(abs(np.subtract(photon_energy, 511)) < (energy_fit / 2))[0][0]

    if DBS_data[ann_peak] - photon_count[peak_idx] != 0:
        print("warning, peak setting incorrect")

    AUC_total = integrate.simps(photon_count[peak_idx - width:peak_idx + width],
                                photon_energy[peak_idx - width:peak_idx + width])
    AUC_center = integrate.simps(photon_count[peak_idx - s_width:peak_idx + s_width],
                                 photon_energy[peak_idx - s_width:peak_idx + s_width])

    y_normal = np.divide(y_avg, AUC_total)
    y_normal_err = np.divide(y_err, AUC_total)

    s_value = AUC_center / AUC_total
    s_parameter[n] = s_value
    print("S_parameter of "+basename+": ", s_value)

    plt.errorbar(x_DBS, y_normal, yerr=y_normal_err, fmt=linestyle[n], label=basename, capsize=2)
plt.title('GaN DBS')
plt.yscale('log')
plt.xlabel('energy[keV]')
plt.ylabel('Normalized Intensity [A.U.]')
plt.legend(loc='best')
plt.show()
