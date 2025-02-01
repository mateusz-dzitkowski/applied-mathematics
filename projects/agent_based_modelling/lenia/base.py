from typing import Callable
import numpy as np


Array = np.ndarray
Func = Callable[[Array], Array]


def bell(m: float, s: float) -> Func:
    def inner(x: Array) -> Array:
        return np.exp(-0.5 * ((x - m) / s) ** 2)

    return inner


def h(x: Array) -> Array:
    return np.heaviside(x, 0)
