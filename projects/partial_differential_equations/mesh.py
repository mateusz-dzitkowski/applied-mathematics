from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cached_property
from itertools import product
from typing import TypeAlias

from nptyping import NDArray

import numpy as np


Element: TypeAlias = tuple[int, ...]


@dataclass
class Mesh(ABC):
    shape: tuple[int, int]
    points: NDArray
    elements: list[Element]

    @staticmethod
    @abstractmethod
    def make_elements(num_points: int) -> list[Element]: ...

    @classmethod
    def new(cls, num_points: int, start: float = 0, end: float = 1) -> "Mesh":
        grid = np.linspace(start, end, num_points)

        points = np.array(list(product(grid, grid)))
        elements = cls.make_elements(num_points)

        return cls(
            shape=(num_points, num_points),
            points=points,
            elements=elements,
        )

    @property
    @abstractmethod
    def element_area(self) -> float: ...

    @property
    @abstractmethod
    def topological_dimension(self) -> str: ...


class QuadraticMesh(Mesh):
    @staticmethod
    def make_elements(num_points: int) -> list[tuple]:
        return [
            (
                num_points * i + j,
                num_points * i + j + 1,
                num_points * (i + 1) + j,
                num_points * (i + 1) + j + 1,
            )
            for i in range(num_points - 1)
            for j in range(num_points - 1)
        ]

    @cached_property
    def element_area(self) -> float:
        x_min, y_min = self.points[0]
        x_max, y_max = self.points[-1]
        return (x_max - x_min) / (self.shape[0] - 1) * (y_max - y_min) / (self.shape[1] - 1)

    @property
    def topological_dimension(self) -> str:
        return "quad"


class TriangularMesh(Mesh):
    @staticmethod
    def make_elements(num_points: int) -> list[Element]:
        elements = []
        for i in range(num_points - 1):
            for j in range(num_points - 1):
                elements.append(
                    (
                        num_points * i + j,
                        num_points * i + j + 1,
                        num_points * (i + 1) + j,
                    )
                )
                elements.append(
                    (
                        num_points * i + j + 1,
                        num_points * (i + 1) + j,
                        num_points * (i + 1) + j + 1,
                    )
                )
        return elements

    @cached_property
    def element_area(self) -> float:
        x_min, y_min = self.points[0]
        x_max, y_max = self.points[-1]
        return (x_max - x_min) / (self.shape[0] - 1) * (y_max - y_min) / (self.shape[1] - 1) / 2

    @property
    def topological_dimension(self) -> str:
        return "triangle"


def test_quadratic_mesh_generation():
    mesh_2 = QuadraticMesh.new(2)
    assert (mesh_2.points == [[0., 0.], [0., 1.], [1., 0.], [1., 1.]]).all()  # type: ignore
    assert mesh_2.elements == [(0, 1, 2, 3)]

    mesh_3 = QuadraticMesh.new(3, 0, 2)
    assert (  # type: ignore
        mesh_3.points == [
            [0., 0.], [0., 1.], [0., 2.],
            [1., 0.], [1., 1.], [1., 2.],
            [2., 0.], [2., 1.], [2., 2.],
        ]
    ).all()
    assert mesh_3.elements == [(0, 1, 3, 4), (1, 2, 4, 5), (3, 4, 6, 7), (4, 5, 7, 8)]


def test_triangular_mesh_generation():
    mesh_2 = TriangularMesh.new(2)
    assert (mesh_2.points == [[0., 0.], [0., 1.], [1., 0.], [1., 1.]]).all()  # type: ignore
    assert mesh_2.elements == [(0, 1, 2), (1, 2, 3)]

    mesh_3 = TriangularMesh.new(3, 0, 2)
    assert (  # type: ignore
            mesh_3.points == [
        [0., 0.], [0., 1.], [0., 2.],
        [1., 0.], [1., 1.], [1., 2.],
        [2., 0.], [2., 1.], [2., 2.],
    ]
    ).all()
    assert mesh_3.elements == [
        (0, 1, 3),
        (1, 3, 4),
        (1, 2, 4),
        (2, 4, 5),
        (3, 4, 6),
        (4, 6, 7),
        (4, 5, 7),
        (5, 7, 8),
    ]


def test_quadratic_mesh_element_area():
    assert np.isclose(QuadraticMesh.new(2).element_area, 1)
    assert np.isclose(QuadraticMesh.new(3).element_area, 1 / 4)
    assert np.isclose(QuadraticMesh.new(4).element_area, 1 / 9)


def test_triangular_mesh_element_area():
    assert np.isclose(TriangularMesh.new(2).element_area, 1 / 2)
    assert np.isclose(TriangularMesh.new(3).element_area, 1 / 8)
    assert np.isclose(TriangularMesh.new(4).element_area, 1 / 18)


if __name__ == "__main__":
    test_quadratic_mesh_generation()
    test_triangular_mesh_generation()
    test_quadratic_mesh_element_area()
    test_triangular_mesh_element_area()
