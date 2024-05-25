from abc import ABC, abstractmethod
from dataclasses import dataclass

import matplotlib.pyplot as plt
import scipy.sparse as sp
import numpy as np
from nptyping import NDArray
import scipy.sparse.linalg as spla

from projects.partial_differential_equations.mesh import Mesh, TriangularMesh


@dataclass
class Solution:
    mesh: Mesh
    values: NDArray

    def plot(self):
        x = self.mesh.points[:, 0].reshape(self.mesh.shape)
        y = self.mesh.points[:, 1].reshape(self.mesh.shape)
        u = self.values.reshape(self.mesh.shape)

        plt.contourf(x, y, u, 20, cmap="viridis")
        plt.show()


@dataclass
class LinearSystem(ABC):
    mesh: Mesh
    stiffness_matrix: sp.spmatrix
    load_vector: NDArray

    @classmethod
    @abstractmethod
    def assemble(cls, mesh: Mesh) -> "LinearSystem": ...

    @abstractmethod
    def with_boundary_conditions(self) -> "LinearSystem": ...

    def solve(self) -> Solution:
        return Solution(
            mesh=self.mesh,
            values=spla.spsolve(self.stiffness_matrix.tocsr(), self.load_vector),
        )


class PoissonLinearSystem(LinearSystem):
    # chatgpt for the win

    @staticmethod
    def f(x: NDArray, y: NDArray):
        return np.sin(np.pi * x) * np.sin(np.pi * y)

    @classmethod
    def assemble(cls, mesh: Mesh) -> "LinearSystem":
        n_nodes = mesh.points.shape[0]
        matrix = sp.lil_matrix((n_nodes, n_nodes))
        vector = np.zeros(n_nodes)
        area = mesh.element_area

        for elem in mesh.elements:
            x = mesh.points[elem, 0]
            y = mesh.points[elem, 1]

            # Gradients of the basis functions
            grad_phi = np.array([
                [y[1] - y[2], y[2] - y[0], y[0] - y[1]],
                [x[2] - x[1], x[0] - x[2], x[1] - x[0]]
            ]) / (2 * area)

            # Local stiffness matrix
            local_A = area * (grad_phi.T @ grad_phi)

            # Local load vector
            mid_x = np.mean(x)
            mid_y = np.mean(y)
            local_b = area * cls.f(mid_x, mid_y) / 3

            for i in range(3):
                vector[elem[i]] += local_b
                for j in range(3):
                    matrix[elem[i], elem[j]] += local_A[i, j]

        return PoissonLinearSystem(mesh=mesh, stiffness_matrix=matrix, load_vector=vector)

    def with_boundary_conditions(self) -> "LinearSystem":
        boundary_nodes = np.where(
            (self.mesh.points[:, 0] == 0)
            | (self.mesh.points[:, 0] == 1)
            | (self.mesh.points[:, 1] == 0)
            | (self.mesh.points[:, 1] == 1)
        )[0]

        for bn in boundary_nodes:
            self.stiffness_matrix[bn, :] = 0
            self.stiffness_matrix[bn, bn] = 1
            self.load_vector[bn] = 0

        return self


if __name__ == "__main__":
    (
        PoissonLinearSystem
        .assemble(TriangularMesh.new(50))
        .with_boundary_conditions()
        .solve()
        .plot()
    )
