import numpy as np
from nptyping import NDArray

from projects.partial_differential_equations.domain import Domain
from projects.partial_differential_equations.uvp import UVP

"""
Considering the equations (Incompressible Navier-Stokes):
(1) u_t = 𝛎Δu - (u·∇)u - ∇p/ϱ + f
(2) ∇·u = 0

Taking the divergence of (1) and applying (2) we get
(1') u_t = 𝛎Δu - (u·∇)u - ∇p/ϱ + f
(2') Δp = ϱ(∇f - ∇·(u·∇)u)
which is known as the velocity-pressure formulation of the Navier-Stokes equations

In the computations we let vector(u) = (u, v), and
u = u(t, x, y)
v = v(t, x, y)
p = p(t, x, y)
"""


def main():
    domain = Domain.new((1000, 40, 40), (1, 2, 2))
    rho = 1.0
    nu = 0.01

    f = np.zeros(domain.shape.xy), np.zeros(domain.shape.xy)

    def u_bcs(u: NDArray, t: float, x: NDArray, y: NDArray):
        u[0, :] = 0
        u[:, 0] = (1 + np.sin(y - 40*t))[:, 0]
        u[:, -1] = -(y * (2 - y) * (1 - 0.5 * y))[:, -1]
        u[-1, :] = 0

        u[:, :] = np.where(
            np.logical_and(np.abs(x - 1) <= 0.5, np.abs(y - 1) <= 0.5),
            0,
            u,
        )

        u[:, :] = np.where(
            np.logical_and(np.abs(x - 1) <= 0.5, np.abs(y - 1) <= 0.5),
            0,
            u,
        )

    def v_bcs(v: NDArray, t: float, x: NDArray, y: NDArray):
        v[:, 0] = 0
        v[:, -1] = 0

        v[:, :] = np.where(
            np.logical_and(np.abs(x - 1) <= 0.3, np.abs(y - 1) <= 0.3),
            0,
            v,
        )

    def p_bcs(p: NDArray, t: float, x: NDArray, y: NDArray):
        p[:, 0] = 0
        p[:, -1] = 0

    UVP.initial(domain=domain).animate(
        f=f,
        u_bcs=u_bcs,
        v_bcs=v_bcs,
        p_bcs=p_bcs,
        filename="animation.gif",
        rho=rho,
        nu=nu,
    )


if __name__ == "__main__":
    main()
