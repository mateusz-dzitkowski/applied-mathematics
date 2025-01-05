from typing import Callable

from matplotlib import pyplot as plt
import numpy as np
from scipy.integrate import solve_bvp
from scipy.constants import hbar, pi


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
            -2*m*e/hbar**2 * psi,
        )
    return inner


def bc(psi_phi_a: Point, psi_phi_b: Point) -> Field:
    return np.array([psi_phi_a[0], psi_phi_b[0]])


def solve(system: System, bcs: BCs, x: Field) -> Field:
    return solve_bvp(system, bcs, x, np.zeros((2, x.size)))  # type: ignore


def main():
    a = 1
    n = 1
    m = 1

    e = (n + 1/2)**2 * hbar**4 * pi**2 / (2*m*a**2)
    x = np.linspace(0, a, 100)
    psi = solve(
        system=ode_system(m=m, e=e),
        bcs=bc,
        x=x,
    )
    print(psi)


if __name__ == "__main__":
    main()
