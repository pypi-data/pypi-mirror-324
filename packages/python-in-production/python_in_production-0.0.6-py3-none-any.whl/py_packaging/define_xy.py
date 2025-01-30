import numpy as np


def my_sin():
    constant = np.pi
    x = np.linspace(0, 1, 50)
    y = np.sin(2 * constant * x)
    return x, y
