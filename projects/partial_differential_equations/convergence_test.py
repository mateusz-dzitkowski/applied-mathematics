from matplotlib import pyplot as plt
import numpy as np
from nptyping import NDArray

from projects.partial_differential_equations.domain import Domain
from projects.partial_differential_equations.uvp import UVP

"""
"inspired" by
https://www.researchgate.net/publication/244990017_On_Consistency_of_Finite_Difference_Approximations_to_the_Navier-Stokes_Equations
"""

NU = 10**-7


def u_true(t: float, x: NDArray, y: NDArray) -> NDArray:
    return -np.exp(-2 * NU * t) * np.cos(x) * np.sin(y)


def v_true(t: float, x: NDArray, y: NDArray) -> NDArray:
    return np.exp(-2 * NU * t) * np.sin(x) * np.cos(y)


def p_true(t: float, x: NDArray, y: NDArray) -> NDArray:
    return -np.exp(-4 * NU * t) * (np.cos(2 * x) + np.cos(2 * y)) / 4


def u_bcs(u: NDArray, t: float, x: NDArray, y: NDArray):
    vals = u_true(t, x, y)
    u[:, 0] = vals[:, 0]
    u[:, -1] = vals[:, -1]
    u[0, :] = vals[0, :]
    u[-1, :] = vals[-1, :]


def v_bcs(v: NDArray, t: float, x: NDArray, y: NDArray):
    vals = v_true(t, x, y)
    v[:, 0] = vals[:, 0]
    v[:, -1] = vals[:, -1]
    v[0, :] = vals[0, :]
    v[-1, :] = vals[-1, :]


def p_bcs(p: NDArray, t: float, x: NDArray, y: NDArray):
    vals = p_true(t, x, y)
    p[:, 0] = vals[:, 0]
    p[:, -1] = vals[:, -1]
    p[0, :] = vals[0, :]
    p[-1, :] = vals[-1, :]


def error(f: NDArray, g: NDArray) -> float:
    return np.max(np.abs(f - g) / (1 + np.abs(g)))


all_errors: dict[str, list[float]] = {
    "u": [],
    "v": [],
    "p": [],
}
num_points_list = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
for shape in [(100, num, num) for num in num_points_list]:
    print(f"{shape=}")
    domain = Domain.new(shape, max_vals=(1, np.pi, np.pi))

    uvp = (
        UVP.new(domain=domain)
        .with_initial_conditions(
            u=u_true(0, domain.x, domain.y),
            v=v_true(0, domain.x, domain.y),
            p=p_true(0, domain.x, domain.y),
        )
        .with_boundary_conditions(
            u_bcs=u_bcs,
            v_bcs=v_bcs,
            p_bcs=p_bcs,
        )
        .with_parameters(nu=NU)
    )

    for step in range(uvp.domain.shape.t - 1):
        uvp.solve_for_next_uvp(inplace=True)

    all_errors["u"].append(error(uvp.u, u_true(uvp.t, domain.x, domain.y)))
    all_errors["v"].append(error(uvp.v, v_true(uvp.t, domain.x, domain.y)))
    all_errors["p"].append(error(uvp.p, p_true(uvp.t, domain.x, domain.y)))

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(num_points_list, all_errors["u"], label="u")
ax.plot(num_points_list, all_errors["v"], label="v")
ax.plot(num_points_list, all_errors["p"], label="p")
ax.set_yscale("log")
ax.legend()
ax.grid()
ax.set_xlabel("n")
ax.set_ylabel("error")
plt.show()
