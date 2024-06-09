import numpy as np
from nptyping import NDArray

from projects.partial_differential_equations.domain import Domain
from projects.partial_differential_equations.uvp import UVP


def u_true(x: NDArray, y: NDArray) -> NDArray:
    return np.ones_like(x)


def v_true(x: NDArray, y: NDArray) -> NDArray:
    return np.zeros_like(x)


def p_true(x: NDArray, y: NDArray) -> NDArray:
    return np.zeros_like(x)


def u_bcs(u: NDArray, x: NDArray, y: NDArray):
    vals = u_true(x, y)
    u[:, 0] = vals[:, 0]
    u[:, -1] = vals[:, -1]
    u[0, :] = u[1, :]
    u[-1, :] = u[-2, :]


def v_bcs(v: NDArray, x: NDArray, y: NDArray):
    vals = v_true(x, y)
    v[:, 0] = vals[:, 0]
    v[:, -1] = vals[:, -1]
    v[0, :] = vals[0, :]
    v[-1, :] = vals[-1, :]


def p_bcs(p: NDArray, x: NDArray, y: NDArray):
    vals = p_true(x, y)
    p[:, 0] = vals[:, 0]
    p[:, -1] = vals[:, -1]
    p[0, :] = vals[0, :]
    p[-1, :] = vals[-1, :]


def f(x: NDArray, y: NDArray) -> tuple[NDArray, NDArray]:
    return (
        np.zeros_like(x),
        np.zeros_like(x),
    )


all_errors: dict[str, list[float]] = {
    "u": [],
    "v": [],
    "p": [],
}
for shape in [
    (100, 5, 5),
    (200, 10, 10),
    (400, 20, 20),
    (800, 40, 40),
    (1600, 80, 80),
    (3200, 160, 160),
]:
    print(f"{shape=}")
    domain = Domain.new(shape, max_vals=(0.01, 1, 1))
    f_vals = f(domain.x, domain.y)

    u_true_vals = u_true(domain.x, domain.y)
    v_true_vals = v_true(domain.x, domain.y)
    p_true_vals = p_true(domain.x, domain.y)

    uvp = UVP.initial(
        domain=domain,
        u=lambda x, y: 0.997 * np.ones_like(x),  # checking if it falls back to 1 over time
        v=v_true,
        p=p_true,
    )
    errors: dict[str, list[float]] = {
        "u": [],
        "v": [],
        "p": [],
    }
    for step in range(uvp.domain.shape.t):
        uvp = uvp.solve_for_next_uvp(f_vals, u_bcs, v_bcs, p_bcs)

    all_errors["u"].append(np.linalg.norm(uvp.u - u_true_vals))
    all_errors["v"].append(np.linalg.norm(uvp.v - v_true_vals))
    all_errors["p"].append(np.linalg.norm(uvp.p - p_true_vals))

print(all_errors["u"])
print(all_errors["v"])
print(all_errors["p"])
