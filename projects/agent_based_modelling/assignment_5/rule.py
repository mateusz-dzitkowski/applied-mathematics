from functools import cached_property
from typing import Callable

import numpy as np
from pydantic import BaseModel, Field
from scipy.ndimage import shift

BITS_IN_RULE = 8
RULES = 2**BITS_IN_RULE


StepFunction = Callable[[np.ndarray], np.ndarray]


class Rule(BaseModel):
    number: int = Field(ge=0, lt=RULES)

    @cached_property
    def bit_list(self) -> list[int]:
        return [int(bit) for bit in f"{self.number:0{BITS_IN_RULE}b}"]

    @cached_property
    def step_function(self) -> StepFunction:
        def step_function(middle: np.ndarray) -> np.ndarray:
            left = shift(middle, 1, cval=False)
            right = shift(middle, -1, cval=False)
            return np.where(
                left,
                np.where(
                    middle,
                    np.where(
                        right,
                        self.bit_list[0],
                        self.bit_list[1],
                    ),
                    np.where(
                        right,
                        self.bit_list[2],
                        self.bit_list[3],
                    ),
                ),
                np.where(
                    middle,
                    np.where(
                        right,
                        self.bit_list[4],
                        self.bit_list[5],
                    ),
                    np.where(
                        right,
                        self.bit_list[6],
                        self.bit_list[7],
                    ),
                ),
            )

        return step_function
