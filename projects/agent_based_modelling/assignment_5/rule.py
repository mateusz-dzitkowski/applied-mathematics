from functools import cached_property
from typing import Protocol

import numpy as np
from pydantic import BaseModel, Field

BITS_IN_RULE = 8
MAX_RULE_NUMBER = 2**BITS_IN_RULE - 1


class StepFunction(Protocol):
    def __call__(self, p: np.ndarray, q: np.ndarray, r: np.ndarray) -> np.ndarray: ...


class Rule(BaseModel):
    number: int = Field(ge=0, le=MAX_RULE_NUMBER)

    @cached_property
    def bit_list(self) -> list[int]:
        without_padding = [int(bit) for bit in f"{self.number:b}"]
        return [0] * (BITS_IN_RULE - len(without_padding)) + without_padding

    @cached_property
    def step_function(self) -> StepFunction:
        def step_function(p: np.ndarray, q: np.ndarray, r: np.ndarray) -> np.ndarray:
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

        return step_function
