import math
import numpy as np
from skimage import metrics


def calculate_psnr(img1, img2):
    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)
    mse = np.mean((img1 - img2)**2)
    if mse == 0:
        return float('int')
    return 20 * math.log10(255.0/math.sqrt(mse))

