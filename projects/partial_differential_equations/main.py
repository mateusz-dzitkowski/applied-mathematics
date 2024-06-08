import numpy as np
from nptyping import NDArray
from matplotlib import (
    cm,
    pyplot as plt
)

from projects.partial_differential_equations.domain import Domain
from projects.partial_differential_equations.solution import UVP

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
    domain = Domain.new((500, 41, 41), (0.5, 2, 2))
    rho = 1.0
    nu = 0.1

    f = np.zeros(domain.shape.xy), np.zeros(domain.shape.xy)

    def u_bcs(u: NDArray, _: NDArray, __: NDArray):
        u[0, :] = 0
        u[:, 0] = 0
        u[:, -1] = 0
        u[-1, :] = 1

    def v_bcs(v: NDArray, _: NDArray, __: NDArray):
        v[0, :] = 0
        v[:, 0] = 0
        v[:, -1] = 0
        v[-1, :] = 0

    def p_bcs(p: NDArray, _: NDArray, __: NDArray):
        p[:, -1] = p[:, -2]
        p[0, :] = p[1, :]
        p[:, 0] = p[:, 1]
        p[-1, :] = 0

    uvp = UVP.initial(domain=domain)

    for step in range(uvp.domain.shape.t):
        print(step)
        uvp = uvp.solve_for_next_uvp(f, u_bcs, v_bcs, p_bcs, rho, nu)

    fig = plt.figure(figsize=(11, 7), dpi=100)
    plt.contourf(domain.x, domain.y, uvp.p, alpha=0.5, cmap=cm.viridis)
    plt.colorbar()
    plt.contour(domain.x, domain.y, uvp.p, cmap=cm.viridis)
    plt.streamplot(domain.x, domain.y, uvp.u, uvp.v)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()


if __name__ == "__main__":
    main()
