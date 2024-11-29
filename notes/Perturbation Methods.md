## Organisational stuff

Consultations: Wed. 17-19, Thu. 13-15, room C-19 3.25
Attendance obligatory, skip at most 3
Test: 2025-01-24 09:15:00+01:00
2nd term: 2025-02-03 09:15:00+01:00

Literature:
- E.J. Hinch, "Perturbation Methods", Cambridge, 1992
- M.H. Holmes, "Introduction to Perturbation Methods", Springer, 2013
- R.S. Johnson, "Singular Perturbation Theory", Springer, 2009
- J.D. Logan, "Applied Mathematics", Wiley, 2013

Plan of the lecture:
1. Introduction
2. Asymptotic solutions of algebraic equations
3. Regular perturbations of ODEs and PDEs
4. Singular perturbations
5. Lindstedt expansion
6. Multiple scales
7. Asymptotic expansion of integrals
8. Asymptotic expansion in homogenisation

# 1. Introduction

Say we have a problem 
$$
P(u_\varepsilon, \varepsilon) = 0,
$$
and this problem is "difficult" to solve. We call this problem a **perturbed** problem. Then the problem
$$
P(u_0, 0) = 0,
$$
which is easier to solve, is an unperturbed problem, that is an approximation to the first one.
Then we can apply corrections to the unperturbed problem by e.g.
$$
u_\varepsilon = u_0 + \varepsilon u_1 + \varepsilon^2 u_2 + \dots
$$

### Example
Consider the following ODE:
$$
u_\varepsilon'' + (u_\varepsilon')^2 + \varepsilon u_\varepsilon = 0.
$$
We can consider the unperturbed problem:
$$
u_0'' + (u_0')^2 = 0,
$$
which is easier to solve.

### Def 1.1 Big O and small O
We write $f(\varepsilon) = O(g(\varepsilon))$  as $\varepsilon \rightarrow \varepsilon_0$ if there exists a constant $M > 0$ such that the following inequality holds for all $\varepsilon$ in some neighbourhood of $\varepsilon_0$:
$$
|f(\varepsilon)| \le M|g(\varepsilon)|.
$$
We write $f(\varepsilon) = o(g(\varepsilon))$ as $\varepsilon \rightarrow \varepsilon_0$ if 
$$
\lim\limits_{\varepsilon \rightarrow \varepsilon_0}\left|\frac{f(\varepsilon)}{g(\varepsilon)}\right| = 0.
$$
#### Remarks
- If $\lim\limits_{\varepsilon\rightarrow\varepsilon_0}\left|\frac{f(\varepsilon)}{g(\varepsilon)}\right|$ exists and is finite, then $f(\varepsilon) = O(g(\varepsilon))$
- The notation $f(\varepsilon) = O(g(\varepsilon))$ means that functions $f$ and $g$ are of the same size or order.
- The notation $f(\varepsilon) = o(g(\varepsilon))$ means that $f$ is much smaller than $g$, or $f$ goes to $0$ faster than $g$. We can also write $f <\!\!< g$.
- The notation $f(\varepsilon) = O(1)$ means that $f$ is bounded in the neighbourhood of $\varepsilon_0$.
- The notation $f(\varepsilon) = o(1)$ means that $f(\varepsilon)\rightarrow0$ as $\varepsilon\rightarrow\varepsilon_0$.

### Def 1.2 Asymptotic approximation
We call a function $g$ an asymptotic approximation of $f$ for $\varepsilon\rightarrow\varepsilon_0$ if
$$
f(\varepsilon) = g(\varepsilon) + o(g(\varepsilon))
$$
and then we write $f(\varepsilon) \sim g(\varepsilon)$.

#### Example 1
Verify that $\varepsilon^2\ln(\varepsilon) = o(\varepsilon)$ as $\varepsilon\rightarrow0$. I'm not writing all of that, just compute the limit, use L'Hopital.

#### Example 2
Verify that $\sin(\varepsilon) = O(\varepsilon)$. We know that
$$
\lim\limits_{\varepsilon\rightarrow0}\frac{\sin(\varepsilon)}{\varepsilon} = 1,
$$
so we get the result by the first remark.

### Def 1.3 O/o uniform
We write $f(x; \varepsilon) = O(g(x; \varepsilon))$ as $\varepsilon\rightarrow\varepsilon_0$ and $x \in \mathbb{I}$ if there exists a positive function $M(x)$ on $\mathbb{I}$ such that 
$$
f(x; \varepsilon) \le M(x)|g(x; \varepsilon)|,
$$
for all $\varepsilon$ in some neighbourhood of $\varepsilon_0$ and all $x\in\mathbb{I}$.
If $M(x)$ is a bounded function on $\mathbb{I}$, then we write $f(x; \varepsilon) = O(g(x; \varepsilon))$ as $\varepsilon\rightarrow\varepsilon_0$ **uniformly** on $\mathbb{I}$.

We write $f(x; \varepsilon) = o(g(x; \varepsilon))$ as $\varepsilon\rightarrow\varepsilon_0$ and $x\in\mathbb{I}$ if 
$$
\lim\limits_{\varepsilon\rightarrow\varepsilon_0} \left|\frac{f(x; \varepsilon)}{g(x; \varepsilon)}\right| = 0
$$
pointwise on $\mathbb{I}$.
If the limit is uniform on $\mathbb{I}$, we write $f(x; \varepsilon) = o(g(x; \varepsilon))$ as $\varepsilon\rightarrow\varepsilon_0$ **uniformly** on $\mathbb{I}$.

### Def 1.4 Uniformly valid asymptotic approximation
We say that a function $g$ is a **uniformly valid asymptotic approximation** to a function $f$ on $\mathbb{I}$ as $\varepsilon\rightarrow\varepsilon_0$ if the error $e(x; \varepsilon) = f(x; \varepsilon) - g(x; \varepsilon)$ converges to $0$ as $\varepsilon\rightarrow\varepsilon_0$ uniformly.

#### Example
Let $f(x; \varepsilon) = \exp(-\varepsilon x)$ for $x > 0$ and $0 < \varepsilon <\!\!< 1$ . The first terms of the Taylor expansion in powers of $\varepsilon$ provide an approximation $g(x; \varepsilon) = 1 - \varepsilon x + \frac{1}{2}x^2\varepsilon^2$

I'm not writing all of that, just compute the error (it's not uniform, just pointwise).

### Def 1.5 Asymptotic sequence
A sequence of function $\{\phi_i\}$ is an asymptotic sequence as $\varepsilon \rightarrow \varepsilon_0$ and $x \in \mathbb{I}$ if
$$
\phi_{i+1}(x; \varepsilon) = o(\phi_i(x; \varepsilon)), \quad \text{ as } \varepsilon \rightarrow \varepsilon_0.
$$

### Def 1.6 Asymptotic expansion
Given an asymptotic sequence $\{\phi_i\}$, we say that a function $f$ has an asymptotic expansion to $n$ terms with respect to the sequence $\{\phi_i\}$ if
$$
f(x; \varepsilon) = \sum_{i=1}^ka_i\phi_i(x; \varepsilon) + o(\phi_k(x; \varepsilon))
$$
for $k=1,\dots,n$, and $\varepsilon \rightarrow \varepsilon_0$, where the coefficients $a_i$ are independent on $\varepsilon$. In this case we write
$$
f(x; \varepsilon) \sim \sum_{i=1}^na_i\phi_i(x, \varepsilon).
$$
The functions $\phi_i$ are called scale or basis functions.

#### Remark
Frequently we use the power functions $\phi_i(\varepsilon) = \varepsilon^{\alpha i}$ where $\alpha_i < \alpha_{i+1}$, as basis functions. An asymptotic expansion using such functions is called Poincare expansion.

#### Example
$$
\sin(\varepsilon) \sim \sum_{i=0}^na_i\varepsilon^{2i + 1}, \text{ with } a_i = \frac{(-1)^i}{(2i + 1)!}.
$$
#### Example
Let's consider the error function
$$
erf(x) = \frac{2}{\sqrt{\pi}}\int_0^xe^{-t^2}dt.
$$
How do we approximate this function?

The first idea is to expand the integrand into its Taylor series:
$$
e^{-t^2} = \sum_{k=0}^\infty\frac{(-t^2)^k}{k!},
$$
and then integrate:
$$
E_n(x) = \frac{2x}{\sqrt{\pi}}\sum_{k=0}^n\frac{-x^{2k}}{k!(2k+1)}.
$$
We may expand that $E_n(x) \rightarrow erf(x)$ as $n \rightarrow \infty$, but the convergence rate is shit.

The second idea consists on constructing an asymptotic expansion for $x >\!\!>1$. To do so we write
$$
erf(x) = \frac{2}{\sqrt{\pi}}\int_0^xe^{-t^2}dt = \frac{2}{\sqrt{\pi}}\int_0^\infty e^{-t^2}dt - \frac{2}{\sqrt{\pi}}\int_x^\infty e^{-t^2}dt = 1 - \frac{2}{\sqrt{\pi}}\int_x^\infty e^{-t^2}dt.
$$
Then we integrate with $u = t^2 - x^2$
$$
\int_x^\infty e^{-t^2}dt = \int_0^\infty \frac{1}{2x}e^{-x^2}e^{-u}\left(1 + \frac{u}{x^2}\right)^{-\frac{1}{2}}du.
$$
Next we use the generalised binomial $(1+y)^\alpha = \sum_{k=0}^\infty {\alpha \choose k}y^k$, with $\alpha = -\frac{1}{2}$. We note that
$$
{-\frac{1}{2}\choose k} = \frac{(-1)^k}{\sqrt{\pi}k!}\Gamma\left(\frac{1}{2} + k\right),
$$
then we get
$$
\int_0^\infty\frac{e^{-x^2}}{2\sqrt{\pi}x}e^{-u}\sum_{k=0}^n\frac{1}{k!}\Gamma\left(\frac{1}{2} + k\right)\left(-\frac{u}{x^2}\right)^kdu = \frac{e^{-x^2}}{2\sqrt{\pi}x}\sum_{k=0}^n\Gamma\left(\frac{1}{2} + k\right)(-x)^{2k}\Gamma(k + 1).
$$
Then the second expansion of $erf$ is 
$$
E_n(x) = 1 - \frac{e^{-x^2}}{\pi x}\sum_{k=0}^n\Gamma\left(\frac{1}{2} + k\right)(-x)^{2k}k!.
$$

#### Remarks
- Asymptotic expansions need not to be convergent with an increasing number of terms ($n \rightarrow \infty$).
- Asymptotic expansions can be added and multiplied, if they are obtained in a special way.
- In general, we can not differentiate asymptotic expansions, but if 
  $$
	f(x; \varepsilon) \sim \sum_{i=1}^n a_i\phi_i(x; \varepsilon),
	$$
	and 
	$$
	\frac{\partial f}{\partial x}(x; \varepsilon) \sim \sum_{i=1}^n b_i(x)\phi(x; \varepsilon)
	$$
	then $b_i = \frac{\partial}{\partial x}a_i$.
- Asymptotic expansions can be integrated
  $$
  \int_a^bf(x; \varepsilon)dx \sim \sum_{i=1}^n\int_a^ba_i(x)\phi_i(x; \varepsilon).
  $$
# 2. Asymptotic solutions of algebraic equations
#### Example
Suppose we want to solve the following equation
$$
x^2 - 3.99x + 3.02 = 0.
$$
Then we may introduce $\varepsilon = 0.01$, and rewrite this equation to 
$$
x^2 + (\varepsilon - 4)x + (3 + 2\varepsilon) = 0.
$$
We want to find the asymptotic approximation of its solution.
The unperturbed problem is
$$
x^2 - 4x + 3 = 0,
$$
and it has solutions $x_0 = 1$, and $x_0 = 3$.
Using power functions as basis, we consider the following approximation
$$
x_\varepsilon \sim x_0 + a_1\varepsilon^{\alpha_1} + a_2\varepsilon^{\alpha_2}.
$$
I'm not writing all of that, insert $x_\varepsilon$ approximation above into the rewritten equation, should be $\sim$ to $0$. We should get $\alpha_1 = 1, \alpha_2 = 2, a_1 = -\frac{5}{2}, a_2 = -\frac{15}{8}$.

#### Example
Consider the quadratic equation
$$
(1-\varepsilon)x^2 - 2x + 1 = 0.
$$
Setting $\varepsilon = 0$ we get the unperturbed problem
$$
x^2 - 2x + 1 = (x - 1)^2 = 0
$$
with a double root $x = 1$. Assume that the asymptotic expansion takes the form
$$
x(\varepsilon) \sim 1 + \varepsilon a_1 + \varepsilon^2 a_2.
$$
Substituting $x(\varepsilon)$ back to the quadratic equation we get something nasty again. Comparing the coefficients at $\varepsilon^n$ we find a contradiction in $\varepsilon^1$ case. So $x(\varepsilon)$ can't be the asymptotic expansion.

Looking for an exact solution of the quadratic we get
$$
x_1 = \frac{1 + \sqrt{\varepsilon}}{1 - \varepsilon}, \quad x_2 = \frac{1 - \sqrt{\varepsilon}}{1 - \varepsilon},
$$
which is kinda sus, and the expansion with integer powers is like a five block jump, impossible.

Now let 
$$
x(\varepsilon) \sim 1 + \varepsilon^\frac{1}{2} a_1 + \varepsilon a_2 + \varepsilon^\frac{3}{2} a_3.
$$
Substitute this back into quadratic again, and get a horrible atrocity that should not be seen by any mortal man.

#### Example
Consider the equation
$$
\varepsilon x^3 - x + 1 = 0. 
$$
We seek the asymptotic expansion:
$$
x(\varepsilon) \sim a_0 + \varepsilon a_1 + \varepsilon^2 a_2.
$$
Inserting this into the original equation and equating the coefficients of $\varepsilon^n$ we get:
$$
a_1 + 1 = 0, \quad a_1 + a_0^3 = 0, \quad a_2 + 3a_0^2a_1 = 0,
$$
so
$$
x(\varepsilon) = 1 + \varepsilon + 3\varepsilon^2 + O(\varepsilon^3).
$$
To find the remaining roots of the original equation we introduce
$$
x(\varepsilon) = \frac{y(\varepsilon)}{\delta(\varepsilon)}
$$
and substitute it into the original equation.
$$
\varepsilon \frac{y^3}{\delta^3} - \frac{y}{\delta} + 1 = 0.
$$
We need to find $\delta(\varepsilon)$ such that
$$
\frac{\varepsilon}{\delta^3(\varepsilon)} \sim \frac{1}{\delta(\varepsilon)}
$$
and $1$ should be small compared to $\frac{\varepsilon}{\delta^3(\varepsilon)}$ and $\frac{\varepsilon}{\delta(\varepsilon)}$. Then we get $\delta^2(\varepsilon) \sim \varepsilon$ which implies that $\delta(\varepsilon) \sim \sqrt{\varepsilon}$. Taking this into account in the equation for $y$, we get
$$
y^3 - y + \sqrt{\varepsilon} = 0.
$$
Now we want to find the asymptotic expansions for the roots of the above equation. We assume
$$
y(\varepsilon) \sim b_0 + b_1 \varepsilon^\frac{1}{2}.
$$
Then something happens, and we get
$$
x(\varepsilon) = \pm \varepsilon^{-\frac{1}{2}} + \frac{1}{4} + O(\varepsilon^\frac{1}{2}).
$$

#### Example
Consider the algebraic equation $g(x; \varepsilon) = 0$, where $g$ is a function having derivatives of all orders. Assuming $g(x_0; 0) = 0$ is solvable for $x_0$, show how to find a three term asymptotic expansion of the form $x = x_0 + \varepsilon x_1 + \varepsilon^2 x_2$.

We introduce the function $h(\varepsilon) = g(x(\varepsilon), \varepsilon) = 0$, and expand it into the Taylor series
$$
h(\varepsilon) = \sum_{n=0}^\infty \frac{h^{(n)}(0)}{n!}\varepsilon^n = 0.
$$
Using the chain rule 
$$
\begin{aligned}
h'(\varepsilon) &= \frac{\partial g}{\partial x}(x(\varepsilon), \varepsilon)x'(\varepsilon) + \frac{\partial g}{\partial\varepsilon}(x(\varepsilon), \varepsilon) \\
h''(\varepsilon) &= \frac{\partial^2g}{\partial \varepsilon^2}(x(\varepsilon), \varepsilon) = \text{even worse mess}.
\end{aligned}
$$

Finally we get
$$
\begin{aligned}
h(0) = 0 &\implies g(x_0, 0) = 0, \\
h'(0) = 0 &\implies \frac{\partial g}{\partial x}(x_0, 0)x_1 + \frac{\partial g}{\partial \varepsilon}(x_0, 0) = 0,
\end{aligned}
$$
# 3. Regular perturbations of ODEs

#### Example
Consider the ODE:
$$
\begin{aligned}
y' &= -y + \varepsilon y^2, \quad t > 0, \\
y(0) &= 1.
\end{aligned}
$$
It's the Bernoulli equation, and it can be solved analytically by substitution $u = y^{-1}$.
We get the solution:
$$
y(t) = \frac{1}{\varepsilon + (1-\varepsilon)e^t}.
$$
The exact solution can be expanded in a Taylor series in powers of $\varepsilon$:
$$
y(t) = e^{-t} + \varepsilon(e^{-t} - e^{-2t}) + e^2(e^{-t} - e^{-2t} + e^{-3t}) + \cdots.
$$
Now, let's try to apply the regular perturbation method to obtain an asymptotic approximation of $y$. To do so, we assume that
$$
y(t) = y_0(t) + \varepsilon y_1(t) + \varepsilon^2 y_2(t) + \cdots.
$$
The functions $y_0, y_1, y_2$ can be determined by substituting the above into the original equation and then equating coefficients of equal powers of $\varepsilon$:
$$
y_0' + \varepsilon y_1' + \varepsilon^2 y_2' + y_0 + \varepsilon y_1 + \varepsilon^2 y_2 - \varepsilon (y_0 + \varepsilon y_1 \varepsilon^2 y_2)^2 = 0.
$$
Collecting the coefficients we obtain the sequence of linear equations
$$
\begin{aligned}
y_0' + y_0 = 0, &\quad y_0(0) = 1, \\
y_1' + y_1 = y_0^2, &\quad y_1(0) = 0, \\
y_2' + y_2 = 2y_0y_1, &\quad y_2(0) = 0.
\end{aligned}
$$
Solving these we obtain
$$
y_0(t) = e^{-t}, \quad y_1(t) = e^{-t} - e^{-2t}, \quad y_2(t) = e^{-t} - 2e^{-2t} + e^{-3t}.
$$
We can see that we got the first three terms in the Taylor expansion of $y$.

#### Example
Consider the nearly linear system of ODEs
$$
u' = Au + \varepsilon f(t, u, \varepsilon), \quad u(0) = \alpha.
$$
where $0 < \varepsilon <\!< 1, u:[0,T]\rightarrow\mathbb{R}^n, A\in\mathbb{R}^{n \times m}, \alpha\in\mathbb{R}^n$, and $f$ is Lipschitz w.r.t $u$.
We seek an asymptotic expansion of the form $u(t) \sim u_0(t) + \varepsilon u_1(t)$. Then the correctors satisfy
$$
u_0' = Au_0, \quad u_0(0) = \alpha,
$$
so $u_0(t) = \alpha e^{At}$, and
$$
u_1' = Au_1 + f(t, u_0, \varepsilon), \quad u_1(0) = 0,
$$
so $u_1(t) = \int_0^te^{A(t-s)}f(s, \alpha e^{As}, \varepsilon)ds$.
Now, we seek an estimate for the error
$$
R(t, \varepsilon) = u(t) - (u_0(t) + \varepsilon u_1(t)).
$$
To do this, we will need the two following lemmas.

### Lemma 3.1
Let $r \in C^1(\mathbb{R}, \mathbb{R}^n)$. Then $||r||^2 = r_1^2(t) + \cdots + r_n^2(t)$, $||r||$ is right-differentiable for all $t$, i.e
$$
\lim\limits_{\tau \rightarrow 0^+}\frac{||r(t + \tau) - ||r(t)||}{\tau}
$$
is finite, and differentiable for all $t$ where $r(t) \ne 0$. Moreover, the following inequality holds for all $t$
$$
\frac{d}{dt}||r(t)|| \le ||r'(t)||.
$$

### Lemma 3.2 (Gronwell inequality)
If $\varphi' \le \alpha \varphi + \beta$ and $\varphi(0) = \varphi_0$, then 
$$
\varphi(t) \le \varphi_0 e^{\alpha t} + \frac{\beta}{\alpha}(e^{\alpha t} - 1).
$$

### Theorem 3.3
Consider 
$$
u' = Au + \varepsilon f(t, u, \varepsilon), \quad u(0) = \alpha.
$$
Then 
$$
||R(t, \varepsilon)|| \le \varepsilon^2\frac{LM}{||A|| + \varepsilon L}\left(e^{t(||A|| + \varepsilon L)} - 1\right),
$$
where $L$ is the Lipschitz constant of $f$ w.r.t. the second variable and $M = \max\limits_{t\in[0, T]} ||u_1(t)||$.

# 4 Nonlinear oscillations and Poincaré-Lindstedt method

Consider the equation
$$
\begin{aligned}
y'' + y + \varepsilon y^3 &= 0 \\
y(0) = 1, \; y'(0) &= 0
\end{aligned}
$$
We have
$$
y_0'' + y_0 = 0, \;\; y_0(0) = 1, y_0'(0) = 0,
$$
and
$$
y_1'' + y_1 = y_0^3, \;\; y_1(0) = 0, y_1'(0) = 0.
$$
The equations can be solved analytically, yielding
$$
y_0(t) = \cos(t)
$$
and
$$
y_1(t) = \frac{1}{32}\left(\cos(3t) - \cos(t) \right) - \frac{3}{8}t\sin(t).
$$
Note the secular term $t\sin(t)$ which goes to infinity as $t$ goes to infinity.

The idea of the Poincaré-Lindstedt method is to introduce a d???ed time scale in the perturbation sense
$$
y(t) = y_0(\tau) + \varepsilon y_1(\tau) + \varepsilon^2 y_2(\tau) + \cdots
$$
with
$$
\tau = \omega t, \quad \omega = \omega_0 + \varepsilon\omega_1 + \varepsilon^2\omega_2 + \cdots.
$$
We plug that into the equation and collect the coefficients with the same power of $\varepsilon$. Voila.
The solution to the original equation using this method yield
$$
y_0(\tau) = \cos(\tau),
$$
$$
y_1(\tau) = \frac{1}{32}\left(\cos(3\tau) - \cos(\tau)\right).
$$
In general the Poincaré-Lindstedt method works for equations of the following form:
$$
y'' + \omega^2y = \varepsilon f(t, y, y'), \; 0 < \varepsilon << 1.
$$

# 5 Singular perturbation of ODEs
#### Example
Consider the boundary value problem
$$
\varepsilon y'' + (1 + \varepsilon)y' + y = 0, \quad y(0) = 0, \quad y(1) = 1.
$$
Let's try to apply the regular perturbation method. Assume a perturbation of the form
$$
y(x) = y_0(x) + \varepsilon y_1(x) + \varepsilon^2 y_2(x) + \cdots.
$$
Then substituting into the ODE we get
$$
\varepsilon \left( y_0'' + \varepsilon y_1'' + \varepsilon^2 y_2'' \right) + \left(y_0' + \varepsilon y_1' + \varepsilon^2 y_2'\right) + \varepsilon \left( y_0' + \varepsilon y_1' + \varepsilon^2 y_2' \right) + \left(y_0 + \varepsilon y_1 + \varepsilon^2 y_2\right) = 0.
$$
Collecting the terms with the same powers of $\varepsilon$, we get:
$$
y_0' + y_0 = 0, \quad y_0(0) = 0, \quad y_0(1) = 1.
$$
The general solution for the $y_0$ ODE is $y_0(x) = ce^{-x}$, which cannot exist with the given conditions. Hence, the regular perturbation method fails in the first step.

Let's examine the perturbed problem. The exact solution to the ODE is 
$$
y(x) = \frac{1}{e^{-1} - e^{\frac{1}{\varepsilon}}}\left(e^{-x} - e^{-\frac{x}{\varepsilon}}\right).
$$
We may try to estimate the size of the terms in the ODE. We have
$$
y'(x) = \frac{1}{e^{-1} - e^{\frac{1}{\varepsilon}}}\left(-e^{-x} - \frac{1}{\varepsilon}e^{-\frac{x}{\varepsilon}}\right),
$$
and
$$
y''(x) = \frac{1}{e^{-1} - e^{\frac{1}{\varepsilon}}}\left(e^{-x} - \frac{1}{\varepsilon^2}e^{-\frac{x}{\varepsilon}}\right).
$$
Suppose $\varepsilon$ is small and $x$ is in the boundary layer. We can set $x = \varepsilon$, then
$$
y''(\varepsilon) = \frac{1}{e^{-1} - e^{\frac{1}{\varepsilon}}}\left(e^{-\varepsilon} - \frac{1}{\varepsilon^2}e^{-1}\right) = O(\varepsilon^{-2}).
$$
Note that $\varepsilon y''(\varepsilon)$ is not small.

Suppose $\varepsilon$ is small and $x$ is away from the boundary layer. Let's just set $x = \frac{1}{2}$. Then
$$
y\left(\frac{1}{2}\right) = \frac{1}{e^{-1} - e^{-\frac{1}{\varepsilon}}}\left(e^{-\frac{1}{2}} - \frac{1}{\varepsilon^2}e^{-\frac{1}{2\varepsilon}}\right) = O(1).
$$
Then $\varepsilon y''\left(\frac{1}{2}\right)$ is small.

This analysis suggests that in the outer layer the leading-order problem $y_0' + y_0 = 0$, is a valid approximation provided that $y_0(1) = 1$. Then $y_{out}(x) = e^{1-x}$ is our outer approximation of $y$.

In general, to find an approximate solution of the singular perturbation problem we proceed in four steps:
1. Find the outer approximation.
2. Find the inner approximation.
3. Matching.
4. Composite expansion (uniformly valid approximation).

In our particular case we have:

Outer approximation: $y_{out}(x) = e^{1-x}$.

Inner approximation
The previous analysis we know that on the boundary layer we have to introduce proper scaling. We introduce the change of variables 
$$
\xi = \frac{x}{\delta(\varepsilon)},
$$
$$
Y(\xi) = y(\delta(\varepsilon)\xi).
$$
Then the ODE becomes
$$
\frac{\varepsilon}{\delta(\varepsilon)^2}Y''(\xi) + \frac{1+\varepsilon}{\delta(\varepsilon)}Y'(\xi) + Y(\xi) = 0.
$$
To determine the scale factor $\delta(\varepsilon)$ we consider all possible dominant balances between pairs of coefficients. We want
$$
\frac{\varepsilon}{\delta(\varepsilon)^2} \sim \frac{1}{\delta(\varepsilon)},
$$
but keep $\frac{\varepsilon}{\delta(\varepsilon)}$ and $1$ small in comparison. Then we get
$$
\delta(\varepsilon) \sim \varepsilon.
$$
We also might want
$$
\frac{\varepsilon}{\delta(\varepsilon)^2} \sim 1,
$$
but keep $\frac{1}{\delta(\varepsilon)}$ and $\frac{\varepsilon}{\delta(\varepsilon)}$ small in comparison. Then we get
$$
\delta(\varepsilon) \sim \sqrt{\varepsilon}.
$$
but this does not satisfy our needs of "small in comparison".

We also might want
$$
\frac{\varepsilon}{\delta(\varepsilon)^2} \sim \frac{\varepsilon}{\delta(\varepsilon)},
$$
but keep $\frac{1}{\delta(\varepsilon)}$ and $1$ small in comparison. Then we get
$$
\delta(\varepsilon) \sim 1,
$$
but this does not satisfy our needs of "small in comparison".

So only the first method will work for us. We can set $\delta(\varepsilon) = \varepsilon$.
Therefore, we get
$$
\frac{1}{\varepsilon}Y''(\xi) + \frac{1}{\varepsilon}Y'(\xi) + Y'(\xi) + Y(\xi) = 0.
$$
Then multiply the equation by $\varepsilon$ and voila.

We apply the regular perturbation method to get the approximate solution of the rescaled problem.
$$
Y_0'' + Y_0' = 0,
$$
so we get
$$
Y_0(\xi) = C_1 + C_2e^{-\xi}.
$$
To determine one constant in the general solution we apply the boundary condition
$$
Y_0(0) = 0.
$$
So then we have $C_2 = -C_1$, and
$$
Y_0(\xi) = C_1\left(1 - e^{-\xi}\right)
$$
and the inner approximation is
$$
y_{in}(x) = C_1\left(1 - e^{-\frac{x}{\varepsilon}}\right).
$$

We will determine the constant $C_1$ in the third step: matching.
We expect that $y_{in}$ and $y_{out}$ will match in the overlapped domain. We introduce yet another variable
$$
\eta = \frac{x}{\sqrt{\varepsilon}},
$$
and then for fixed $\eta$ we want to have
$$
\lim\limits_{\varepsilon \rightarrow 0}y_{out}(\sqrt{\varepsilon}\eta) = \lim\limits_{\varepsilon \rightarrow 0}y_{in}(\sqrt{\varepsilon}\eta).
$$
We have
$$
\lim\limits_{\varepsilon\rightarrow0}y_{out}(\sqrt{\varepsilon}\eta) = \lim\limits_{\varepsilon\rightarrow0} e^{1 - \sqrt{\varepsilon}\eta} = e.
$$
$$
\lim\limits_{\varepsilon\rightarrow0}y_{in}(\sqrt{\varepsilon}\eta) = \lim\limits_{\varepsilon\rightarrow0}C_1\left(1-e^{-\frac{\eta}{\sqrt{\varepsilon}}}\right) = e.
$$
Then $y_{in}(x) = e\left(1 - e^{-\frac{x}{\varepsilon}}\right)$.

Now we want to determine the composite expansion.
$$
y_u(x) = y_{out}(x) + y_{in}(x) - \text{"common part"}.
$$
In our case we have
$$
y_u(x) = e^{1-x} + e - e^{1 - \frac{x}{\varepsilon}} - \varepsilon = e\left(e^{-x} - e^{-\frac{x}{\varepsilon}}\right).
$$

In general, we can define the matching condition in an alternative way:
$$
\lim\limits_{x \rightarrow 0^+}y_{out}(x) = \lim\limits_{\xi \rightarrow \infty} Y_{in}(\xi).
$$
### The general procedure
If the boundary layer is at the right point, say $x=x_0$, to find an inner approximation we introduce the scaled variable 
$$
\xi = \frac{x - x_0}{\delta(\varepsilon)}.
$$
Then $Y(\xi) = y(x_0 + \xi\delta(\varepsilon))$. The matching condition is
$$
\lim\limits_{x \rightarrow x_0}y_{out}(x) = \lim\limits_{\xi \rightarrow \infty}Y(\xi).
$$
### Theorem 5.1
Consider the boundary value problem
$$
\varepsilon y'' + p(x)y' + q(x)y = 0, \quad y(0) = a, \quad y(1) = b,
$$
where $p$ and $q$ are continuous functions on $[0, 1]$, and $p(x) > 0$ for all $x \in [0, 1]$. Then there exists a boundary layer at $x = 0$ with the inner and outer approximations given by
$$
y_{in}(x) = C_1 + (a - C_1)\exp\left(\frac{-p(0)x}{\varepsilon}\right),
$$
$$
y_{out}(x) = b\exp\left(-\int_x^1\frac{q(s)}{p(s)}ds\right),
$$
where
$$
C_1 = b\exp\left(\int_0^1\frac{q(s)}{p(s)}ds\right).
$$

We note that if $p(x)<0$ on $[0,1]$, then no matching would be possible.
On the other hand, matching would be possible in this case if the boundary layer is $x=1$.

In summary, if $p(x) > 0$ for all $x \in [0, 1]$, then the boundary layer is at $x=0$, and if $p(x)<0$ for all $x\in[0, 1]$ then the boundary layer is at $x=1$.

### Multiple boundary layer
Consider the problem
$$
\varepsilon^2y'' + \varepsilon xy' - y = -e^x, \quad y(0) = 2, \quad y(1) = 1.
$$
We start with the outer approximation. By setting $\varepsilon=0$, we get $y_{out}(x)=e^x$. This function cannot satisfy either boundary condition.

Now we proceed with the inner approximation.
First, consider the case when the boundary layer is at $x=0$. We introduce
$$
\xi = \frac{x}{\varepsilon^\alpha}, \quad Y(\xi) = y(\varepsilon^\alpha \xi).
$$
Then we get
$$
\varepsilon^{2-2\alpha} Y'' + \varepsilon \xi Y' - Y = -e^{\varepsilon^\alpha\xi}.
$$
We get $\alpha = 1$ for the inner approximation. Then we get
$$
Y'' + \varepsilon \xi Y' - Y = -e^{\varepsilon \xi}.
$$
The inner approximation at $x = 0$ satisfies 
$$
Y_0'' - Y_0 = -1, \quad Y_0(0) = 2.
$$
Then the solution is 
$$
Y_0(\xi) = 1 + Ce^{-\xi} + (1-C)e^\xi.
$$
For matching we consider the following limits:
$$
\lim\limits_{x \rightarrow 0}y_{out}(x) = \lim\limits_{\xi \rightarrow \infty}Y_0(\xi)
$$
In order for $(1-C)e^\xi$ term to not explode, just set $C=1$, then we get
$$
Y_0(\xi) = 1 + e^{-\xi}.
$$

To determine the approximation at the boundary $x=1$, we introduce 
$$
\xi = \frac{x-1}{\varepsilon^\beta}, \quad W(\xi) = y(1 + \xi\varepsilon^\beta).
$$
We get the following equation for $W$:
$$
\varepsilon^{2-2\beta}W'' + (1 + \varepsilon\xi)\varepsilon^{1-\beta}W' - W = e^{1+\varepsilon^\beta\xi}.
$$
The method of dominant balance leads to $\beta = 1$. Then the equation for an inner approximation at $x=1$ is 
$$
W_0'' + W_0 - W_0 = -e, \quad W_0(0) = 1, \quad -\infty < \xi < 0.
$$
The solution of the above equation is given by
$$
W_0(\xi) = e + B\exp\left(\frac{-1+\sqrt{5}}{2}\xi\right) + (1 - e - B)\exp\left(-\frac{-1+\sqrt{5}}{2}\xi\right).
$$
Then the matching condition is
$$
e = \lim\limits_{x\rightarrow1}y_{out}(x) = \lim\limits_{\xi\rightarrow-\infty}W_0(\xi).
$$
We set $1 - e - B = 0$, so $B = 1 - e$. 
Finally, the uniform approximation is given by 
$$
y_u(x) = y_{out}(x) + Y_0\left(\frac{x}{\varepsilon}\right) + W_0\left(\frac{x-1}{\varepsilon}\right) - 1 - e.
$$