# 1 What are inverse problems?
Mathematically, an inverse problem is formalised as solving an operator equation of the form
$$
f = A(u) + e,
$$
where: 
- $f \in Y$ is the measured data
- $u \in X$ is the model parameter we aim to reconstruct
- The mapping $A: X \rightarrow Y$ is the forward operator, which describes how the model parameters give rise to the data in the absence of noise and measurement errors
- $e$ is the noise and observation errors

# 2 Examples of inverse problems
### 2.1 Computed tomography (CT)
The mathematical foundation of CT is based on the Radon transform, which describes how X-ray projections are formed as they pass through a body and is represented by the integral:
$$
A(u)(\omega, x) = \int_{-\infty}^\infty u(x + s\omega)ds.
$$
The model parameter is a real-valued function $u: \Omega \rightarrow \mathbb{R}$, $\Omega \in \mathbb{R}^d$, which represents an image of a cross-section of the body. Here, the unit vector $\omega$ and $x$, which is orthogonal to $\omega$ represent the line $l: s \mapsto x + s \omega$, along which X-rays travel. $A(u)(\omega, x)$ is the recovered projection.

### 2.2 Electrical Impedance Tomography (EIT)
$$
\begin{aligned}
\nabla (a(x)\nabla u) &= 0, \text{ in } \Omega, \\
u &= f, \text{ on } \partial \Omega
\end{aligned}
$$

$u$ is the electric potential, $a$ is the conductivity. The measured currents over the boundary for a specific voltage $f$ are given by 
$$
g_f = a \frac{\partial u}{\partial n}.
$$
Then in EIT the data consists of the Dirichlet-to-Neumann operator
$$
\Lambda_a: f \mapsto g_f.
$$

### 2.3 Groundwater filtration
The groundwater filtration problem is often modelled by the Darcy's law and the following elliptic equation
$$
-\nabla(a(x)\nabla u) = f, \text{ in } \mathbb{R}^d.
$$
Here, $u$ is the hydraulic head (pressure potential of groundwater), $a$ is the permability (hydraulic conductivity), and $f$ is the source term.

### 2.4 Earthquake source location
Here the inverse problem is: given observed seismic wave data, estimate the location and magnitude of the earthquake.

### 2.5 Engineering
Common inverse problem are
- given temperature measurements at time $t=T$, determine the initial temperature distribution at $t=0$
- given temperature measurements over time, determine the unknown heat source
$$
\frac{\partial u}{\partial t} = \Delta u + f
$$
### 2.6 Image denoising
We have an image
$$
f = u + e.
$$
We want to recover the clear image $u$, by removing the noise $e$.

### 2.7 Image deblurring
Assuming the general model
$$
f = A(u) + e,
$$
where $A(u) = K * u$, and $K$ is a smoothing kernel.

### 2.8 Image inpainting
Here we assume that 
$$
f = u|_{U \subset \Omega} + e.
$$
We have only the subset of the original image, and we want to recover the full image.

### 2.9 Parameter estimation in stochastic processes
Given observed trajectories of the stochastic process, try to estimate the parameters. Has applications in:
- finance - option pricing models calibration
- biology - qualitative analysis of particle dynamics

# 3 Definition of well-posedness
Inverse problems are typically ill-posed, i.e., they may not have a unique solution or solution may be sensitive to small errors in data.

### Def (well-posedness)
The notion of ill-posedness is usually attributed to Hadamard (Hadamard 1902) who postulated that well-posed problem should satisfy three conditions:
- it has a solution (existence)
- the solution is unique (uniqueness)
- the solution depends continuously on the data (stability)

The problem that does not satisfy at least one of these conditions is called ill-posed.

Classical research on inverse problems is focused on establishing conditions which guarantee that a solution to such ill-posed problems exists and on methods for approximating solutions in a stable way in presence of noise.

# 4 Differentiation of noisy data
Assume that we have $f \in C^1(0,1)$ with $f(0)=0$ and we want to solve the following inverse problem
$$
A(u)(x) = \int_0^xu(s)ds = f(x).
$$
We easily see that we can find a unique solution by differentiation, i.e. $u(x) = f'(x)$.

Now assume that instead of the exact data $f$ we have
$$
f^\delta(x) = f(x) + n^\delta(x),
$$
and $f^\delta(0)=f(0)=f^\delta(1)=f(1)=0$, where $n^\delta(x)$ represents data noise, and
$$
\int_\Omega|n^\delta(x)|^2dx = \delta^2.
$$
We can not obtain an estimate on the derivative $\frac{df}{dx}$. In the worst case the noise is not differentiable so we can not compute the derivative. However, even if we assume that 
the noise is differentiable, the error in the derivative can be arbitrarily large.

Let us consider 
$$
n^\delta(x) = \sqrt{2}\delta\sin(2 \pi kx).
$$
Then we have
$$
\int_0^1\left|n^\delta(x)\right|^2dx = \delta^2,
$$
but 
$$
\frac{df^\delta}{dx} = \frac{df}{dx} + \sqrt{2} \delta \cdot 2 \pi k \cos(2\pi k x),
$$
so, noting that $k$ can be arbitrarily large, then $\delta k$ can be arbitrarily large. Furthermore, we have
$$
\left\Vert\frac{df^\delta}{dx} - \frac{df}{dx}\right\Vert_{L^2(0, 1)} = 2 \pi \delta k,
$$
and
$$
\left\Vert\frac{df^\delta}{dx} - \frac{df}{dx}\right\Vert_{L^\infty(0, 1)} = 2\sqrt{2} \pi \delta k.
$$
In order to overcome ill-posedness of this problem, we may consider a regularisation.

Let's assume that $f \in C^2(0, 1)$. A simple example of regularisation consists of smoothing the data $f^\delta$ by solving the following differential equation:
$$
f_\alpha(x) - \alpha\frac{d^2 f_\alpha}{dx^2}(x) = f^\delta(x), \quad f_\alpha(0)=f_\alpha(1)=0.
$$
This approach can be identified with the so-called Tikhonov regularisation. Using standard results of variational calculus we can show that above equation is the optimality condition to the following minimisation problem:
$$
\min_f\left\{\frac{1}{2}\int_0^1\left(f(x) - f^\delta(x)\right)^2dx + \frac{\alpha}{2}\int_0^1\left(\frac{df}{dx}(x)\right)^2dx\right\}.
$$
Here the minimum is considered over all functions $f$ in 
$$
H_0^1(0, 1) = \left\{f \in L^2(0,1): \frac{df}{dx} \in L^2(0, 1), f(0)=f(1)=0\right\}.
$$
We aim to derive the estimate of the norm
$$
||\frac{df_\alpha}{dx} - \frac{df}{dx}||_{L^2(0,1)}.
$$
We have
$$
(f_\alpha - f) - \alpha(f_\alpha'' - f'') = f^\delta - f + \alpha f''.
$$
We multiply the above equation by $f_\alpha - f$ and integrate on $(0, 1)$:
$$
\int_0^1(f_\alpha - f)^2dx - \alpha\int_0^1(f_\alpha'' - f'')(f_\alpha - f)dx = \int_0^1\left(f^\delta - f + \alpha f''\right)(f_\alpha - f)dx.
$$
Then the integration by parts formula, and the fact that $f_\alpha$ and $f$ are zero on the boundary, lead to
$$
\int_0^1(f_\alpha - f)^2dx + \alpha\int_0^1(f_\alpha' - f')^2dx = \int_0^1\left(f^\delta - f + \alpha f''\right)(f_\alpha - f)dx.
$$
To estimate the right hand side, we apply $ab \le \frac{a^2}{2} + \frac{b^2}{2}$:
$$
||f_\alpha' - f'||_{L^2(0,1)}^2 \le \frac{1}{2}\frac{\delta^2}{\alpha} + \frac{\alpha}{2}C.
$$
Then, an optimal $\alpha$ is given by $\alpha = \frac{\delta}{\sqrt{C}}$, where $C = ||f||^2_{C^2(0,1)}$.

In the case we assume that $f \in C^1(0,1)$, we need to derive  an estimate in a bit different way
$$
\alpha\int f''(f_\alpha - f) = -\alpha\int f'(f_\alpha' - f') \le \frac{\alpha}{2}||f'||^2_{L^2} + \frac{\alpha}{2}||f_\alpha' - f'||^2_{L^2}.
$$
And we get (???)
$$
||f_\alpha' - f'||^2_{L^2} \le 2\frac{\delta^2}{\alpha} + C.
$$
# 5 Inverse problems modelled by integral equations
#### Examples
- The Fredholm integral equation of the first kind
$$
f(x) = \int_a^bk(x, y)u(y)dy.
$$
- The Volterra integral equation of the first kind
$$
	f(x) = \int_a^xk(x, y)u(y)dy.
$$
- The Abel integral equation
$$
f(x) = \int_0^x\frac{u(y)}{\sqrt{x-y}}dy.
$$
- The convolution equation
$$
f(x) = \int_a^bk(x-y)u(y)dy.
$$
### Tautochrone problem
The total time required for the particle to fall from $y=y_0$ to $y=0$ is given by the integral equation
$$
T(y_0) = \frac{1}{\sqrt{2g}}\int_0^{y_0}\frac{1}{\sqrt{y_0-y}}\frac{ds}{dy}dy,
$$
where $\frac{ds}{dy}$ is the distance remaining along the curve as a function of height.

### Computed tomography
Radon transform of a function $u: \mathbb{R}^2 \rightarrow \mathbb{R}$ is given by the following formula
$$
Ru(t, \omega) = \int_\mathbb{R}u(t\omega^\perp + s\omega)ds.
$$
The basic model of CT assumes the decay $-\Delta I$ of the intensity $I$ of an X-ray beam along a small distance $\Delta s$ is proportional to the intensity $I$, the density $u$ and to $\Delta s$. Hence
$$
\Delta I(t\omega^\perp + s\omega) = -I(t\omega^\perp + s\omega)u(t\omega^\perp\omega)\Delta s.
$$
Then for $\Delta s \rightarrow 0$, we obtain the ODE:
$$
\frac{dI}{ds}(t\omega^\perp + s\omega) = -I(t\omega^\perp + s\omega)u(t\omega^\perp + s\omega).
$$
By integrating from $s=0$ (the position of the emiter) to $s=L$ (the position of the detector), we obtain
$$
\ln\left(I(t\omega^\perp + L\omega)\right) - \ln\left(I(t\omega^\perp)\right) = -\int_0^Lu(t\omega^\perp + s\omega)ds.
$$
$I$ can be measure at the emitters and the detectors for $t$ and $\omega^\perp$. Since $u$ can be extended to be zero for $s \notin (0, L)$ , the inverse problem of CT is the inversion of the Radon transform.

Now consider the special case of radially symmetric density $u$ and $\Omega$ being a disc. In this case it is sufficient to use a single direction $\omega^\perp$, e.g. $\omega_0^\perp = (0, 1)$. Moreover we have
$$
U(r) = u(t\omega^\perp + s\omega).
$$
Then, using a transformation to polar coordinates we can rewrite the Radon transformation
$$
Ru(t, \omega_0) = 2\int_t^\varrho\frac{rU(r)}{\sqrt{r^2-t^2}}dr,
$$
with $\varrho$ sufficiently large.
# 6 The Fredholm integral equation of the first kind
$$
f(x) = \int_a^bk(x, y)u(y)dy,
$$
where $k: [a,b]^2 \rightarrow \mathbb{R}$ is the kernel. Let's derive the discretisation of this equation.
Consider a discrete set of points $a = x_1 < x_2 < \dots < x_M = b$,  $a = y_1 < y_2 < \dots < y_N = b$, then
$$
f(x_i) = \int_a^bk(x_i, y)u(y)dy = \int_a^bg(y)dy.
$$
We apply the trapezoid rule:
$$
\int_{y_k}^{y_{k+1}}g(y)dy = \frac{1}{2}\left(g(y_k) + g(y_{k+1})\right)(y_{k+1} - y_k) = \frac{h_y}{2}\left(g(y_k) + g(y_{k+1})\right),
$$
so
$$
f(x_i) \approx \frac{h_y}{2}\left(g(y_1) + 2g(y_2) + \dots + 2g(y_{N-1}) + g(y_N)\right).
$$
Then, using the matrix-vector notation, we get
$$
Ku = f,
$$
where 
$$
f = (f(x_1), \dots, f(x_M)), \quad u = (u(y_1), \dots, u(y_N)).
$$
1. $M=N$: If $K$ is nonsingular, then $u=K^{-1}f$ is a unique solution.
2. $M>N$: The system is overdetermined. If the rank of $K$ is $N$, then an approximate solution can be found using the least squares method
$$
\min\limits_u\Vert Ku-f\Vert_2.
$$
3. $M<N$: The system is underdetermined and there is no unique solution.
$$
\min\limits_u\left\{\frac{1}{2}\Vert Ku-f \Vert_2^2 + \frac{\alpha}{2}\Vert u \Vert_2^2\right\}.
$$

Assume that $M=N$, $M \in \mathbb{R}^{N \times M}$, $M$ is nonsingular,
$$
Ku = f, \text{ and } Ku_\delta = f_\delta.
$$
We have
$$
||u-u_\delta|| = ||K^{-1}(f-f_\delta)|| \le ||K^{-1}||\cdot||f-f_\delta||.
$$
Since $||f|| = ||Ku|| \le ||K||\cdot||u||$, we express the relative error as
$$
\frac{||u-u_\delta||}{||u||} \le ||K||\cdot||K^{-1}||\frac{||f-f_\delta||}{||f||}.
$$
### What can we do?
###### Tikhonov regularization
$$
\min\limits_u\left\{\frac{1}{2}\Vert Ku -f \Vert_2^2 + \frac{\alpha}{2}\Vert u \Vert_2^2\right\}
$$
###### Truncated singular value decomposition (TSVD)
The SVD of the matrix $K^{M \times N}$ is given by
$$
K = U \Sigma V^T.
$$
Here:
- $U \in \mathbb{R}^{M \times M}$ is an orthonormal matrix whose columns are left singular vectors,
- $V \in \mathbb{R}^{N \times N}$ is an orthonormal matrix whose columns are right singular vectors,
- $\Sigma \in \mathbb{R}^{M \times N}$ is a diagonal matrix with singular values $\sigma_1 > \sigma_2 > \dots > 0$

Truncated SVD approximates $K$ by keeping only the largest $s$ singular values
$$
K_s = U_s \Sigma_s V_s^T,
$$
where $\Sigma_s \in {\mathbb{R}^{s \times s}}$, $U_s \in \mathbb{R}^{M \times s}$, $V_s \in \mathbb{R}^{N \times s}$.

# 7 Inverse heat problem
We have a heat equation in 1d
$$
u_t = u_{xx}, \quad x\in(0, \pi), t>0,
$$
$$
u(0, t) = u(\pi, t) = 0, \quad t > 0,
$$
$$
u(x, 1) = f(x).
$$
We want to determine the initial temperature $g(x) = u(x, 0)$.
To solve the equation we apply the method of separation of variables ez.
