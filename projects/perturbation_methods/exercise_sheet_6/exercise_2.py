from typing import Callable

import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import solve_bvp

Field = np.ndarray
Funcs = tuple[Field, Field]
Point = tuple[float, float]
System = Callable[[Field, Funcs], Funcs]
Func = Callable[[Field], Field]
BCs = Callable[[Point, Point], Field]


def ode_system(*, lam: float) -> System:
    def inner(_x: Field, yz: Funcs) -> Funcs:
        y, z = yz
        return (
            z,
            -lam * (np.pi + _x) ** 4 * y,
        )

    return inner


def bc(yz_a: Point, yz_b: Point) -> Field:
    return np.array([yz_a[0], yz_b[0]])


def solve(system: System, bcs: BCs, x: Field) -> Field:
    return solve_bvp(system, bcs, x, np.vstack((x, x))).y[0]  # type: ignore


def main():
    n = 13
    lam = (3 * n / 7 / np.pi**2) ** 2

    x = np.linspace(0, np.pi, 10000)
    y = solve(
        system=ode_system(lam=lam),
        bcs=bc,
        x=x,
    )

    wkb = np.pi / (np.pi + x) * np.sin(np.sqrt(lam) * (np.pi**2 * x + np.pi * x**2 + x**3 / 3))
    y_scaled = y / y.max() * wkb.max()

    plt.plot(x, y_scaled, label="odeint")
    plt.plot(x, wkb, label="wkb")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
