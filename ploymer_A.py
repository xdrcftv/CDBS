from text_parser import *
from lmfit import Model
from scipy.optimize import curve_fit

PA_path = 'C:/KAERI/CDBS/6. 012 N2/'
file_name = [file for file in os.listdir(PA_path) if file.endswith(".asc")]
file_path = glob.glob(os.path.join(PA_path, "*.asc"))

DB_spectrum = {}
for n, path in enumerate(file_path):
    f = open(path, 'r')
    lines = f.readlines()
    data = []
    for i in range(1024):
        count = lines[i+23].split(",")
        count = list(map(int, count))
        del count[0]
        data.append(count)
    data = np.array(data)
    rot_data = ndimage.rotate(data, -45, reshape=False)
    DB_spectrum[file_name[n]] = rot_data


gmodel = Model(gaussian)
width = 20

for item in file_name:
    x, y, max_point = find_sudo_peak(DB_spectrum[item], width=width)
    params = gmodel.make_params(cen=max_point[1], amp=np.max(y)*(np.sqrt(2*np.pi)*width/2), wid=width/2)
    result = gmodel.fit(y, params, x=x)
    AUC = integrate.simps(result.best_fit, x)

    # p0 = [max_point[1], np.max(y)*(np.sqrt(2*np.pi)*width/2)/AUC, width/2]
    # popt, _ = curve_fit(gaussian, x, np.divide(y, AUC), p0=p0)
    # plt.plot(x, gaussian(x, popt[1], popt[0], popt[2]))

    plt.plot(x, y, label=item)
    plt.plot(x, result.best_fit, label='gmodel')
    # plt.yscale('log')

plt.legend(loc='best')
plt.show()
