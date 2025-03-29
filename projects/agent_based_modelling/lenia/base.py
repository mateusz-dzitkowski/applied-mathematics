from typing import Callable

import numpy as np

Array = np.ndarray
Func = Callable[[Array], Array]
BCS = Callable[[Array], ...]


def bell(m: float, s: float) -> Func:
    def inner(x: Array) -> Array:
        return np.exp(-0.5 * ((x - m) / s) ** 2)

    return inner


def h(x: Array) -> Array:
    return np.heaviside(x, 0)


def bcs_wall(width: int) -> BCS:
    def inner(arr: Array):
        arr[:, :width, :] = 0
        arr[:, -width:, :] = 0
        arr[:, :, :width] = 0
        arr[:, :, -width:] = 0

    return inner
