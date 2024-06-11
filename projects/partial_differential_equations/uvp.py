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


"""
Considering the equations (Incompressible Navier-Stokes):
(1) u_t = 𝛎Δu - (u·∇)u - ∇p/ϱ + f
(2) ∇·u = 0

Taking the divergence of (1) and applying (2) we get
(1') u_t = 𝛎Δu - (u·∇)u - ∇p/ϱ + f
(2') Δp = ϱ(∇f - ∇·(u·∇)u)
which is known as the velocity-pressure formulation of the Navier-Stokes equations

In the computations we let vector(u) = (u, v), and
u = u(t, x, y)
v = v(t, x, y)
p = p(t, x, y)
"""


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
    u_bcs: BoundaryConditions  # u boundary conditions
    v_bcs: BoundaryConditions  # v boundary conditions
    p_bcs: BoundaryConditions  # p boundary conditions
    f: tuple[NDArray, NDArray]  # external force in x and y
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

    def build_pressure_equation_rhs(self, u_new: NDArray, v_new: NDArray) -> NDArray:
        u, v, _ = self
        dt, dx, dy = self.domain.diff
        f_x, f_y = self.f

        rhs = np.zeros(self.domain.shape.xy)
        rhs[1:-1, 1:-1] = self.rho * (
            d_dx(f_x, dx)
            + d_dy(f_y, dy)
            + (d_dx(u_new, dx) + d_dy(v_new, dy)) / dt
            - 2 * d_dy(u_new, dy) * d_dx(v_new, dx)
            - d_dx(u_new, dx)**2
            - d_dy(v_new, dy)**2
        )
        return rhs

    def solve_for_pressure(self, u_new: NDArray, v_new: NDArray, num_iterations: int = 100) -> NDArray:
        rhs = self.build_pressure_equation_rhs(u_new, v_new)
        _, dx, dy = self.domain.diff

        p_next = None
        p_previous = self.p.copy()
        for _ in range(num_iterations):
            p_next = p_previous.copy()

            p_next[1:-1, 1:-1] = (
                (p_previous[1:-1, 2:] + p_previous[1:-1, 0:-2]) * dy**2
                + (p_previous[2:, 1:-1] + p_previous[0:-2, 1:-1]) * dx**2
                - rhs[1:-1, 1:-1] * dx**2 * dy**2
            ) / (2 * (dx**2 + dy**2))

            self.p_bcs(p_next, self.t, self.domain.x, self.domain.y)

        return p_next

    def solve_for_u(self) -> NDArray:
        u_old, v_old, _ = self
        dt, dx, dy = self.domain.diff
        u_new = np.zeros_like(u_old)

        u_new[1:-1, 1:-1] = (
            u_old[1:-1, 1:-1]
            + dt * (
                - u_old[1:-1, 1:-1] * d_dx(u_old, dx)
                - v_old[1:-1, 1:-1] * d_dy(u_old, dy)
                - d_dx(self.p, dx) / self.rho
                + self.nu * (d2_dx2(u_old, dx) + d2_dy2(u_old, dy))
                + self.f[0][1:-1, 1:-1]
            )
        )

        self.u_bcs(u_new, self.t, self.domain.x, self.domain.y)

        return u_new

    def solve_for_v(self) -> NDArray:
        u_old, v_old, _ = self
        dt, dx, dy = self.domain.diff

        v_new = np.zeros_like(v_old)
        v_new[1:-1, 1:-1] = (
            v_old[1:-1, 1:-1]
            + dt * (
                - u_old[1:-1, 1:-1] * d_dx(v_old, dx)
                - v_old[1:-1, 1:-1] * d_dy(v_old, dy)
                - d_dy(self.p, dy) / self.rho
                + self.nu * (d2_dx2(v_old, dx) + d2_dy2(v_old, dy))
                + self.f[1][1:-1, 1:-1]
            )
        )

        self.v_bcs(v_new, self.t, self.domain.x, self.domain.y)

        return v_new

    def solve_for_next_uvp(self, inplace: bool = False) -> Self | None:
        u_new = self.solve_for_u()
        v_new = self.solve_for_v()
        p_new = self.solve_for_pressure(u_new, v_new)

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

    def discard(self):
        # jupyter displaying repr of this object after invoking show, this is to deal with it and not get migraine along the way
        pass

    def show(self, at: float | None = None, fig: Figure | None = None, ax: Axes | None = None) -> Self:
        if at is not None:
            assert self.t <= at
            while self.t < at:
                self.solve_for_next_uvp(inplace=True)

        if fig is None or ax is None:
            fig, ax = _prepare_fig(self.domain)

        color_mesh = ax.pcolormesh(
            self.domain.x,
            self.domain.y,
            self.p,
            cmap=cm.Blues,
            vmin=self.p.min(),
            vmax=self.p.max(),
            shading="gouraud",
        )
        ax.streamplot(self.domain.x, self.domain.y, self.u, self.v)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title(f"t = {self.t}")
        plt.colorbar(
            mappable=color_mesh,
            ax=ax
        )
        fig.show()
        return self

    def animate(
        self,
        filename: str,
        total_number_of_frames: int = 300,
        fps: int = 30,
        x_spacing: int = 3,
        y_spacing: int = 3,
        p_range: tuple[float, float] = (-2, 2),
    ):
        assert total_number_of_frames < self.domain.shape.t
        iterations_per_frame = self.domain.shape.t // total_number_of_frames

        x_slice = slice(None, None, x_spacing)
        y_slice = slice(None, None, y_spacing)

        fig, ax = _prepare_fig(self.domain)
        scalar_field = ax.pcolormesh(
            self.domain.x,
            self.domain.y,
            self.p,
            cmap=cm.Blues,
            vmin=p_range[0],
            vmax=p_range[1],
            shading="gouraud",
        )
        vector_field = ax.quiver(
            self.domain.x[x_slice, y_slice],
            self.domain.y[x_slice, y_slice],
            self.u[x_slice, y_slice],
            self.v[x_slice, y_slice],
            scale=8,
        )

        def update_fields(n: int, _vector_field, _scalar_field, uvp: UVP):
            print(f"{n} / {total_number_of_frames}")
            for _ in range(iterations_per_frame):
                uvp.solve_for_next_uvp(inplace=True)
            _vector_field.set_UVC(uvp.u[x_slice, y_slice], uvp.v[x_slice, y_slice])
            _scalar_field.set_array(uvp.p)

        animation.FuncAnimation(
            fig=fig,
            func=update_fields,  # type: ignore
            fargs=(vector_field, scalar_field, self),
            frames=total_number_of_frames,
            blit=False,
        ).save(
            filename=filename,
            writer=animation.PillowWriter(fps=fps, bitrate=-1),
        )


def _prepare_fig(domain: Domain) -> tuple[Figure, Axes]:
    fig, ax = plt.subplots(figsize=(10, 10))

    ax.set_aspect("equal")
    ax.set_xlim([domain.x.min(), domain.x.max()])
    ax.set_ylim([domain.y.min(), domain.y.max()])
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    return fig, ax
