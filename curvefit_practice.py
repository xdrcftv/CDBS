import os

from lmfit import Model

from text_parser import *

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
energy_bin = (661.7-511)/(502-266)
# plt.imshow(CDBS_matrix[5])
# plt.show()
linestyle = ['--', 'o', '^', '>', 's', '-.', ':']
for i, matrix in enumerate(CDBS_matrix):
    x, y, max_point = find_sudo_peak(matrix, width=width)
    params = gmodel.make_params(cen=max_point[1], amp=np.max(y)*(np.sqrt(2*np.pi)*width/2), wid= width/2)
    result = gmodel.fit(y, params, x=x)
    AUC = integrate.simps(result.best_fit, x)

    plt.plot(x, y, '-.', label=subdir_name[i])
    # plt.plot(x, result.best_fit, '--')
    # plt.plot(x_hr, y_hr, label=subdir_name[i])
    # y_hr = gaussian(x_hr, 1, 0, wid=result.best_values['wid'])  # 가우시안 함수로 그리기
    print(result.best_values['wid'])
    # plt.plot(np.add(energy_bin*x_hr, 511),y_hr,'{}'.format(linestyle[i]), label=subdir_name[i])
    # plt.yscale('log')

plt.xlabel("Energy (keV)")
plt.ylabel("Counts")
plt.legend(loc='best')
plt.show()


# plt.legend(loc='best')
# plt.show()

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