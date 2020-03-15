from text_parser import *

PA_path = 'C:/KAERI/CDBS/1. 570 Polymer_A/'
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
    data = np.array(data, dtype=float)
    rot_data = ndimage.rotate(data, -45, reshape=False)
    DB_spectrum[file_name[n]]=rot_data


