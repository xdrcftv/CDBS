import glob
import os

import numpy as np
from scipy import ndimage


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

# def gaussian_2(x, amp, wid):
#     """1-d gaussian: gaussian(x, amp, wid)"""
#     return (amp / (np.sqrt(2 * np.pi) * wid)) * np.exp(-(x - ) ** 2 / (2 * wid ** 2))


def find_sudo_peak(matrix, width):
    """should be changed (peak detection algorithm needed)"""
    """return chn_num(x), count(y), max_point(peak index)"""
    max_point = np.squeeze(np.array(np.where(matrix == np.amax(matrix))))
    chn_num = np.arange(max_point[1]-width, max_point[1]+width+1) # len(chn_num) = 2*width+1
    count = matrix[max_point[0], chn_num]
    return chn_num, count, max_point


def extract_ROI(matrix, width, ROI_thickness):
    max_point = np.squeeze(np.array(np.where(matrix == np.amax(matrix))))
    chn_num = np.arange(max_point[1]-width, max_point[1]+width+1)
    ROI_matrix = matrix[max_point[0]-ROI_thickness:max_point[0]+ROI_thickness, chn_num]
    ROI_count = ROI_matrix.sum(axis=0)
    return chn_num, ROI_count, max_point

def count_normalize(count):
    count_flip = np.flip(count)
    count_avg = np.divide(np.add(count, count_flip), 2)
    count_normal = np.divide(count_avg, np.max(count_avg))
    count_normal_err = np.divide(np.sqrt(count_avg/2), np.max(count_avg))
    return count_normal, count_normal_err
