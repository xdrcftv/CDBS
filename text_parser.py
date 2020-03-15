import numpy as np
import glob
import matplotlib.pyplot as plt
from scipy import ndimage
from scipy.signal import find_peaks, peak_prominences
from lmfit import Model
import os
from scipy import integrate


def CDBS_parser(path):
    """read asc files under path and return np matrix"""
    asc_file_list = glob.glob(os.path.join(path, "*CDBS*.asc"))
    f = open(asc_file_list[0], 'r')
    lines = f.readlines()
    CDBS_data = []
    for i in range(1024):
        count = lines[i+23].split(",")
        count = list(map(int, count))
        del count[0]
        CDBS_data.append(count)

    CDBS_data = ndimage.rotate(np.array(CDBS_data, dtype=float), -45, reshape=False)
    return CDBS_data


def find_subdir(root):
    """ return subdir under root"""
    subdir_path = []
    for root, dirs, files in os.walk(root):
        if len(dirs) > 0:
            for dir_name in dirs:
                subdir_path.append(root + dir_name)
        break
    return subdir_path


def gaussian(x, amp, cen, wid):
    """1-d gaussian: gaussian(x, amp, cen, wid)"""
    return (amp / (np.sqrt(2 * np.pi) * wid)) * np.exp(-(x - cen) ** 2 / (2 * wid ** 2))


def find_sudo_peak(matrix, width):
    """should be changed (peak detection algorithm needed)"""
    """return chn_num(x), count(y), max_point(peak index)"""
    max_point = np.squeeze(np.array(np.where(matrix == np.amax(matrix))))
    chn_num = np.arange(max_point[1]-width, max_point[1]+width)
    count = matrix[max_point[0], chn_num]
    return chn_num, count, max_point


