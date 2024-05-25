from abc import ABC
from dataclasses import dataclass
from itertools import product

from nptyping import NDArray

import numpy as np


@dataclass
class Mesh(ABC):
    points: NDArray
    elements: NDArray

    @staticmethod
    def make_elements(num_points: int) -> NDArray: ...

    @classmethod
    def new(cls, num_points: int, start: float = 0, end: float = 1) -> "Mesh":
        grid = np.linspace(start, end, num_points)

        points = np.array(list(product(grid, grid)))
        elements = cls.make_elements(num_points)

        return Mesh(points=points, elements=elements)


class QuadraticMesh(Mesh):
    @staticmethod
    def make_elements(num_points: int) -> NDArray:
        return np.array([
            [
                num_points * i + j,
                num_points * i + j + 1,
                num_points * (i + 1) + j,
                num_points * (i + 1) + j + 1,
            ]
            for i in range(num_points - 1)
            for j in range(num_points - 1)
        ])


class TriangularMesh(Mesh):
    @staticmethod
    def make_elements(num_points: int) -> NDArray:
        return np.array(
            [
                [
                    [
                        num_points * i + j,
                        num_points * i + j + 1,
                        num_points * (i + 1) + j,
                    ],  # lower triangle
                    [
                        num_points * i + j + 1,
                        num_points * (i + 1) + j,
                        num_points * (i + 1) + j + 1,
                    ],  # upper triangle
                ]
                for i in range(num_points - 1)
                for j in range(num_points - 1)
            ]
        ).reshape((2 * (num_points - 1)**2, 3))


def test_quadratic_mesh_generation():
    mesh_2 = QuadraticMesh.new(2)
    assert (mesh_2.points == [[0., 0.], [0., 1.], [1., 0.], [1., 1.]]).all()  # type: ignore
    assert (mesh_2.elements == [[0, 1, 2, 3]]).all()  # type: ignore

    mesh_3 = QuadraticMesh.new(3, 0, 2)
    assert (  # type: ignore
        mesh_3.points == [
            [0., 0.], [0., 1.], [0., 2.],
            [1., 0.], [1., 1.], [1., 2.],
            [2., 0.], [2., 1.], [2., 2.],
        ]
    ).all()
    assert (mesh_3.elements == [[0, 1, 3, 4], [1, 2, 4, 5], [3, 4, 6, 7], [4, 5, 7, 8]]).all()  # type: ignore


def test_triangular_mesh_generation():
    mesh_2 = TriangularMesh.new(2)
    assert (mesh_2.points == [[0., 0.], [0., 1.], [1., 0.], [1., 1.]]).all()  # type: ignore
    assert (mesh_2.elements == [[0, 1, 2], [1, 2, 3]]).all()  # type: ignore

    mesh_3 = TriangularMesh.new(3, 0, 2)
    assert (  # type: ignore
            mesh_3.points == [
        [0., 0.], [0., 1.], [0., 2.],
        [1., 0.], [1., 1.], [1., 2.],
        [2., 0.], [2., 1.], [2., 2.],
    ]
    ).all()
    assert (  # type: ignore
        mesh_3.elements == [
            [0, 1, 3],
            [1, 3, 4],
            [1, 2, 4],
            [2, 4, 5],
            [3, 4, 6],
            [4, 6, 7],
            [4, 5, 7],
            [5, 7, 8],
        ]
    ).all()


if __name__ == "__main__":
    test_quadratic_mesh_generation()
    test_triangular_mesh_generation()
