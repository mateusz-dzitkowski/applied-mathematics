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
    def u_bcs(u: NDArray, t: float, x: NDArray, y: NDArray):
        u[0, :] = u[-1, :] = 0
        u[:, 0] = (4 * 1.5 * y * (0.41 - y) / 0.41**2)[:, 0]

        u[:, :] = np.where(
            np.sqrt((x - 0.2)**2 + (y - 0.2)**2) < 0.05,
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

    domain = Domain.new((5000, 100, 50), (5, 1, 0.41))
    (
        UVP.new(domain=domain)
        .with_boundary_conditions(
            u_bcs=u_bcs,
            v_bcs=v_bcs,
            p_bcs=p_bcs,
        )
        .with_parameters(
            rho=1.0,
            nu=0.001,
        )
        .animate(filename="animation.mp4")
    )


if __name__ == "__main__":
    main()
