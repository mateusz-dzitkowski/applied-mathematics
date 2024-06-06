from dataclasses import dataclass
from itertools import product

from nptyping import NDArray

import numpy as np
from types import SimpleNamespace as SN
from scipy.sparse import csr_matrix as sparse
from scipy.sparse.linalg import spsolve
import meshio


def hexahedron(points):
    r, s, t = points
    a = np.array([[-1, 1, 1, -1, -1, 1, 1, -1]]).T
    b = np.array([[-1, -1, 1, 1, -1, -1, 1, 1]]).T
    c = np.array([[-1, -1, -1, -1, 1, 1, 1, 1]]).T
    ar, bs, ct = 1 + a * r, 1 + b * s, 1 + c * t
    gradient = np.stack([a * bs * ct, ar * b * ct, ar * bs * c], axis=1)
    return SN(function=ar * bs * ct / 8, gradient=gradient / 8)


def Domain(mesh, Element, quadrature):
    element = Element(quadrature.points)
    dXdr = np.einsum("cpi,pjq->ijcq", mesh.points[mesh.cells], element.gradient)
    drdX = np.linalg.inv(dXdr.T).T
    return SN(
        mesh=mesh,
        element=element,
        gradient=np.einsum("piq,ijcq->pjcq", element.gradient, drdX),
        dx=quadrature.weights * np.linalg.det(dXdr.T).T,
    )


def VectorField(region, values):
    def grad(values):
        return np.einsum("cpi,pjcq->ijcq", values[region.mesh.cells], region.gradient)

    return SN(region=region, values=values, gradient=grad)


def Assemble(field, lmbda, mu):
    sym = lambda x: (x + np.einsum("ij...->ji...", x)) / 2
    ddot = lambda x, y: np.einsum("ij...,ij...->...", x, y)

    dhdX = field.region.gradient[..., None, None]
    dudX = field.gradient(field.values)
    dV = field.region.dx
    de = sym(np.einsum("im,aj...bn->ijambn...", np.eye(3), dhdX))
    De = sym(np.einsum("in,bj...am->ijambn...", np.eye(3), dhdX))
    e = sym(dudX)[:, :, None, None, None, None, ...]

    def linear_elastic(_de, _e):
        return 2 * mu * ddot(_de, _e) + lmbda * np.trace(_de) * np.trace(_e)

    vector = linear_elastic(de, e) * dV
    matrix = linear_elastic(de, De) * dV

    idx = 3 * np.repeat(mesh.cells, 3) + np.tile(np.arange(3), mesh.cells.size)
    idx = idx.reshape(*mesh.cells.shape, 3)
    vidx = (idx.ravel(), np.zeros_like(idx.ravel()))
    midx = (
        np.repeat(idx, 3 * idx.shape[1]),
        np.tile(idx, (1, idx.shape[1] * 3, 1)).ravel(),
    )
    return SN(
        vector=sparse((vector.sum(-1).transpose([4, 0, 1, 2, 3]).ravel(), vidx)),
        matrix=sparse((matrix.sum(-1).transpose([4, 0, 1, 2, 3]).ravel(), midx)),
    )


mesh = Mesh.new(num_points=50, start=1, end=3)
quadrature = SN(
    points=np.concatenate(np.meshgrid([-1, 1], [-1, 1])).reshape(2, -1) / np.sqrt(3),
    weights=np.ones(8),
)
region = Domain(mesh, hexahedron, quadrature)
field = VectorField(region, values=np.zeros_like(mesh.points))

extforce = np.zeros_like(mesh.points)
extforce[:, 0][mesh.points[:, 0] == 5] = -3 ** 2 / 4 / 16 ** 2

dofs = np.arange(mesh.points.size).reshape(mesh.points.shape)
dof = SN(fixed=dofs[mesh.points[:, 0] == 2].ravel())
dof.active = np.delete(dofs.ravel(), dof.fixed)

b = extforce.ravel()[dof.active]
for iteration in range(8):
    system = Assemble(field, lmbda=1.0, mu=2.0)
    A = system.matrix[dof.active, :][:, dof.active]
    field.values.ravel()[dof.active] += spsolve(A, b).ravel()
    b = (extforce.ravel() - system.vector.toarray().ravel())[dof.active]
    norm = np.linalg.norm(b)
    print(f"Iteration {iteration + 1} | norm(force)={norm:1.2e}")
    if norm < np.sqrt(np.finfo(float).eps):
        break

meshio.Mesh(
    mesh.points, [("hexahedron", mesh.cells)], point_data={"displacement": field.values}
).write("result.vtk")


