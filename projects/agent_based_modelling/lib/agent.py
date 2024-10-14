from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from .space import Pos
if TYPE_CHECKING:
    from .model import Model


class Agent(ABC):
    model: "Model"

    def __init__(self, model: "Model"):
        self.model = model

    @abstractmethod
    def step(self): ...

    @property
    def pos(self) -> Pos:
        return self.model.get_pos_of(self)
