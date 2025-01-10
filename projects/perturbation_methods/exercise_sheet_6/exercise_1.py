from typing import Callable

import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import odeint

Field = np.ndarray
Funcs = tuple[Field, Field]
Initial = tuple[float, float]
System = Callable[[Funcs, Field], Funcs]
Func = Callable[[Field], Field]


def wkb_approx(*, eps: float) -> Func:
    def inner(x: Field) -> Field:
        return eps / np.sqrt(1 + x**2) * (np.exp((x + x**3 / 3) / eps) - np.exp(-(x + x**3 / 3) / eps))

    return inner


def ode_system(*, eps: float) -> System:
    def inner(yz: Funcs, x: Field) -> Funcs:
        y, z = yz
        return (
            z,
            (1 + x**2) ** 2 / eps**2 * y,
        )

    return inner


def solve(*, system: System, init: Initial, x: Field) -> Field:
    solution = odeint(system, init, x)
    return solution[:, 0]  # type: ignore


def main():
    init = 0.0, 1.0
    eps = 0.005
    x = np.linspace(0, 1, 1000000)

    system = ode_system(eps=eps)
    wkb = wkb_approx(eps=eps)

    y_odeint = solve(
        system=system,
        init=init,
        x=x,
    )
    y_wkb = wkb(x)

    plt.loglog(x, y_odeint, label="odeint")
    plt.loglog(x, y_wkb, label="wkb")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
