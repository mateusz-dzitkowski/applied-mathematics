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

# 8 Ill-conditioned matrix equations
We consider an inverse problem that can be posed as a system of linear equations
$$
Ku = f
$$
where $K \in \mathbb{R}^{m \times n}$ is a given matrix and $f \in \mathbb{R}^m$ is our input data.
We aim to find a solution $u \in \mathbb{R}^n$ that approximately satisfies the equations. 
We need to discuss existence, uniqueness, and stability of the solution
1. Well posedness
	1. If $m=n$, and $K$ has full rank, then $K$ is invertible and the solutions is given by 
$$
u = K^{-1}f
$$
	2. if $m>n$, and $rank(K)=n$, then the system of equations may be inconsistent, in which case a solution doesn't exist when $f$ is not in the range of $K$:
$$
R(K) = \left\{x_1k_1 + x_2k_2 + \dots + x_nk_n: x=(x_1, \dots x_n)\in\mathbb{R}^n, \text{ and $k$ denotes the $i$th column of $K$}\right\}.
$$
	3. if $m<n$, and $rank(K)=m$, we can always find a solution but it may be not unique because $K$ has a non-trivial null space:
$$
N(K) = \left\{x\in\mathbb{R}^n: Kx=0\right\}.
$$
	4. if $K$ doesn't have maximal rank, the system of equations may be both inconsistent and undetermined.
2. Stability
   Let $Ku=f$, $Ku^\delta=f^\delta$. We wish for $C$ such that
$$
||u-u^\delta|| \le C||f-f^\delta||.
$$
	We get the relative error:
$$
\frac{||u-u^\delta||}{||u||} \le ||K||||K^{-1}||\frac{||f-f^\delta||}{||f||}.
$$
## 8.1 Pseudo-inverse
We need to discuss how we may define solutions of inconsistent or indetermined systems of equations. Let $K \in \mathbb{R}^{m \times n}$. Then the singular value decomposition (SVD) of $K$ is given by 
$$
K = U \Sigma V^*,
$$
where:
- $U \in \mathbb{R}^{m \times m}$ is a unitary matrix $UU^* = U^*U$,
- $V \in \mathbb{R}^{n \times n}$ is a unitary matrix $VV^* = V^*V$,
- $\Sigma \in \mathbb{R}^{m \times n}$ is a diagonal matrix with $\sigma_i = \Sigma_{ii}$ - singular values of $K$.
Remarks:
- columns of $U$, $(u_1, u_2, \dots, u_m)$, form an orthonormal basis in $\mathbb{R}^m$,
- the number of non-zero singular values is equal to the rank of $K$,
- if $\sigma_1 \ge \sigma_2 \ge \dots \sigma_r > 0$, then
$$
K = \Sigma_{i=1}^r\sigma_i u_iv_i^* = U_r \Sigma_r V_r^*.
$$
	where $r \le \min\{m, n\}$ is the rank of $K$.

Now we can define the pseudo-inverse:
- if $m>n$, the system is inconsistent when $f \notin R(K)$. If $K$ has a full rank, i.e. $rank(K)=n$, we can write
$$
K = U_n \Sigma_n V_n^*.
$$
	we rewrite the system of equations to
$$
Ku = U_nU_n^*f,
$$
	then, using the SVD we see that
$$
u = K^{-1}\left(U_nU_n^*f\right) = V_n \Sigma_n^{-1} U_n^* U_n U_n^* f = V_n \Sigma_n^{-1} U_n^*.
$$
Define
$$
K^{\dagger}f = V_n \Sigma_n^{-1} U_n^* f
$$
to be the Moore-Penrose pseudo-inverse of $K$. We can show that this conincides witht the least-squares solution
$$
\min\limits_u||Ku-f||^2.
$$
To show this we consider the normal equation
$$
K^*Ku = K^*f.
$$
Now we have $K = U_n \Sigma_n V_n^*$, and $K^*=V_n \Sigma_n U_n^*$, so
$$
K^*K = V_n \Sigma_n^2 V_n^*,
$$
and 
$$
(K^*K)^{-1} = V_n^* \Sigma_n^{-2} V_n,
$$
hence
$$
u = (K^*K)^{-1}K^*f = V_n \Sigma_n^{-1} U_n f.
$$
- if $m<n$, and $K$ has a full rank, $rank(K)=m$, then a solution exists, but is not unique. In this case, we can look for the smallest solution that is we look for a solution that is spanned by the first $m$ right singular eigenvectors $(v_1, \dots, v_m)$, i.e
$$
K V_m z = f, \quad\text{ with } u = V_m z.
$$
	We find this solution is given by
$$
u = V_m \Sigma_m^{-1} U_m f = K^\dagger f.
$$
	We can show that this solution is equivalent to the solution of the problem
$$
\min\limits_u ||u||^2, \quad\text{ such that } Ku=f.
$$
	To show this, we consider a solution of the form
$$
v = u + z,
$$
	with $u = K^\dagger f$, and $Kz=0$. By straightforward calculations we have
$$
\begin{aligned}
||v||^2 = ||u+z||^2 &= ||u||^2 + 2\langle u,z \rangle + ||z||^2 = \\
&= ||u||^2 + 2\langle V_m \Sigma_n^{-1} U_m^* f,z \rangle + ||z||^2 = \\
&= ||u||^2 + 2\langle \Sigma_m^{-1} U_m^* f, V_m^* z \rangle + ||z||^2 = \\
&= ||u||^2 + ||z||^2 \ge ||u||^2.
\end{aligned}
$$
### Definition (Moore-Penrose pseudo-inverse)
The pseudo-inverse of a matrix $K \in \mathbb{R}^{m \times n}$ with the rank $r \le \{m, n\}$ if defined in terms of the SVD as
$$
K^\dagger = V_r \Sigma_r^{-1} U_r^*
$$
where $V_r = (v_1, v_2, \dots, v_r)$, $U_r = (u_1, u_2, \dots, u_r)$, and $\Sigma_r$ contains the $r$ largest (non-zero) singular values.
We note that the pseudo-inverse allows to define a unique solution, however this solution is not necessarily stable since the condition number 
$$
||K|| \cdot ||K^\dagger|| = \frac{\sigma_1}{\sigma_r}
$$
may be large.
We can write
$$
u = V_r \Sigma_r^{-1} U_r^* f = \sum_{i=1}^r \frac{1}{\sigma_i}\langle u_i, f \rangle v_i.
$$
To stabilise the problem we can modify the pseudo-inverse to avoid dividing by small singular values. One possibility is to simply ignore small singular values and consider
$$
u_\alpha = V_r R_\alpha(\Sigma_r) U_r^* f,
$$
where
$$
R_\alpha(\sigma) = \begin{cases}
	\frac{1}{\sigma},& \sigma \ge \alpha, \\
	0,& \text{otherwise}.
\end{cases}
$$

Another option to avoid dividing by small singular values is to add a small positive constant to shift the singular eigenvalues away from zero. This leads to the Tikhonov regularisation:
$$
u_\alpha = \sum_{i=1}^r \frac{\sigma_i}{\sigma_i^2 + \alpha}\langle u_i, f \rangle v_i.
$$
This corresponds to setting
$$
R_\alpha(\sigma) = \frac{\sigma}{\sigma^2 + \alpha}.
$$
The Tikhonov regularisation corresponds to the variational problem
$$
\min\limits_u\left\{ ||Ku - f||^2 + \alpha||u||^2 \right\}.
$$
# 9 Parameter identification problems in differential equations
Consider the following problem
$$
-\nabla\left(a(x) \nabla u\right) = f,
$$
with appropriate boundary conditions.
We wish to determine $a$ based on the observations $u$.
#### Uniqueness
Let us consider a 1d case:
$$
-(au')' = f, \quad u'(0)=0, \quad u(1) = 0.
$$
Let's define the so-called parameter to solution map
$$
F: a \mapsto u_a
$$
Turns out in this case $F$ is a bijection lets go.

The natural question is: how to guarantee that $u' \ne 0$.
- if $\int_0^xf(s)ds > 0$ in $(0,1)$, then we get $u'(x) < 0$,
- we can assume that $f(x) \ne 0$ for almost every $x$, then $u'(x)$ cannot vanish on an open interval $I \subset [0, 1]$, since otherwise we would get a contradiction with the original equation
#### Stability
We consider the continuity of the inverse operator on a special subset of its domain
$$
C_{\gamma, M} = \left\{ u \in C^2([0, 1]): ||u||_{C^2} \le M, u'(x) \ge \gamma \right\}.
$$
Let $u_j$ be the solution of the direct problem for given parameter $a_j$, $j = 1, 2, \dots$.
Then we have
$$
a_1(x) - a_2(x) = \frac{-\int_0^xf(s)ds}{u_1'(x)u_2'(x)}\left(u_2'(x) - u_1'(x)\right).
$$
We square both sides, integrate, and use some tricks (?) to get
$$
||a_1 - a_2||_{L^2}^2 \le \frac{1}{\gamma^4}||f||_{L^1}^2||u_2' - u_1'||_{L^2}^2.
$$
Then we use integration by parts, and the Cauchy-Schwartz inequality:
$$
||u_2' - u_1'||_{L^2}^2 = \int_0^1(u_2 - u_1)\left(u_2'' - u_1''\right)dx \le ||u_2-u_1||_{L^2} ||u_2'' - u_1''||_{L^2}.
$$
Then we use the Minkowski inequality, and the assumptions, and finally
$$
||a_1 - a_2||_{L^2}^2 \le \frac{2}{\gamma^4}\sqrt{M}||f||_{L_1}^2||u_1 - u_2||_{L^2}.
$$

### Def (Gateaux derivative)
Let $U$ be a normed vector space and let $J: U \rightarrow \mathbb{R}$ be a functional. Then the Gateaux derivative of $J$ at $u \in U$ in the direction $\varphi \in U$ is defined by
$$
J'(u; \varphi) = \lim\limits_{\varepsilon \rightarrow 0} \frac{J(u + \varepsilon \varphi) - J(u)}{\varepsilon}
$$
provided that the limit exists.

If $U$ is a Hilbert space, and $J$ is Gateaux differentiable, then there exists a gradient $\nabla J(u) \in U$ such that
$$
J'(u; \varphi) = \langle \nabla J(u), \varphi\rangle.
$$

#### Example
Consider the functional $J: U \rightarrow \mathbb{R}$ defined by
$$
J(u) = \int_0^1\left(\frac{du}{dx}\right)^2dx.
$$
By the definition we have
$$
J'(u; \varphi) = \lim\limits_{\varepsilon \rightarrow 0}\frac{1}{\varepsilon}\left(\int_0^1\left(\left(\frac{d(u+\varepsilon\varphi)}{dx}\right)^2 - \left(\frac{du}{dx}\right)^2\right)dx\right) = 2\int_0^1\frac{du}{dx}\frac{d\varphi}{dx}dx.
$$
To get the gradient $\nabla J(u)$ we apply the integration by parts formula and get
$$
J'(u; \varphi) = -\int_0^1\frac{d^2u}{dx^2}\varphi dx + \left[\frac{du}{dx}\varphi\right]_0^1 = -\int_0^1\frac{d^2u}{dx^2}\varphi dx,
$$
applying appropriate boundary conditions that make the last term vanish.

Consider the following problem
$$
-(a(x)u'(x))' = f(x),
$$
$$
a(0)u'(0) = a(1)u'(1) = 0.
$$
We consider the inverse problem of determining the parameter $a$ from the measurements $u^\delta$ of $u$. For this purpose we consider the objective functional $J: U \rightarrow \mathbb{R}$ defined by
$$
J(u) = \int_0^1(u-u^\delta)^2dx.
$$
We note that in the above definition the state variable $u \in U$ is implicitly dependent on $a \in V$ through the state equation.
 
Let's denote by $u_a \in U$ the unique solution to the state equation, and, moreover, impose on $a$ to be in $U$. Then we can use the so-called reduced objective functional, which is given by
$$
\tilde{J} = J(u_a) + \alpha \int_0^1\left(\frac{da}{dx}\right)^2dx,
$$
and formulate the minimisation problem as follows
$$
\min_{a \in U}\tilde{J}(a), \quad \text{s.t.} \quad -(a(x)u_a'(x)) = f, \quad a(0)u_a'(0) = a(1)u_a'(1) = 0.
$$
We solve the above problem by the method of Lagrangian multipliers. The associated Lagrange functional $L: U \times U \times U \rightarrow \mathbb{R}$ is given by
$$
L(u, p, a) = J(u) + \alpha\int_0^1a'^2dx + \int_0^1 au'p'dx - \int_0^1fpdx,
$$
where $p$ is the Lagrange multiplier or the adjoint state variable.

The Lagrangian method states that the solution to the problem has to be a stationary point of the Lagrangian, that is, it has to satisfy the system of equations
$$
\begin{aligned}
\langle \nabla_u L, \varphi \rangle &= 0, \quad \text{ for all } \varphi \in U \\
\langle \nabla_p L, \varphi \rangle &= 0, \quad \text{ for all } \varphi \in U \\
\langle \nabla_a L, \varphi \rangle &= 0, \quad \text{ for all } \varphi \in U.
\end{aligned}
$$
We note that the second equation in the above system is equivalent to the state equation.
The first equation is the so-called adjoint state equation and is given by
$$
-(au')' = -\nabla J(u), \quad p(0)=p(1)=0.
$$
Finally the last equation is given by
$$
-\alpha a'' = u'p', \quad a'(0)=a'(1)=0.
$$
# 10 Tikhonov regularisation
Let $K = U_k \Sigma_k V_k^*$, where $rank(K) = k \le \min\{m, n\}$. The Tikhonov-regularised solution to the equation $Ku=f$ is given by
$$
u_\alpha = \sum_{i=1}^k\frac{\sigma_i\langle u_i, f \rangle}{\sigma_i^2 + \alpha}v_i,
$$
where $\left\{(u_i, \sigma_i, v_i)\right\}_{i=1}^k$ is the singular system of $K$. 
The Tikhonov regularisation can be formulated as the following optimisation problem
$$
\min\limits_{u \in \mathbb{R}^n}\left\{ \Vert Ku - f\Vert_2^2 + \alpha\Vert u \Vert_2^2 \right\},
$$
which solution is given by $u_\alpha = (K^*K + \alpha I)^{-1}K^*f$.

We note that the idea of the Tikhonov regularisation can be extended to more general setting and the regularised solution can be interpreted as a minimiser of the functional defined by
$$
J_\alpha(u) = \Vert Ku - f \Vert_V^2 + \alpha  \Vert u \Vert_U^2,
$$
where $U$ is a Hilbert space, and $V$ is a Banach space. Here $K: U \rightarrow V$, $K \in \mathcal{L}(U, V)$, $\mathcal{L}(U, V)$ is the set of all linear, bounded operators $K: U \rightarrow V$.

Then we define the regularised solution
$$
u_\alpha = \min\limits_{u \in U}J_\alpha(u).
$$
### Theorem
For $f \in V$, the Tikhonov-regularised solution is given by
$$
u_\alpha = (K^*K + \alpha I)^{-1}K^*f,
$$
and is a unique global minimiser of $J_\alpha$.

### Variational regularisation
In variational regularisation we generalise the Tikhonov regularisation by choosing different regularisation functionals $R: U \rightarrow \mathbb{R}$ and then compute the regularised solution by minimising the functional
$$
J_\alpha = \Vert Ku - f \Vert_V^2 + \alpha R(u).
$$
#### Example (Sobolev regularisation)
$$
J_\alpha(u) = \Vert Ku - f \Vert_{L^2{\Omega}}^2 + \alpha \Vert \nabla u \Vert_{L^2{\Omega}}^2
$$
$$
K: H^1(\Omega) \rightarrow L^2(\Omega)
$$
#### Example ($l^1$-norm regularisation)
$$
J_\alpha(u) = \Vert Ku - f \Vert_{l^2}^2 + \alpha \Vert u \Vert_{l^1}.
$$
Here, $l^2$ and $l^1$ are spaces of sequences, and 
$$
\Vert u \Vert_{l^p} = \sum_{i=1}^\infty|u_i|^p.
$$
Tao worked on this btw.
#### Example (Maximum-entropy regularisation)
It is of particular interest if the solutions of the inverse problems are assumed to be probability density functions, which are functions in the set
$$
PDF(\Omega) = \left\{ u \in L^1(\Omega): \int_\Omega u dx = 1, u \ge 0 \right\}.
$$
Then the entropy is defined as
$$
E(u) = \int_\Omega u\log(u)dx.
$$
Usually, since $PDF(\Omega)$ may not be a vector space, we define
$$
R(u) = 
\begin{cases}
	E(u), &\quad u \in PDF(\Omega),\\
	\infty, &\quad \text{otherwise}.
\end{cases}
$$
Then
$$
J_\alpha(u) = \Vert Ku - f \Vert_{L^2}^2 + \alpha R(u).
$$

