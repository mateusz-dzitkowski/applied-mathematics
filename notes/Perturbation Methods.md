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

# Asymptotic approximation of integrals
We will consider integrals of the form
$$
I(\lambda) = \int_a^bf(t)e^{-\lambda g(t)}dt
$$
with $\lambda >> 1$, or $\lambda = \frac{1}{\varepsilon}$, and where $g$ is a strictly increasing function on $[a, b]$ and $g'$ is continuous, $a < b \le \infty$.

#### Example (The Laplace transform)
$$
\mathcal{U}(\lambda) = \int_0^\infty f(t)e^{-\lambda t}dt.
$$
We note that it is sufficient to examine integrals of the form
$$
I(\lambda) = \int_0^b f(t)e^{-\lambda t}dt.
$$
By substitution $s(t) = g(t) - g(a)$, where $t=t(s)$ is a solution of $s(t)=g(t)-g(a)$ for $t$ we get
$$
I(\lambda) = e^{-\lambda g(a)}\int_0^{g(b)-g(a)}\frac{f(t(s))}{g'(t(s))}e^{-\lambda s}ds
$$
The fundamental idea in finding an approximation for $I(\lambda)$ is to determine what subinterval gives the dominant contribution. We see that $e^{-\lambda t}$ is rapidly decreasing for large $\lambda$, thus the main contribution comes from the neighbourhood of $t=0$.

#### Example
Consider the integral
$$
I(\lambda) = \int_0^\infty\frac{\sin(t)}{t}e^{-\lambda t}dt.
$$
We can split the integral into two parts
$$
I(\lambda) = \int_0^T\frac{\sin(t)}{t}e^{-\lambda t}dt + \int_T^\infty\frac{\sin(t)}{t}e^{-\lambda t}dt.
$$
We observe that 
$$
\left|\int_T^\infty\frac{\sin(t)}{t}e^{-\lambda t}dt\right| \le \max\limits_{t\in[T, \infty]}\left|\frac{\sin(t)}{t}\right|\left|\int_T^\infty e^{-\lambda t} dt\right| \le \left|\int_T^\infty e^{-\lambda t} dt\right| \le \left|-\frac{1}{\lambda}e^{-\lambda T}\right| = o(\lambda^{-m})
$$
for any $m>0$. Thus, we have
$$
I(\lambda) = \int_0^T\frac{\sin(t)}{t}e^{-\lambda t}dt + o(\lambda^{-m}).
$$
In $[0, T]$ we approximate $\frac{\sin(t)}{t}$ by its Taylor series around $t=0$.
$$
\frac{\sin(t)}{t} = 1 - \frac{t^2}{3!} + O(t^4).
$$
Thus,
$$
I(\lambda) = \int_0^T\left(1 - \frac{t^2}{3!} + O(t^4)\right)e^{-\lambda t} dt + o(\lambda^{-m}).
$$
Then we introduce a variable $u=\lambda t$, $du = \lambda dt$:
$$
I(\lambda) = \frac{1}{\lambda}\int_0^{\lambda T}\left(1 - \frac{t^2}{\lambda^23!} + O\left(\frac{1}{\lambda^4}\right)\right)e^{-u}du.
$$
We use the formula
$$
\int_0^\infty u^me^{-u}du = m!.
$$
Then
$$
I(\lambda) \sim \frac{1}{\lambda} - \frac{2!}{3!\lambda^3} + O\left(\frac{1}{\lambda^5}\right).
$$
### Def
The gamm function is defined by 
$$
\Gamma(x) = \int_0^\infty u^{x-1}e^{-u}du, \quad x>0,
$$
and has the property $\Gamma(x+1) = x\Gamma(x)$. In particular
$$
\Gamma(n) = (n-1)!, \quad n\in\mathbb{N},
$$
$$
\Gamma\left(\frac{1}{2}\right) = \sqrt\pi.
$$
### Theorem (Watson's Lemma)
Consider the integral
$$
I(\lambda) \int_0^bt^\alpha h(t) e^{-\lambda t}dt,
$$
where $\alpha > -1$, $h$ has a Taylor series expansion around $t=0$ with $h(0)\ne0$, and $|h(t)|<ke^{ct}$ on $[0, b]$ for some positive constants $k$ and $c$. Then
$$
I(\lambda) \sim \sum_{n=0}^\infty\frac{h^{(n)}(0)}{n!}\frac{\Gamma(\alpha + n + 1)}{\lambda^{\alpha + n + 1}}.
$$
#### Example
Consider the error function
$$
erfc(\lambda) = \frac{2}{\sqrt\pi}\int_\lambda^\infty e^{-s^2}ds.
$$
We note that this integral can be transformed to the required form by substitution $t=s-\lambda$:
$$
erfc(\lambda) = \frac{2}{\sqrt\pi}e^{-\lambda^2}\int_0^\infty e^{-t^2} e^{-2\lambda t}dt = \frac{2}{\sqrt\pi}e^{-\lambda^2}\int_0^\infty e^{-\frac{\tau^2}{4}}e^{-\lambda\tau}d\tau.
$$
The Wilson's lemma implies that
$$
erfc(\lambda) \sim \frac{2}{\sqrt\pi}e^{-\lambda^2}\left(\frac{1}{2\lambda} - \frac{\Gamma(3)}{(2\lambda)^3} + \frac{\Gamma(5)}{2!(2\lambda)^5} + \cdots\right).
$$
## Integration by parts
Sometimes an asymptotic expansion of integrals can be found by a successive integration by parts.
$$
erfc(\lambda) = \frac{2}{\sqrt\pi}\int_\lambda^\infty e^{-t^2}dt = \frac{2}{\sqrt\pi}\int_\lambda^\infty \frac{-2te^{-t^2}}{-2t}dt
= \frac{2}{\sqrt\pi}\left(\frac{e^{-\lambda^2}}{2\lambda} - \int_\lambda^\infty \frac{e^{-t^2}}{2t^2}dt\right).
$$
We do the same trick to the remaining integral over and over. We note that by repeated integration by parts we can eventually reproduce the asymptotic expansion that we got by the application of the Watson's lemma.

#### Remark
We note that for fixed $\lambda$ the series does not converge, but we can check that after just $5$ terms we obtain $erfc(2)\approx0.004744$, where the exact value is $0.004678$.

#### Remark
Note that in order to get an approximation of $erfc(\lambda)$ we could also proceed as follows:
$$
erfc(\lambda) = \frac{2}{\sqrt\pi}\int_0^\infty e^{-t^2}dt - \frac{2}{\sqrt\pi}\int_0^\lambda e^{-t^2}dt = 1 - \frac{2}{\sqrt\pi}\int_0^\lambda e^{-t^2}dt.
$$
Next we replace $e^{-t^2}$ by its Taylor series and integrate term by term to obtain
$$
erfc(\lambda) = 1 - \frac{2}{\sqrt\pi}\int_0^\lambda\left(1 - \frac{t^2}{2} + \frac{t^2}{2^22!} + \cdots\right)dt = 1 - \frac{2}{\sqrt\pi}\left(\lambda - \frac{\lambda^3}{3} + \frac{\lambda^5}{5\cdot2!} + \cdots\right).
$$
We can show that this series converges, however to get the same accuracy as before, we should take at least $20$ terms.

# The WKB approximation
The WKB (Wentzel-Kramers-Brillouin) method can be applied in particular to the linear differential equations of the following form:
$$
\varepsilon^2 y'' + q(t)y = 0,
$$
$$
y'' + (\lambda^2p(t) - q(t))y = 0,
$$
$$
y'' + q(\varepsilon t)^2 y = 0.
$$
Consider the first equation, with $q(t) = -k^2(t) < 0$, a non-oscillatory case:
$$
\varepsilon y'' - k^2(t) y = 0.
$$
We note that if $k$ is constant, $k(t) = k_0$, the equation would have the solution of the form
$$
y(t) = e^{\pm \frac{k_0}{\varepsilon}t}.
$$
This suggests making the substitution
$$
y(t) = e^{\frac{u(t)}{\varepsilon}}.
$$
Then we have
$$
y'(t) = y(t)\frac{u'(t)}{\varepsilon}, \quad y''(t) = y(t)\left(\left(\frac{u'(t)}{\varepsilon}\right)^2 + \frac{u''(t)}{\varepsilon}\right).
$$
Then, substituting back into the equation, we are left with
$$
\varepsilon v' + v^2 - k^2 = 0, \quad v = u'.
$$
Now we can apply the regular perturbation method to solve this equation. Let
$$
v(t) = v_0(t) + \varepsilon v_1(t) + O(\varepsilon^2).
$$
This gives us
$$
\varepsilon\left(v_0' + \varepsilon v_1'\right) + (v_0 + \varepsilon v_1)^2 - k^2 \sim 0
$$
$$
\varepsilon v_0' + \varepsilon^2 v_1' + v_0^2 + \varepsilon^2 v_1^2 + 2\varepsilon v_0v_1 - k^2 \sim 0.
$$
Equating the same powers of $\varepsilon$ we get
$$
\begin{aligned}
v_0^2 - k^2 &= 0, \\
v_0' + 2v_0v_1 &= 0.
\end{aligned}
$$
The first equation gives us $v_0 = \pm k$, the second one gives us $v_1 = -\frac{1}{2}\frac{k'}{k}$. From the fact that $v = u'$, we get
$$
u(t) = \pm\int_a^t k(s)ds - \frac{\varepsilon}{2}\ln\left(\frac{k(t)}{k(a)}\right) + O(e^2).
$$
Finally we get
$$
y(t) = e^{\frac{u(t)}{\varepsilon}} = \frac{\sqrt{k(a)}}{\sqrt{k(x)}}\exp\left(\pm\frac{1}{\varepsilon}\int_a^tk(s)ds\right)(1 + O(\varepsilon)).
$$
The WKB approximation is the linear combination of these two solutions
$$
y_{WKB}(t) = C_1\frac{\sqrt{k(a)}}{\sqrt{k(x)}}\exp\left(\frac{1}{\varepsilon}\int_a^tk(s)ds\right) + C_2\frac{\sqrt{k(a)}}{\sqrt{k(x)}}\exp\left(-\frac{1}{\varepsilon}\int_a^tk(s)ds\right).
$$
The constants $C_1$ and $C_2$ can be determined by the initial conditions.

#### Example
Find the WKB approximation to
$$
\varepsilon^2 y'' - (1 + t)^2 y = 0,\quad y(0)=1, \quad y(\infty) = 0.
$$
Here, $k(t) = 1 + t$, so $\int_0^tk(s)ds = t + \frac{t^2}{2}$. Hence, our approximation is
$$
y_{WKB}(t) = C_1\frac{1}{\sqrt{1 + t}}\exp\left(\frac{1}{\varepsilon}\left(t + \frac{t^2}{2}\right)\right) + C_2\frac{1}{\sqrt{1 + t}}\exp\left(-\frac{1}{\varepsilon}\left(t + \frac{t^2}{2}\right)\right).
$$
In order to satisfy $y(\infty) = 0$, $C_1$ has to be equal to $0$. Then $y_{WKB}(0) = C_2$, hence $C_2=1$. Finally we get
$$
y_{WKB}(t) = \frac{1}{\sqrt{1 + t}}\exp\left(-\frac{1}{\varepsilon}\left(t + \frac{t^2}{2}\right)\right).
$$

Now let's consider the oscillatory case, $q(t) = k^2(t) > 0$. Then
$$
\varepsilon^2 y'' + k^2(t)y = 0.
$$
To get the WKB approximation we proceed in a similar way as before. We make a substitution
$$
y(t) = e^{i\frac{u(t)}{\varepsilon}}
$$
and get
$$
y_{WKB}(t) = C_1\frac{\sqrt{k(a)}}{\sqrt{k(t)}}\exp\left(\frac{i}{\varepsilon}\int_a^tk(s)ds\right) + C_2\frac{\sqrt{k(a)}}{\sqrt{k(t)}}\exp\left(-\frac{i}{\varepsilon}\int_a^tk(s)ds\right).
$$
Using the Euler formula $e^{ix} = \cos(x) + i\sin(x)$ we can rewrite this $y_{WKB}$ to
$$
y_{WKB}(t) = C_1\frac{\sqrt{k(a)}}{\sqrt{k(t)}}\cos\left(\frac{1}{\varepsilon}\int_a^tk(s)ds\right) + C_2\frac{\sqrt{k(a)}}{\sqrt{k(t)}}\sin\left(\frac{1}{\varepsilon}\int_a^tk(s)ds\right).
$$

#### Example (Schrödinger equation)
$$
-\frac{\hbar^2}{2m}y'' + (V(t) - E)y = 0,
$$
where $\hbar$ is the reduced Planck constant, $m$ is a mass, $V(t)$ is a potential, and $E$ is some constant. In the case $V(t) > E$, we have
$$
y_{WKB}(t) = \frac{A}{(V(t) - E)^{\frac{1}{4}}}\cos\left(\frac{\sqrt{2m}}{\hbar}\int_a^t\sqrt{V(s) - E}ds + \phi\right),
$$
where $A$ and $\phi$ depend on specific initial/boundary conditions.

#### Example
Consider the boundary value problem
$$
y'' + \lambda q(t) y = 0, \quad 0 < t < \pi, \quad y(0) = y(\pi) = 0.
$$
We assume that $q(t) > 0$. 
Here the number $\lambda$ is called the eigenvalue of the equation is there exists a non-trivial solution for that particular value of $\lambda$. The corresponding non-trivial solutions are called eigenfunctions.

We set $\varepsilon = \frac{1}{\sqrt{\lambda}}$ and $k(t) = \sqrt{q(t)}$. Then the equation in question becomes
$$
\varepsilon^2 y'' + k^2(t) y = 0.
$$
If $\varepsilon$ is small, or, equivalently, $\lambda$ is large, then the WKB approximation is given by
$$
y_{WKB}(t) = \left(\frac{q(0)}{q(t)}\right)^\frac{1}{4}\left(C_1\cos\left(\sqrt{\lambda}\int_0^t\sqrt{q(s)}ds\right) + C_2\sin\left(\sqrt{\lambda}\int_0^t\sqrt{q(s)}ds\right)\right).
$$
Since $y(0) = 0$, then $C_1 = 0$, and since $y(\pi) = 0$, then 
$$
C_2\sin\left(\sqrt{\lambda}\int_0^\pi\sqrt{q(s)}ds\right) = 0,
$$
hence, since we don't want trivial solutions, we need $\lambda$ such that
$$
\sqrt{\lambda}\int_0^\pi\sqrt{q(s)}ds = \pi k, \quad k\in\mathbb{Z}.
$$
$$
\lambda = \frac{\pi^2 k^2}{A^2},
$$
where $A = \int_0^\pi\sqrt{q(s)}ds$.
Then the corresponding eigenfunctions have the form
$$
y_{WKB}(t) = C_2\left(\frac{q(0)}{q(t)}\right)^\frac{1}{4}\sin\left(k\pi\frac{\int_0^t\sqrt{q(s)}ds}{\int_0^\pi\sqrt{q(s)}ds}\right).
$$

# Regular perturbations of PDEs

Consider a "near" sphere with a surface given by
$$
S(\theta; \varepsilon) = 1 + \varepsilon P_2(\cos(\theta)),
$$
where $P_2(x) = \frac{1}{2}(3x^2 - 1)$ is the Legendre polynomial of degree $2$.
We assume that the potential outside this perturbed sphere is given by the equation
$$
\Delta u = 0, \quad r > S(\theta, \varepsilon),
$$
$$
u = 1, \quad r = S(\theta, \varepsilon),
$$
$$
\lim\limits_{r \rightarrow \infty} u = 0.
$$
Recall that the Laplacian in spherical coordinates is given by
$$
\Delta u = \frac{1}{r^2}\frac{\partial}{\partial r}\left(r^2\frac{\partial u}{\partial r}\right) + \frac{1}{r^2\sin(\theta)}\frac{\partial}{\partial \theta}\left(\sin(\theta)\frac{\partial u}{\partial \theta}\right) + \frac{1}{r^2\sin(\theta)}\frac{\partial^2 u}{\partial \phi^2},
$$
where $\phi$ is a polar angle, and $\theta$ is an azymuthal angle.

Assuming azymuthal symmetry the Laplacian becomes
$$
\Delta u = \frac{1}{r^2}\frac{\partial}{\partial r}\left(r^2\frac{\partial u}{\partial r}\right) + \frac{1}{r^2\sin(\theta)}\frac{\partial}{\partial \theta}\left(\sin(\theta)\frac{\partial u}{\partial \theta}\right).
$$
We are seeking an asymptotic expansion of the form
$$
u(r, \theta) = u_0(r, \theta) + \varepsilon u_1(r, \theta) + \varepsilon^2 u_2(r, \theta).
$$
Expanding the boundary conditions in a Taylor series we get
$$
1 = u(1 + \varepsilon P_2(\cos(\theta)), \theta) = u(1, \theta) + \varepsilon P_2(\cos(\theta))\frac{\partial u}{\partial r}(1, \theta) + \frac{(\varepsilon P_2(\cos(\theta)))^2}{2}\frac{\partial^2 u}{\partial r^2}(1, \theta) + \cdots
$$
Substituting the expansion to the above we get
$$
\begin{aligned}
1 &\sim u_0(1, \theta) + \\
& +\varepsilon\left(u_1(1, \theta) + P_2(\cos(\theta))\frac{\partial u_0}{\partial r}(1, \theta)\right) + \\ 
&+\varepsilon^2\left(u_2(1, \theta) + P_2(\cos(\theta)) \frac{\partial u_1}{\partial r}(1, \theta) + \frac{1}{2}P_2(\cos(\theta))^2\frac{\partial^2 u_0}{\partial r^2}(1, \theta)\right).
\end{aligned}
$$
Then we get
$$
\begin{aligned}
\Delta u_0 = 0,& \quad r > S(\theta, 0), \\
u_0 = 1,& \quad r = 1, \\
\lim\limits_{r \rightarrow \infty} u_0 = 0,& \\
&\\
\Delta u_1 = 0,& \quad r > S(\theta, 0), \\
u_1 = -P_2(\cos(\theta))\frac{\partial u_0}{\partial r}(1, \theta),& \quad r = 1, \\
\lim\limits_{r \rightarrow \infty} u_1 = 0,& \\
&\\
\Delta u_2 = 0,& \quad r > S(\theta, 0), \\
u_2 = -P_2(\cos(\theta))\frac{\partial u_1}{\partial r}(1, \theta) - \frac{1}{2}P_2(\cos(\theta))^2\frac{\partial^2 u_0}{\partial r^2}(1, \theta),& \quad r = 1, \\
\lim\limits_{r \rightarrow \infty} u_2 = 0.
\end{aligned}
$$
To solve the Laplace equation $\Delta u = 0$ in spherical coordinates we apply the method of separation of variables. Assume that
$$
u(r, \theta) = R(r)\Theta(\theta),
$$
and use the assumption by substituting into the equation. We have
$$
\frac{\partial u}{\partial r} = R'(r)\Theta(\theta),
$$
and
$$
\frac{\partial u}{\partial \theta} = R(r)\Theta(\theta),
$$
so
$$
\Delta u = \frac{\Theta(\theta)}{r^2}(r^2R'(r))' + \frac{R(r)}{r^2\sin(\theta)}(\sin(\theta)\Theta'(\theta))' = 0.
$$
We multiply the equation by $\frac{r^2}{R\Theta}$ to get
$$
\frac{1}{R}(r^2R')' = -\frac{1}{\Theta\sin(\theta)}(\sin(\theta)\Theta')' = C,
$$
where $C$ is a chosen constant. We get two equations then:
$$
\frac{1}{R}(r^2R')' = C,
$$
$$
\frac{1}{\Theta\sin(\theta)}(\sin(\theta)\Theta')' = -C.
$$
The general solution of the first equation is
$$
R(r) = Ar^l + Br^{-(l+1)}.
$$
The general solution to the second equation is
$$
\Theta(\theta) = P_l(\cos(\theta)),
$$
where $P_l$ is the Legendre polynomial of degree $l$

Then the general solution to the Laplace equation is
$$
u(r, \theta) = \sum_{l=0}^\infty \left(Ar^l + Br^{-(l+1)}\right)P_l(\cos(\theta)).
$$
For our perturbed problem we get:
$$
u_0(r, \theta) = \frac{1}{r},
$$
$$
u_1(r, \theta) = \frac{1}{r^3}P_2(\cos(\theta)),
$$
# Multiple scales

Consider the Duffing equation:
$$
u'' + u = \varepsilon u^3, \quad u(0)=1, \quad u'(0)=0.
$$
Application of the Lindstedt method leads to the approximation
$$
u(t) \approx \cos\left(t - \frac{3}{8}\varepsilon t\right) = \cos(t)\cos\left(\frac{3}{8}\varepsilon t\right) + \sin(t)\sin\left(\frac{3}{8}\varepsilon t\right).
$$
We observe that the solution of the Duffing equation loves on two different time scales. This observation suggests that the solution of the Duffing equation should be written (formally) as $u(t_1, t_2)$ where $t_1=t$, and $t_2=\varepsilon t$. Then we seek a multiple scales expansion
$$
u(t_1, t_2) \sim u_0(t_1, t_2) + \varepsilon u_1(t_1, t_2).
$$
We have
$$
\frac{d}{dt} = \frac{\partial}{\partial t_1} + \varepsilon \frac{\partial}{\partial t_2},
$$
and
$$
\frac{d^2}{dt^2} = \frac{\partial^2}{\partial t_1^2} + 2\varepsilon\frac{\partial^2}{\partial t_1 \partial t_2} + \varepsilon^2\frac{\partial^2}{\partial t_2^2}.
$$
Plugging that into the Duffing equation, hell nah, I'm not writing all that. Then collecting the terms:
$$
\frac{\partial^2}{\partial t_1}u_0 + u_0 = 0 \quad \implies \quad u_0(t_1, t_2) = A_0(t_2)\cos(t_1) + B_0(t_2)\sin(t_1).
$$
From the initial condition we get
$$
f(0) = 1, \quad g(0) + \varepsilon f'(0) = 0.
$$
Using some trigonometry black magic we get
$$
\begin{aligned}
g' &= \frac{3}{8}f(f^2 + g^2), \\
f' &= -\frac{3}{8}g(f^2 + g^2), \\
\frac{\partial^2 u_1}{\partial t_1^2} + u_1 &= \frac{f}{4}(f^2-3g^2)\cos(3t_1) + \frac{g}{4}(3f^2-g^2)\sin(3t_1).
\end{aligned}
$$
We note that the first two equations have to hold for all $t_2$, so
$$
0 = g'g + f'f = \frac{1}{2}(f^2+g^2)',
$$
hence $f^2 + g^2 = 1$, by the initial condition. Then we get simplified equations
$$
\begin{aligned}
g' &= \frac{3}{8}f, \\
f' &= -\frac{3}{8}g,
\end{aligned}
$$
with the solutions (initial conditions applied)
$$
\begin{aligned}
g(t) &= \sin\left(\frac{3}{8}t\right), \\
f(t) &= \cos\left(\frac{3}{8}t\right).
\end{aligned}
$$
Finally we get
$$
u_0(t_1, t_2) = \cos\left(\frac{3}{8}t_2\right)\cos(t_1) + \sin\left(\frac{3}{8}t_2\right)\sin(t_1).
$$
Then
$$
u(t) \sim \cos\left(\frac{3}{8}\varepsilon t\right)\cos(t) + \sin\left(\frac{3}{8}\varepsilon t\right)\sin(t).
$$

Multiple temporal (or spacial) scales to not only appear in periodic systems. Such problems we may also find in problems that are modelled by
- $u''+\varepsilon u' + u = 0$ - weakly damped oscillator
- $u'' + k(\varepsilon t) u = 0$ - slowly varying coefficients
- $\nabla\left(k\left(\frac{x}{\varepsilon}\right)\nabla u\right) = f$ - diffusion in complex media

### Example (weakly dampened oscillator)
Consider the following problem
$$
u'' + \varepsilon u' + u = 0, \quad u(0)=0, \quad u'(0)=1.
$$
By the application of the regular perturbation method we get
$$
u(t) \sim \sin(t) - \frac{1}{2}\varepsilon t\sin(t),
$$
which doesn't make sense physically due to the secular term.

On the other side, from the application of the Lindstedt method we get
$$
u(t) \sim \left(1 - \varepsilon t + \frac{\varepsilon^3}{8}\right)\sin\left(t - \frac{\varepsilon^2}{8}t\right).
$$
We can see the same issue with the solution blowing up.

Then we try to apply the multiple scale approach.
We assume te existence of two time scales $t_1=t$, and $t_2=\varepsilon^\alpha t$.
$$
u(t) \sim u_0(t_1, t_2) + \varepsilon^\alpha u_1(t_1, t_2) + \cdots
$$
Comparing the terms with the same power of $\varepsilon$ yields
$$
\frac{\partial^2 u_0}{\partial t_1^2} + u_0 = 0
$$
The solution to the above is
$$
u_0(t_1, t_2) = a(t_2)\sin(t_1) + b(t_2)\cos(t_1),
$$
with $b(0)=0$, and $a(0)=1$. I don't want to write notes anymore.

# Slowly varying coefficients

Let $k: \mathbb{R} \rightarrow [a, b]$ be smooth and $a > 0$. Then we consider two problems:
$$
u'' + k^2(\varepsilon t)u = 0,
$$
and
$$
u'' + k^2\left(\frac{t}{\varepsilon}\right)u = 0.
$$
The first equation is well defined for $\varepsilon \rightarrow 0$ since $k(0) = k_0$, and we expect $u(t, \varepsilon) \rightarrow \alpha\cos(k_0t) + \beta\sin(k_0t)$.

The situation is not so clear with the second problem:
- what happens with $k\left(\frac{t}{\varepsilon}\right)$ as $\varepsilon \rightarrow 0$?
- does the solution $u(t, \varepsilon)$ converge to $u_0(t)$ in some sense?
- which equation does $u_0$ satisfy?

For now let's consider the first problem.
$$
u'' + k^2(\varepsilon t)u = 0, \quad u(0)=1, \quad u'(0)=0.
$$

We seek a two-scales solution with $t_1 = f(t, \varepsilon)$, and $t_2=\varepsilon t$.
For the solution we seek an expansion of the form $u(t, \varepsilon) \sim u_0(t_1, t_2)$.
The function $f$ should satisfy the following assumptions:
- $f$ should be smooth,
- $f$ should be increasing w.r.t $t$,
- $f(0)=0$,
- $f >> \varepsilon t$ to separate it from the slow scale $t_2=\varepsilon t$,
- $f$ should simplify the problem.

We get the following equation
$$
f''{u_0}_{t_1} + (f')^2{u_0}_{t_1t_1} + k^2(t_2)u_0 = 0.
$$
We note that the unperturbed problem oscillates and is damped, therefore second and third term should be of the same order and dominate.

$$
(f')^2{u_0}_{t_1t_1} + k^2(t_2)u_0 = 0.
$$
We solve it with some initial conditions and get
$$
u_0(t_1, t_2) = a(t_2)\cos(t_1) + b(t_2)\cos(t_1).
$$
To determine $a$ and $b$, we have to consider the next order term:
$$
TODO: equation here
$$
To avoid secular terma ins the solution we set
$$
\begin{aligned}
2ka' + ak' &= 0, \quad a(0)=1 \\
2kb' + bk' &= 0, \quad b(0)=0.
\end{aligned}
$$
The solutions are:
$$
\begin{aligned}
a(t_2) &= \sqrt{\frac{k(0)}{k(t_2)}}, \\
b(t_2) &= 0.
\end{aligned}
$$

Finally we get
$$
u(t_1, t_2) = a(t_2)\cos(t_1) = \sqrt{\frac{k(0)}{k(t_2)}}\cos\left(\int_0^tk(\varepsilon s)ds\right).
$$

