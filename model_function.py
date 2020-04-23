import numpy as np


def gaussian_band(x, amp_band, wid_band):
    """1-d gaussian: gaussian(x, amp, wid)"""
    return (amp_band / (np.sqrt(2 * np.pi) * wid_band)) * np.exp(-(x) ** 2 / (2 * wid_band ** 2))


def gaussian_1(x, amp_1, wid_1):
    """1-d gaussian: gaussian(x, amp, cen, wid)"""
    return (amp_1 / (np.sqrt(2 * np.pi) * wid_1)) * np.exp(-(x) ** 2 / (2 * wid_1 ** 2))


def gaussian_2(x, amp_2, wid_2):
    """1-d gaussian: gaussian(x, amp, cen, wid)"""
    return (amp_2 / (np.sqrt(2 * np.pi) * wid_2)) * np.exp(-(x) ** 2 / (2 * wid_2 ** 2))


def gaussian_3(x, amp_3, wid_3):
    """1-d gaussian: gaussian(x, amp, cen, wid)"""
    return (amp_3 / (np.sqrt(2 * np.pi) * wid_3)) * np.exp(-(x) ** 2 / (2 * wid_3 ** 2))


def gaussian_4(x, amp_4, wid_4):
    """1-d gaussian: gaussian(x, amp, cen, wid)"""
    return (amp_4 / (np.sqrt(2 * np.pi) * wid_4)) * np.exp(-(x) ** 2 / (2 * wid_4 ** 2))


def parabola_band_1(x, c_1, alpha_1):
    """parabola for fermi level1"""
    value = c_1*(x-alpha_1)(x+alpha_1)
    return np.clip(value, a_min=0)


def parabola_band_2(x, c_2, alpha_2):
    """parabola for fermi level2"""
    value = c_2*(x-alpha_2)(x+alpha_2)
    return np.clip(value, a_min=0)


def parabola_band_3(x, c_3, alpha_3):
    """parabola for fermi level3"""
    value = c_3*(x-alpha_3)(x+alpha_3)
    return np.clip(value, a_min=0)
