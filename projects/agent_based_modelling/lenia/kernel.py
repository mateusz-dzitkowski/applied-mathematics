from dataclasses import dataclass
from functools import cached_property
from typing import Self

import numpy as np
from scipy.signal import convolve2d

from base import Array, Func


@dataclass
class Kernel:
    arr: Array

    @classmethod
    def from_func(cls, func: Func, radius_cells: int, radius_xy: float, midpoint: bool = False) -> Self:
        if midpoint:
            x, y = np.meshgrid(*np.ogrid[-radius_cells : radius_cells + 1, -radius_cells : radius_cells + 1])
        else:
            x, y = np.meshgrid(*np.ogrid[-radius_cells:radius_cells, -radius_cells:radius_cells])
        x, y = x / radius_xy, y / radius_xy
        r = np.sqrt(x**2 + y**2)
        return cls(arr=func(r))

    @cached_property
    def fft(self) -> Array:
        print("using fft to compute the convolution")
        return np.fft.fft2(np.fft.fftshift(self.arr / self.arr.sum()))

    def apply(self, arr: Array) -> Array:
        if arr.shape == self.arr.shape:  # if you set everything up nicely you will get a performance boost from fft
            return np.real(np.fft.ifft2(self.fft * np.fft.fft2(arr)))
        return convolve2d(arr, self.arr, mode="same", boundary="wrap")
