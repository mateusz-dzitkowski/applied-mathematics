from dataclasses import dataclass
from typing import Callable

import numpy as np
from nptyping import NDArray

from projects.partial_differential_equations.domain import Domain


FunctionXY = Callable[[NDArray, NDArray], ...]
BoundaryConditions = Callable[[NDArray, NDArray, NDArray], ...]  # for now assume that BCs are time-independent


@dataclass
class UVP:
    u: NDArray  # x component of velocity
    v: NDArray  # y component of velocity
    p: NDArray  # pressure
    domain: Domain

    @classmethod
    def initial(
        cls,
        domain: Domain,
        u: FunctionXY = lambda x, y: 0 * x,  # just 0 would return a float
        v: FunctionXY = lambda x, y: 0 * x,
        p: FunctionXY = lambda x, y: 0 * x,
    ) -> "UVP":
        x = domain.x
        y = domain.y
        return cls(
            u=u(x, y),
            v=v(x, y),
            p=p(x, y),
            domain=domain,
        )

    def __iter__(self):
        return iter((self.u, self.v, self.p))

    def build_pressure_equation_rhs(
        self,
        f: tuple[NDArray, NDArray],
        rho: float,
    ) -> NDArray:
        u, v, _ = self
        dt, dx, dy = self.domain.diff
        f_x, f_y = f

        rhs = np.zeros(self.domain.shape.xy)
        rhs[1:-1, 1:-1] = rho * (
            (f_x[1:-1, 2:] - f_x[1:-1, 0:-2]) / (2 * dx)
            + (f_y[2:, 1:-1] - f_y[0:-2, 1:-1]) / (2 * dy)
            + (
                (u[1:-1, 2:] - u[1:-1, 0:-2]) / (2 * dx)
                + (v[2:, 1:-1] - v[0:-2, 1:-1]) / (2 * dy)
            ) / dt
            - 2 * (
                (u[2:, 1:-1] - u[0:-2, 1:-1]) / (2 * dy)
                * (v[1:-1, 2:] - v[1:-1, 0:-2]) / (2 * dx)
            )
            - ((u[1:-1, 2:] - u[1:-1, 0:-2]) / (2 * dx))**2
            - ((v[2:, 1:-1] - v[0:-2, 1:-1]) / (2 * dy))**2
        )
        return rhs

    def solve_for_pressure(
        self,
        f: tuple[NDArray, NDArray],
        apply_boundary_conditions: BoundaryConditions,
        rho: float = 1,
        num_iterations: int = 10,
    ) -> NDArray:
        rhs = self.build_pressure_equation_rhs(f, rho)
        _, dx, dy = self.domain.diff

        p_next = None
        p_previous = self.p.copy()
        for _ in range(num_iterations):
            p_next = p_previous.copy()
            p_next[1:-1, 1:-1] = (
                (
                    (p_previous[1:-1, 2:] + p_previous[1:-1, 0:-2]) * dy**2
                    + (p_previous[2:, 1:-1] + p_previous[0:-2, 1:-1]) * dx**2
                ) / (2 * (dx**2 + dy**2)) -
                dx**2 * dy**2 / (2 * (dx**2 + dy**2)) * rhs[1:-1, 1:-1]
            )

            apply_boundary_conditions(p_next, self.domain.x, self.domain.y)

        return p_next

    def solve_for_u(
        self,
        f: tuple[NDArray, NDArray],
        p_new: NDArray,
        apply_boundary_conditions: BoundaryConditions,
        rho: float = 1,
        nu: float = 1,
    ) -> NDArray:
        u_old, v_old, _ = self
        dt, dx, dy = self.domain.diff
        u_new = np.zeros_like(u_old)

        u_new[1:-1, 1:-1] = (
            u_old[1:-1, 1:-1]
            - u_old[1:-1, 1:-1] * dt / dx * (u_old[1:-1, 1:-1] - u_old[1:-1, 0:-2])
            - v_old[1:-1, 1:-1] * dt / dy * (u_old[1:-1, 1:-1] - u_old[0:-2, 1:-1])
            - dt / (2 * rho * dx) * (p_new[1:-1, 2:] - p_new[1:-1, 0:-2])
            + nu * (
                dt / dx ** 2 * (u_old[1:-1, 2:] - 2 * u_old[1:-1, 1:-1] + u_old[1:-1, 0:-2])
                + dt / dy ** 2 * (u_old[2:, 1:-1] - 2 * u_old[1:-1, 1:-1] + u_old[0:-2, 1:-1])
            )
            + dt * f[0][1:-1, 1:-1]
        )

        apply_boundary_conditions(u_new, self.domain.x, self.domain.y)

        return u_new

    def solve_for_v(
        self,
        f: tuple[NDArray, NDArray],
        p_new: NDArray,
        apply_boundary_conditions: BoundaryConditions,
        rho: float = 1,
        nu: float = 1,
    ) -> NDArray:
        u_old, v_old, _ = self
        dt, dx, dy = self.domain.diff

        v_new = np.zeros_like(v_old)
        v_new[1:-1, 1:-1] = (
            v_old[1:-1, 1:-1]
            - u_old[1:-1, 1:-1] * dt / dx * (v_old[1:-1, 1:-1] - v_old[1:-1, 0:-2])
            - v_old[1:-1, 1:-1] * dt / dy * (v_old[1:-1, 1:-1] - v_old[0:-2, 1:-1])
            - dt / (2 * rho * dy) * (p_new[2:, 1:-1] - p_new[0:-2, 1:-1])
            + nu * (
                dt / dx**2 * (v_old[1:-1, 2:] - 2 * v_old[1:-1, 1:-1] + v_old[1:-1, 0:-2])
                + dt / dy**2 * (v_old[2:, 1:-1] - 2 * v_old[1:-1, 1:-1] + v_old[0:-2, 1:-1])
            )
            + dt * f[1][1:-1, 1:-1]
        )

        apply_boundary_conditions(v_new, self.domain.x, self.domain.y)

        return v_new

    def solve_for_next_uvp(
        self,
        f: tuple[NDArray, NDArray],
        u_bcs: BoundaryConditions,
        v_bcs: BoundaryConditions,
        p_bcs: BoundaryConditions,
        rho: float = 1,
        nu: float = 1,
    ) -> "UVP":
        p_new = self.solve_for_pressure(f, p_bcs, rho)
        u_new = self.solve_for_u(f, p_new, u_bcs, rho, nu)
        v_new = self.solve_for_v(f, p_new, v_bcs, rho, nu)
        return UVP(
            u=u_new,
            v=v_new,
            p=p_new,
            domain=self.domain,
        )