from dataclasses import dataclass, field
from functools import cached_property
from typing import Self

import numpy as np
from scipy.signal import convolve2d

from base import Array, Func


@dataclass
class Kernel:
    arr: Array

    @classmethod
    def from_func(
        cls,
        func: Func,
        radius_cells: int,
        radius_xy: float,
        midpoint: bool = False,
        peaks: Array | list[float] | None = None,
    ) -> Self:
        if peaks is None:
            peaks = [1]
        peaks = np.asarray(peaks)

        if midpoint:
            x, y = np.meshgrid(*np.ogrid[-radius_cells : radius_cells + 1, -radius_cells : radius_cells + 1])
        else:
            x, y = np.meshgrid(*np.ogrid[-radius_cells:radius_cells, -radius_cells:radius_cells])
        x, y = x / radius_xy * len(peaks), y / radius_xy * len(peaks)
        r = np.sqrt(x**2 + y**2)
        return cls(arr=(r < len(peaks)) * peaks[np.minimum(r.astype(int), len(peaks)-1)] * func(r % 1))

    @cached_property
    def fft(self) -> Array:
        print("using fft to compute the convolution")
        return np.fft.fft2(np.fft.fftshift(self.arr / self.arr.sum()))

    def apply(self, arr: Array) -> Array:
        if arr.shape == self.arr.shape:  # if you set everything up nicely you will get a performance boost from fft
            return np.real(np.fft.ifft2(self.fft * np.fft.fft2(arr)))
        return convolve2d(arr, self.arr, mode="same", boundary="wrap")
