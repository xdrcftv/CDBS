from lmfit import Model

from text_parser import *

dir_path = 'C:/Users/user/Desktop/DBS/GaN1'
DBS_files = glob.glob(os.path.join(dir_path, '*.Spe'))
file_name = []

gmodel = Model(gaussian)
linestyle = ['s-', '^-', '>-', 'o-', '-.', ':', '--', 'o-', 'o-']

for n, file in enumerate(DBS_files[:1]):
    basename = os.path.splitext(os.path.basename(file))[0]
    file_name.append(basename)
    f = open(file, 'r')
    lines = f.readlines()
    DBS_data = []
    # starts at 13, ends at 16397
    for i in range(16397-13):
        count = int(lines[i+12])
        DBS_data.append(count)

    energy_fit = float(lines[16403].strip()[-8:])
    width = round(10/energy_fit)

    ann_peak = round(511/energy_fit)
    chn_num = np.arange(ann_peak-width, ann_peak+width)
    x_DBS = np.multiply(energy_fit, chn_num)
    photon_count = np.array(DBS_data[chn_num[0]:chn_num[-1]])
    y_flip = np.flip(photon_count)
    y_avg = np.divide(np.add(photon_count, y_flip), 2)
    y_err = np.sqrt(y_avg/2)
    y_normal = np.divide(y_avg, np.max(y_avg))
    y_normal_err = np.divide(y_err, np.max(y_avg))

    params_DBS = gmodel.make_params(cen=ann_peak, amp=y_avg[round((len(y_avg)+1)/2)]*(np.sqrt(2*np.pi)*width/2),
                                    wid=width/2)
    result_DBS = gmodel.fit(y_avg, params_DBS, x=x_DBS)

    print(result_DBS)
