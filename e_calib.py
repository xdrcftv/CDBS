from text_parser import *

e_calib_path = 'C:/KAERI/200313 CDBS energy calibration/'
file_name = os.listdir(e_calib_path)
file_path = glob.glob(os.path.join(e_calib_path, "*.asc"))


doppler_spectrum = {}
for n, path in enumerate(file_path):
    f = open(path, 'r')
    lines = f.readlines()
    data = []
    for i in range(1024):
        count = lines[i+23].split(",")
        count = list(map(int, count))
        del count[0]
        data.append(count)

    data = np.array(data, dtype=float)
    rot_data = ndimage.rotate(data, -45, reshape=False)
    doppler_spectrum[file_name[n]] = rot_data


#
plt.figure()
plt.title(file_name[0])
plt.imshow(doppler_spectrum[file_name[0]])
plt.show()


# plt.imshow(CDBS_data)
# plt.show()
#

# max_value = np.amax(CDBS_data)
# r, c = np.where(CDBS_data == max_value)
# print(r,c)
# print(CDBS_data[r][c])
# print(len(CDBS_data[0]))

