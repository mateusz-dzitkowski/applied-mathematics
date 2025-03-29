from typing import Callable

import numpy as np


def runge_kutta_4(func: Callable[[float, float], float], init: float, x: np.ndarray) -> np.ndarray:
    output = [init]

    for h, t in zip(np.diff(x), x[:-1]):
        y = output[-1]
        k1 = func(t, y)
        k2 = func(t + h / 2, y + h * k1 / 2)
        k3 = func(t + h / 2, y + h * k2 / 2)
        k4 = func(t + h, y + h * k3)
        output.append(y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4))

    return np.array(output)
