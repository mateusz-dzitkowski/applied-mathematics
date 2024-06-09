from dataclasses import dataclass
from typing import Callable, Self

from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib import (
    animation,
    cm,
    pyplot as plt,
)
import numpy as np
from nptyping import NDArray

from projects.partial_differential_equations.domain import Domain


FunctionXY = Callable[[NDArray, NDArray], ...]
BoundaryConditions = Callable[[NDArray, float, NDArray, NDArray], ...]


def d_dx(values: NDArray, dx: float) -> NDArray:
    # first derivative wrt x
    return (values[1:-1, 2:] - values[1:-1, 0:-2]) / (2 * dx)


def d2_dx2(values: NDArray, dx: float) -> NDArray:
    # second derivative wrt x
    return (values[1:-1, 2:] - 2 * values[1:-1, 1:-1] + values[1:-1, 0:-2]) / dx**2


def d_dy(values: NDArray, dy: float) -> NDArray:
    # first derivative wrt y
    return (values[2:, 1:-1] - values[0:-2, 1:-1]) / (2 * dy)


def d2_dy2(values: NDArray, dy: float) -> NDArray:
    # second derivative wrt y
    return (values[2:, 1:-1] - 2 * values[1:-1, 1:-1] + values[0:-2, 1:-1]) / dy**2


@dataclass
class UVP:
    u: NDArray  # x component of velocity
    v: NDArray  # y component of velocity
    p: NDArray  # pressure
    domain: Domain
    current_step: int

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
            current_step=0,
        )

    def __iter__(self):
        return iter((self.u, self.v, self.p))

    @property
    def t(self) -> float:
        return self.domain.t[self.current_step]  # type: ignore

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
            d_dx(f_x, dx)
            + d_dy(f_y, dy)
            + (d_dx(u, dx) + d_dy(v, dy)) / dt
            - 2 * d_dy(u, dy) * d_dx(v, dx)
            - d_dx(u, dx)**2
            - d_dy(v, dy)**2
        )
        return rhs

    def solve_for_pressure(
        self,
        f: tuple[NDArray, NDArray],
        apply_boundary_conditions: BoundaryConditions,
        rho: float = 1,
        num_iterations: int = 100,
    ) -> NDArray:
        rhs = self.build_pressure_equation_rhs(f, rho)
        _, dx, dy = self.domain.diff

        p_next = None
        p_previous = self.p.copy()
        for _ in range(num_iterations):
            p_next = p_previous.copy()

            p_next[1:-1, 1:-1] = (
                (p_previous[1:-1, 2:] + p_previous[1:-1, 0:-2]) * dx**2
                + (p_previous[2:, 1:-1] + p_previous[0:-2, 1:-1]) * dy**2
                - rhs[1:-1, 1:-1] * dx**2 * dy**2
            ) / (2 * (dx**2 + dy**2))

            apply_boundary_conditions(p_next, self.t, self.domain.x, self.domain.y)

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
            + dt * (
                - u_old[1:-1, 1:-1] * d_dx(u_old, dx)
                - v_old[1:-1, 1:-1] * d_dy(u_old, dy)
                - d_dx(p_new, dx) / rho
                + nu * (d2_dx2(u_old, dx) + d2_dy2(u_old, dy))
                + f[0][1:-1, 1:-1]
            )
        )

        apply_boundary_conditions(u_new, self.t, self.domain.x, self.domain.y)

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
            + dt * (
                - u_old[1:-1, 1:-1] * d_dx(v_old, dx)
                - v_old[1:-1, 1:-1] * d_dy(v_old, dy)
                - d_dy(p_new, dy) / rho
                + nu * (d2_dx2(v_old, dx) + d2_dy2(v_old, dy))
                + f[1][1:-1, 1:-1]
            )
        )

        apply_boundary_conditions(v_new, self.t, self.domain.x, self.domain.y)

        return v_new

    def solve_for_next_uvp(
        self,
        f: tuple[NDArray, NDArray],
        u_bcs: BoundaryConditions,
        v_bcs: BoundaryConditions,
        p_bcs: BoundaryConditions,
        rho: float = 1,
        nu: float = 1,
        inplace: bool = False,
    ) -> Self | None:
        p_new = self.solve_for_pressure(f, p_bcs, rho)
        u_new = self.solve_for_u(f, p_new, u_bcs, rho, nu)
        v_new = self.solve_for_v(f, p_new, v_bcs, rho, nu)

        uvp_new = UVP(
            u=u_new,
            v=v_new,
            p=p_new,
            domain=self.domain,
            current_step=self.current_step + 1,
        )

        if inplace:
            self.u = uvp_new.u
            self.v = uvp_new.v
            self.p = uvp_new.p
            self.current_step = uvp_new.current_step
            return None
        else:
            return uvp_new

    def show(self):
        fig = plt.figure(figsize=(11, 7), dpi=100)
        plt.contourf(self.domain.x, self.domain.y, self.p, alpha=0.5, cmap=cm.viridis)
        plt.colorbar()
        plt.contour(self.domain.x, self.domain.y, self.p, cmap=cm.viridis)
        plt.streamplot(self.domain.x, self.domain.y, self.u, self.v)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.show()

    def animate(
        self,
        f: tuple[NDArray, NDArray],
        u_bcs: BoundaryConditions,
        v_bcs: BoundaryConditions,
        p_bcs: BoundaryConditions,
        filename: str,
        rho: float = 1,
        nu: float = 1,
    ):
        fig, ax = _prepare_fig(self.domain)
        scalar_field = ax.pcolormesh(
            self.domain.x,
            self.domain.y,
            self.p,
            cmap=cm.Blues,
            vmin=-4,
            vmax=4,
        )
        vector_field = ax.quiver(
            # TODO: this is ugly, determine slices from the size of the domain or something
            self.domain.x[::3, ::3],
            self.domain.y[::3, ::3],
            self.u[::3, ::3],
            self.v[::3, ::3],
            scale=8,
        )

        def update_quiver(n: int, _vector_field, _scalar_field, uvp: UVP):
            print(n)
            uvp.solve_for_next_uvp(f, u_bcs, v_bcs, p_bcs, rho, nu, inplace=True)
            _vector_field.set_UVC(uvp.u[::3, ::3], uvp.v[::3, ::3])
            _scalar_field.set_array(uvp.p)

        animation.FuncAnimation(
            fig=fig,
            func=update_quiver,  # type: ignore
            fargs=(vector_field, scalar_field, self),
            frames=self.domain.shape.t - 1,
            blit=False,
        ).save(
            filename=filename,
            writer=animation.PillowWriter(fps=30, bitrate=-1),
        )


def _prepare_fig(domain: Domain) -> tuple[Figure, Axes]:
    fig, ax = plt.subplots(figsize=(10, 10))

    ax.set_aspect("equal")
    ax.set_xlim([domain.x.min(), domain.x.max()])
    ax.set_ylim([domain.y.min(), domain.y.max()])

    return fig, ax
