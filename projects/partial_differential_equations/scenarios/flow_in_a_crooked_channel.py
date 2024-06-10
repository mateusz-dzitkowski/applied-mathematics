import numpy as np
from nptyping import NDArray

from projects.partial_differential_equations.domain import Domain
from projects.partial_differential_equations.uvp import UVP


def u_bcs(u: NDArray, t: float, x: NDArray, y: NDArray):
    u[0, :] = u[-1, :] = 0
    u[:, 0] = (3 * 1.5 * y * (0.41 - y) / 0.41 ** 2)[:, 0]

    u[:, :] = np.where(
        np.sqrt((x - 0.2) ** 2 + (y - 0.2) ** 2) < 0.05,
        0,
        u
    )


def v_bcs(v: NDArray, t: float, x: NDArray, y: NDArray):
    v[0, :] = v[-1, :] = 0

    v[:, :] = np.where(
        np.sqrt((x - 0.2) ** 2 + (y - 0.2) ** 2) < 0.05,
        0,
        v
    )


def p_bcs(p: NDArray, t: float, x: NDArray, y: NDArray):
    p[:, -1] = 0


(
    UVP.new(domain=Domain.new((10000, 100, 50), (10, 1, 0.41)))
    .with_boundary_conditions(
        u_bcs=u_bcs,
        v_bcs=v_bcs,
        p_bcs=p_bcs,
    )
    .with_parameters(
        rho=1.0,
        nu=0.005,
    )
    .animate(
        filename="flow_past_a_cylinder.gif",
    )
)
