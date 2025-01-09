from functools import cached_property
from typing import Callable

import numpy as np
from pydantic import BaseModel, Field
from scipy.ndimage import shift

BITS_IN_RULE = 8
RULES = 2**BITS_IN_RULE

_not = np.logical_not
_and = np.logical_and
_or = np.logical_or
_xor = np.logical_xor


StepFunction = Callable[[np.ndarray], np.ndarray]

CUSTOM_STEP_FUNCTIONS = {
    30: lambda p, q, r: _xor(p, _or(q, r)),
    36: lambda p, q, r: _and(_xor(p, q), _xor(q, r)),
    42: lambda p, q, r: _and(r, _not(_and(p, q))),
    45: lambda p, q, r: _xor(p, _or(q, _not(r))),
    50: lambda p, q, r: _and(_not(q), _or(p, r)),
    57: lambda p, q, r: _xor(q, _or(p, _not(r))),
    106: lambda p, q, r: _xor(r, _and(p, q)),
    110: lambda p, q, r: _or(_and(q, _not(p)), _xor(q, r)),
    118: lambda p, q, r: _or(_and(p, _not(_and(q, r))), _and(_not(p), _xor(q, r))),
    146: lambda p, q, r: _and(_or(p, r), _xor(_xor(p, q), r)),
}


class Rule(BaseModel):
    number: int = Field(ge=0, lt=RULES)

    @cached_property
    def bit_list(self) -> list[int]:
        return [int(bit) for bit in f"{self.number:0{BITS_IN_RULE}b}"]

    @cached_property
    def step_function(self) -> StepFunction:
        if func := CUSTOM_STEP_FUNCTIONS.get(self.number):
            return lambda q: func(left(q), q, right(q)).astype(int)
        return self.generic_step_function

    @cached_property
    def generic_step_function(self) -> StepFunction:
        def inner(q: np.ndarray) -> np.ndarray:
            p = left(q)
            r = right(q)
            return np.where(
                p,
                np.where(
                    q,
                    np.where(
                        r,
                        self.bit_list[0],
                        self.bit_list[1],
                    ),
                    np.where(
                        r,
                        self.bit_list[2],
                        self.bit_list[3],
                    ),
                ),
                np.where(
                    q,
                    np.where(
                        r,
                        self.bit_list[4],
                        self.bit_list[5],
                    ),
                    np.where(
                        r,
                        self.bit_list[6],
                        self.bit_list[7],
                    ),
                ),
            )

        return inner


def left(x: np.ndarray) -> np.ndarray:
    return shift(x, 1, cval=0)


def right(x: np.ndarray) -> np.ndarray:
    return shift(x, -1, cval=0)
