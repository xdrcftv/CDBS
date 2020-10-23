import glob
import os

cwd = os.getcwd()
CDBS_files = glob.glob(os.path.join(cwd, "*.asc"))
file_name = []
CDBS_matrix = {}

for file in CDBS_files:
    basename = os.path.splitext(os.path.basename(file))[0]
    file_name.append(basename)
    f = open(file, 'r')
    lines = f.readlines()
    CDBS_data = []
    with open(basename[:-4]+'.txt','w') as txtfile:
        for i in range(1024):
            count = lines[i+23].split(",")
            count = list(map(int, count))
            del count[0]
            for cn in count:
                txtfile.write(str(cn)+' ')
            if i == 1024-1:
                break
            txtfile.write('\n')
            CDBS_data.append(count)
        txtfile.close()
    f.close()



