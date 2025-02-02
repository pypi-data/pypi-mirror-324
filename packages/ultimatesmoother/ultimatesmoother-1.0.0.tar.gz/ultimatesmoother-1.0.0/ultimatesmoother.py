import numpy as np

def ultimate_smoother(data: np.ndarray, period: float) -> np.ndarray:
    """
    Ultimate Smoother function by John Ehlers
    
    :param price_in: NumPy array of data values
    :param period: Critical smoothing period
    :return: Smoothed data series
    """
    if len(data) < 3:
        return data  # Not enough data to smooth
    
    a1 = np.exp(-1.414 * np.pi / period)
    b1 = 2 * a1 * np.cos(1.414 * np.deg2rad(180) / period)
    c2 = b1
    c3 = -a1 * a1
    c1 = (1 + c2 - c3) / 4
    
    us = np.copy(data)
    
    for i in range(2, len(data)):
        if i >= 4:
            us[i] = (1 - c1) * data[i] + (2 * c1 - c2) * data[i - 1] \
                    - (c1 + c3) * data[i - 2] + c2 * us[i - 1] + c3 * us[i - 2]
    
    return us