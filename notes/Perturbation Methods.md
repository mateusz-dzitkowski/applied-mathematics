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
