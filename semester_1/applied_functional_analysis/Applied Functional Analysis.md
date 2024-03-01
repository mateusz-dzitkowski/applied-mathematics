# Metric spaces and Banach's FPT (Fixed Point Theorem)

## Def: metric and metric space
Let $X$ be a nonempty set, and $d: X^2 \rightarrow \mathbb{R}$ be a function satisfying:
- $(d(x, y) = 0$ iff $x=y$
- $d(x, y) = d(y, x)$
- $d(x, y) \le d(x, z) + d(z, y)$
Then the function $d$ is called the metric, the pair $(X, d)$ is called the metric space, and the number $d(x, y)$ is called the distance between $x$ and $y$ in $X$.
### Examples
- $(\mathbb R^n, d)$, with $d(x, y) = \left(\sum_{i=1}^n(x_i-y_i)^2\right)^{\frac{1}{2}}$
- $(\mathbb R^n, d)$, with $d(x, y) = \max\limits_{i\le n}|x_i-y_i|$
- $(C[a,b], d)$, with $d(f, g) = \left(\int_a^b|f(x)-g(x)|^2dx\right)^{\frac{1}{2}}$
- $(C[a,b], d)$, with $d(f, g) = \sup\limits_{a\le x \le b}|f(x) - g(x)|$
- $(L^p[a, b], d)$, with $d(f, g) = \left(\int_a^b|f(x) - g(x)|^pdx\right)^\frac{1}{p}$
## Def: fixed point
A fixed point of the mapping $T:X \rightarrow X$ is the point $x^*\in X$ such that $T(x^*) = x^*$.
## Def: contraction
Let $(X, d)$ be a [[Applied Functional Analysis#Def metric and metric space|metric space]]. A mapping $T: X\rightarrow X$ is called a contraction on $X$ of there exists a constant $0\lt k\lt1$ such that $$d(T(x), T(y)) \le kd(x, y)$$ for all $x, y \in X$.
## Theorem 1 (Banach's FPT)
Let $(X, d)$  be a complete [[Applied Functional Analysis#Def metric and metric space|metric space]] and let $T:X\rightarrow X$ be a [[Applied Functional Analysis#Def contraction|contraction]] on $X$. Then $T$ has a unique [[Applied Functional Analysis#Def fixed point|fixed point]] $x^*\in X$.

