3 skipped lectures/labs allowed

# 1. What are inverse problems?
Mathematically, an inverse problem is formalised as solving an operator equation of the form
$$
f = A(u) + e,
$$
where: 
- $f \in Y$ is the measured data
- $u \in X$ is the model parameter we aim to reconstruct
- The mapping $A: X \rightarrow Y$ is the forward operator, which describes how the model parameters give rise to the data in the absence of noise and measurement errors
- $e$ is the noise and observation errors

# 2. Examples of inverse problems
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

