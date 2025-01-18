from typing import Callable

import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import odeint

Field = np.ndarray
Funcs = tuple[Field, Field]
Initial = tuple[float, float]
System = Callable[[Funcs, Field], Funcs]
Func = Callable[[Field], Field]


def wkb_approx(*, lam: float) -> Func:
    def inner(x: Field) -> Field:
        return 1 / 2 / np.sqrt(lam) / np.sqrt(1 + x**2) * (np.exp(np.sqrt(lam) * (x + x**3 / 3)) - np.exp(-np.sqrt(lam) * (x + x**3 / 3)))

    return inner


def ode_system(*, lam: float) -> System:
    def inner(yz: Funcs, x: Field) -> Funcs:
        y, z = yz
        return (
            z,
            (1 + x**2) ** 2 * lam * y,
        )

    return inner


def solve(*, system: System, init: Initial, x: Field) -> Field:
    solution = odeint(system, init, x)
    return solution[:, 0]  # type: ignore


def main():
    init = 0.0, 1.0
    lam = 100000
    x = np.linspace(0, 0.5, 100000)

    system = ode_system(lam=lam)
    wkb = wkb_approx(lam=lam)

    y_odeint = solve(
        system=system,
        init=init,
        x=x,
    )
    y_wkb = wkb(x)

    plt.loglog(x, y_odeint, label="odeint")
    plt.loglog(x, y_wkb, label="wkb")
    # plt.loglog(x, y_odeint - y_wkb, label="difference")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
