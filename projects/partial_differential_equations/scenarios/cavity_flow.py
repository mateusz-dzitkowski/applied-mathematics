import numpy as np
from nptyping import NDArray

from projects.partial_differential_equations.domain import Domain
from projects.partial_differential_equations.uvp import UVP


def u_bcs(u: NDArray, t: float, x: NDArray, y: NDArray):
    u[0, :] = 0
    u[-1, :] = 2
    u[:, 0] = 0
    u[:, -1] = 0


def v_bcs(v: NDArray, t: float, x: NDArray, y: NDArray):
    v[0, :] = 0
    v[-1, :] = 0
    v[:, 0] = 0
    v[:, -1] = 0


def p_bcs(p: NDArray, t: float, x: NDArray, y: NDArray):
    p[0, :] = p[1, :]
    p[-1, :] = 0
    p[:, 0] = p[:, 1]
    p[:, -1] = p[:, -2]


(
    UVP.new(domain=Domain.new((10000, 100, 100), (3, 1, 1)))
    .with_boundary_conditions(
        u_bcs=u_bcs,
        v_bcs=v_bcs,
        p_bcs=p_bcs,
    )
    .with_parameters(
        rho=1.0,
        nu=0.001,
    )
    .animate(
        filename="cavity_flow.gif",
    )
)
