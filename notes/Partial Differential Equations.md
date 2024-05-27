# 1. PDEs
### Def 1.1 (PDE)
A PDE is a relation that involves the unknown function $u(x_1, x_2, \dots, x_n, t)$, where $(x_1, x_2, \dots, x_n)$ is the spacial coordinate, and $t$ is the time, with its derivatives.
Symbolically we have
$$
F(x_1, x_2, \dots, x_n, t, u, u_{x_1}, u_{x_2}, \dots, u_{x_n}, u_{x_1x_1}, u_{x_1x_2}, \dots) = 0,
$$
for example
$$
u_t + u_x + u = 0,
$$
$$
u_t = u_{xx},
$$
etc.
# 2. Method of characteristics
### Def 2.1 (Quasilinear 1st order PDE)
A quasilinear first order PDE is
$$
u_t + c(x, t, u)u_x = f(x, t, u),
$$
where $u=u(x, t)$, $x \in \mathbb{R}$, $t \gt 0$. Moreover, $c$ and $f$ are known.
If $c=c(x, t)$, we call the above equation a semilinear equation, and additionally, if $f=f(x, t)$, we call it linear.
#### Remarks
- Quasilinear means "linear" in the derivatives. So that the nonlinearity involves only $u$
- We can consider a more general equation $d(x, t, u)u_t + c(x, t, u) = f(x, t, u)$, but we assume it is always possible to divide by $d$.
- A general balance law looks like the following
	$$
	u_t + q_x(x, t, u) = g(x, t, u).
	$$
- Function $c$ is actually the velocity of the wave, and we will see that later.
### Def 2.2 (Method Of Characteristics)
Let $X_\xi(t)$ be an arbitrary curve on the $x - t$ plane. Define $U_\xi(t) = u(X_\xi(t), t)$, where $u$ is the solution of our equation. Now differentiate:
$$
U_\xi'(t) = u_t + X_\xi'(t)u_x.
$$
Notice that this is exactly the left hand side of our equation, provided we have $X_\xi'(t) = c(X_\xi(t), t, U_\xi(t))$. Then we have
$$
U_\xi'(t) = f(X_\xi(t), t, U_\xi(t)).
$$
We have thus reduced our equation into an ODE
$$
\begin{aligned}
X_\xi'(t) &= c(X_\xi(t), t, U_\xi(t)), \\
U_\xi'(t) &= f(X_\xi(t), t, U_\xi(t)).
\end{aligned}
$$
These are the so-called characteristics equation, and $X_\xi(t)$ are called the characteristics.
We have to impose initial conditions. Assume that $u(x, 0) = \phi(x)$, then let $X_\xi(0) = \xi$, and obtain $U_\xi(0) = u(X_\xi(0), 0) = \phi(X_\xi(0)) = \phi(\xi)$.
In order to find the solution at any $(x, t)$ we find a unique characteristic $X_\xi(t)$ passing through $(x, t)$, go back to $t=0$, and use the initial condition, then read the solution from $U_\xi(t)$. 

# 3. Heat equation
Consider a homogenous initial-boundary value problem (IBV):
$$
\begin{cases}
u_t = \alpha^2u_{xx}, &\quad (x, t) \in (0, L) \times (0, T], \\
u(x, 0) = \varphi(x), &\quad x \in [0, L], \\
u(0, t) = u(L, t) = 0, &\quad t \in [0, T],
\end{cases}
$$
assume that $\varphi$ is continuous on $[0, L]$, and that $\varphi(0) = \varphi(L) = 0$.
The Fourier's method gives
$$
u(x, t) = \sum_{n=1}^\infty A_n\sin\left(\frac{n\pi}{L}x\right)\exp\left(-\frac{\alpha^2n^2\pi^2}{L^2}t\right),
$$
where
$$
A_n = \frac{2}{L}\int_0^L\varphi(x)\sin\left(\frac{n\pi}{L}x\right)dx.
$$
### Theorem 3.1 (Classical solution)
Let $\varphi \in C([0, L])$, and $\varphi(0) = \varphi(L) = 0$. Then $u(x, t)$ defined by the above is a classical solution of homogenous IBV problem. Moreover $u \in C^\infty([0, L] \times [0, T])$.

### Definition 3.2 (Green's function)
Notice that
$$
\begin{aligned}
u(x, t) &= \sum_{n=1}^\infty\int_0^L\frac{2}{L}\sin\left(\frac{n\pi}{L}x\right)\sin\left(\frac{n\pi}{L}y\right)\exp\left(-\frac{\alpha^2n^2\pi^2}{L^2}t\right)\varphi(y)dy = \\
&= \int_0^L\sum_{n=1}^\infty\frac{2}{L}\sin\left(\frac{n\pi}{L}x\right)\sin\left(\frac{n\pi}{L}y\right)\exp\left(-\frac{\alpha^2n^2\pi^2}{L^2}t\right)\varphi(y)dy = \\
&= \int_0^LG(x, y, t)\varphi(y)dy.
\end{aligned}
$$
We say that $G$, defined by $G(x, y, t) = \sum_{n=1}^\infty\frac{2}{L}\sin\left(\frac{n\pi}{L}x\right)\sin\left(\frac{n\pi}{L}y\right)\exp\left(-\frac{\alpha^2n^2\pi^2}{L^2}t\right)$ is the Green's function for homogenous IBV for the heat equation.


Now let's consider a non-homogenous heat equation:
$$
\begin{cases}
u_t = \alpha^2u_{xx} + f(x, t), &\quad (x, t) \in (0, L) \times (0, T], \\
u(x, 0) = \varphi(x), &\quad x \in [0, L], \\
u(0, t) = u(L, t) = 0, &\quad t \in [0, T],
\end{cases}
$$
Suppose that
$$
\begin{aligned}
u(x, t) &= \sum_{n=1}^\infty u_n(t)\sin\left(\frac{n\pi}{L}x\right), \\
f(x, t) &= \sum_{n=1}^\infty f_n(t)\sin\left(\frac{n\pi}{L}x\right).
\end{aligned}
$$
Plugging into the equation, and integrating yields
$$
u(x, t) = \int_0^t\int_0^LG(x, y, t-\tau)f(y, \tau)dyd\tau.
$$
### Theorem 3.3 (Green's function for heat equation in $\mathbb{R}$)
The Green's function given by
$$
G(x, y, t) = \frac{1}{\sqrt{4\pi}t}\exp\left(-\frac{(x-y)^2}{4t}\right)
$$
is:
- the Green's function for heat equation in $\mathbb{R}$,
- the fundamental solution of the heat equation,
- the Gauss characteristic kernel,
- the heat kernel.

