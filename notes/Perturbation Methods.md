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
If $M(x) is a bounded function on $\mathbb{I}$, then we write $f(x; \varepsilon) = O(g(x; \varepsilon))$ as $\varepsilon\rightarrow\varepsilon_0$ **uniformly** on $\mathbb{I}$.

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