import os

from lmfit import Model

from text_parser import *


def gaussian_band(x_band, amp_band, wid_band):
    """1-d gaussian: gaussian_band(x_band, amp_band, wid_band)"""



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
gmodel = Model()

