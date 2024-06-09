from dataclasses import dataclass, replace
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
    domain: Domain
    u: NDArray  # x component of velocity
    v: NDArray  # y component of velocity
    p: NDArray  # pressure
    u_bcs: BoundaryConditions
    v_bcs: BoundaryConditions
    p_bcs: BoundaryConditions
    f: tuple[NDArray, NDArray]
    rho: float
    nu: float
    current_step: int

    @classmethod
    def new(
        cls,
        domain: Domain,
    ) -> Self:
        return cls(
            u=np.zeros(domain.shape.xy),
            v=np.zeros(domain.shape.xy),
            p=np.zeros(domain.shape.xy),
            u_bcs=lambda u, t, x, y: None,
            v_bcs=lambda u, t, x, y: None,
            p_bcs=lambda u, t, x, y: None,
            domain=domain,
            f=(np.zeros(domain.shape.xy), np.zeros(domain.shape.xy)),
            rho=1,
            nu=1,
            current_step=0,
        )

    def __iter__(self):
        return iter((self.u, self.v, self.p))

    def with_initial_conditions(
        self,
        u: NDArray | None = None,
        v: NDArray | None = None,
        p: NDArray | None = None,
    ) -> Self:
        if u is not None: self.u = u
        if v is not None: self.v = v
        if p is not None: self.p = p
        return self

    def with_boundary_conditions(
        self,
        u_bcs: BoundaryConditions | None = None,
        v_bcs: BoundaryConditions | None = None,
        p_bcs: BoundaryConditions | None = None,
    ):
        if u_bcs is not None: self.u_bcs = u_bcs
        if v_bcs is not None: self.v_bcs = v_bcs
        if p_bcs is not None: self.p_bcs = p_bcs
        return self

    def with_parameters(
        self,
        f: tuple[NDArray, NDArray] | None = None,
        rho: float | None = None,
        nu: float | None = None,
        current_step: int | None = None,
    ):
        if f is not None: self.f = f
        if rho is not None: self.rho = rho
        if nu is not None: self.nu = nu
        if current_step is not None: self.current_step = current_step
        return self

    @property
    def t(self) -> float:
        return self.domain.t[self.current_step]  # type: ignore

    def build_pressure_equation_rhs(self) -> NDArray:
        u, v, _ = self
        dt, dx, dy = self.domain.diff
        f_x, f_y = self.f

        rhs = np.zeros(self.domain.shape.xy)
        rhs[1:-1, 1:-1] = self.rho * (
            d_dx(f_x, dx)
            + d_dy(f_y, dy)
            + (d_dx(u, dx) + d_dy(v, dy)) / dt
            - 2 * d_dy(u, dy) * d_dx(v, dx)
            - d_dx(u, dx)**2
            - d_dy(v, dy)**2
        )
        return rhs

    def solve_for_pressure(self, num_iterations: int = 100) -> NDArray:
        rhs = self.build_pressure_equation_rhs()
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

            self.p_bcs(p_next, self.t, self.domain.x, self.domain.y)

        return p_next

    def solve_for_u(self, p_new: NDArray) -> NDArray:
        u_old, v_old, _ = self
        dt, dx, dy = self.domain.diff
        u_new = np.zeros_like(u_old)

        u_new[1:-1, 1:-1] = (
            u_old[1:-1, 1:-1]
            + dt * (
                - u_old[1:-1, 1:-1] * d_dx(u_old, dx)
                - v_old[1:-1, 1:-1] * d_dy(u_old, dy)
                - d_dx(p_new, dx) / self.rho
                + self.nu * (d2_dx2(u_old, dx) + d2_dy2(u_old, dy))
                + self.f[0][1:-1, 1:-1]
            )
        )

        self.u_bcs(u_new, self.t, self.domain.x, self.domain.y)

        return u_new

    def solve_for_v(self, p_new: NDArray) -> NDArray:
        u_old, v_old, _ = self
        dt, dx, dy = self.domain.diff

        v_new = np.zeros_like(v_old)
        v_new[1:-1, 1:-1] = (
            v_old[1:-1, 1:-1]
            + dt * (
                - u_old[1:-1, 1:-1] * d_dx(v_old, dx)
                - v_old[1:-1, 1:-1] * d_dy(v_old, dy)
                - d_dy(p_new, dy) / self.rho
                + self.nu * (d2_dx2(v_old, dx) + d2_dy2(v_old, dy))
                + self.f[1][1:-1, 1:-1]
            )
        )

        self.v_bcs(v_new, self.t, self.domain.x, self.domain.y)

        return v_new

    def solve_for_next_uvp(self, inplace: bool = False) -> Self | None:
        p_new = self.solve_for_pressure()
        u_new = self.solve_for_u(p_new)
        v_new = self.solve_for_v(p_new)

        if inplace:
            self.u = u_new
            self.v = v_new
            self.p = p_new
            self.current_step += 1
            return None

        return (
            UVP.new(domain=replace(self.domain))
            .with_initial_conditions(
                u=self.u.copy(),
                v=self.v.copy(),
                p=self.p.copy(),
            )
            .with_boundary_conditions(
                u_bcs=self.u_bcs,
                v_bcs=self.v_bcs,
                p_bcs=self.p_bcs,
            )
            .with_parameters(
                f=self.f,
                rho=self.rho,
                nu=self.nu,
                current_step=self.current_step + 1,
            )
        )

    def show(self):
        fig = plt.figure(figsize=(11, 7), dpi=100)
        plt.contourf(self.domain.x, self.domain.y, self.p, alpha=0.5, cmap=cm.viridis)
        plt.colorbar()
        plt.contour(self.domain.x, self.domain.y, self.p, cmap=cm.viridis)
        plt.streamplot(self.domain.x, self.domain.y, self.u, self.v)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.show()

    def animate(self, filename: str):
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
            uvp.solve_for_next_uvp(inplace=True)
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
