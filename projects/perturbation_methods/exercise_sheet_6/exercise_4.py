from typing import Callable

import numpy as np
from matplotlib import pyplot as plt
from scipy.constants import hbar, pi
from scipy.integrate import solve_bvp

Field = np.ndarray
Funcs = tuple[Field, Field]
Point = tuple[float, float]
System = Callable[[Field, Funcs], Funcs]
Func = Callable[[Field], Field]
BCs = Callable[[Point, Point], Field]


def ode_system(*, m: float, e: float) -> System:
    def inner(_x: Field, psi_phi: Funcs) -> Funcs:
        psi, phi = psi_phi
        return (
            phi,
            -2 * m * e / hbar**2 * psi,
        )

    return inner


def bc(psi_phi_a: Point, psi_phi_b: Point) -> Field:
    return np.array([psi_phi_a[0], psi_phi_b[0]])


def solve(system: System, bcs: BCs, x: Field) -> Field:
    return solve_bvp(system, bcs, x, np.vstack((x, x))).y[0]  # type: ignore


def main():
    a = 1
    n = 10
    m = 10

    e = (n * pi * hbar / a) ** 2 / (2 * m)
    x = np.linspace(0, a, 10000)
    psi = solve(
        system=ode_system(m=m, e=e),
        bcs=bc,
        x=x,
    )
    psi_minmax = psi / psi.max()
    int_psi = (np.abs(psi_minmax) ** 2).sum() * a * np.diff(x)[0]
    psi_scaled = psi_minmax / int_psi

    wkb = np.sin(np.sqrt(2 * m * e) / hbar * x)
    int_wkb = (np.abs(wkb) ** 2).sum() * a * np.diff(x)[0]
    wkb_scaled = wkb / int_wkb

    plt.plot(x, psi_scaled, label="odeint")
    plt.plot(x, wkb_scaled, label="wkb")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
