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
