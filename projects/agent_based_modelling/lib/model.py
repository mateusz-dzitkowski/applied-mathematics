from abc import ABC, abstractmethod
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Iterable,
    Self,
)

from .space import Grid, Pos

if TYPE_CHECKING:
    from .agent import Agent


class Model(ABC):
    grid: Grid
    data_collectors: dict[str, Callable[[Self], Any]]
    running: bool

    def __init__(self, grid: Grid, data_collectors: dict[str, Callable[[Self], Any]]):
        self.grid = grid
        self.data_collectors = data_collectors

        self.running = True

    @abstractmethod
    def step(self): ...

    @property
    def agents(self) -> Iterable["Agent"]:
        for agent in self.grid.grid.values():
            yield agent

    @property
    def pos_agents(self) -> Iterable[tuple[Pos, "Agent"]]:
        for pos, agent in self.grid.grid.items():
            yield pos, agent

    def get_pos_of(self, agent: "Agent") -> Pos:
        return self.grid.get_pos_of(agent)

    def run_and_collect(self) -> dict[str, Any]:
        while self.running:
            self.step()

        return {key: foo(self) for key, foo in self.data_collectors.items()}
