from typing import (
    Generic,
    Iterator,
    NamedTuple,
    TypeVar,
)

T = TypeVar("T")


class Pos(NamedTuple):
    x: int
    y: int


class Grid(Generic[T]):
    width: int
    height: int
    grid: dict[Pos, T]
    reverse_lookup: dict[int, Pos]

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = {}
        self.reverse_lookup = {}

    @property
    def size(self) -> int:
        return self.width * self.height

    def get(self, pos: Pos) -> T | None:
        return self.grid.get(pos)

    def set(self, pos: Pos, val: T):
        if not self.out_of_bounds(pos):
            self.grid[pos] = val
            self.reverse_lookup[id(val)] = pos

    def get_pos_of(self, val: T) -> Pos | None:
        return self.reverse_lookup.get(id(val))

    def coord_iter(self) -> Iterator[Pos]:
        for x in range(self.width):
            for y in range(self.height):
                yield Pos(x, y)

    def out_of_bounds(self, pos: Pos) -> bool:
        return not (0 <= pos.x < self.width and 0 <= pos.y < self.height)
