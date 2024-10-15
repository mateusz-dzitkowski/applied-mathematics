# 1. Necessary and sufficient optimality conditions

### Theorem 1.1 (Necessary optimality condition)
Let $x^* \in \mathbb{R}^n$ be  an unconstrained local minimum (maximum) of $f: X \rightarrow \mathbb{R}$, where $X \subset \mathbb{R}^n$. If $f$ is continuously differentiable on an open set $S$ containing $x^*$, then
$$
\nabla f(x^*) = 0.
$$
If, in addition, $f$ is twice continuously differentiable on $S$, then $\nabla^2f(x^*)$ is positive semidefinite (negative semidefinite).

### Theorem 1.2 (Sufficient optimality condition)
Let the function $f: X \rightarrow \mathbb{R}$, where $X \subset \mathbb{R}^n$, be twice continuously differentiable on an open set $S$. Suppose that $x^* \in S$ satisfies
$$ 
\nabla f(x^*) = 0, \quad \nabla^2f(x^*) \text{ is positive (negative) definite}.
$$
Then $x^*$ is a strict unconstrained local minimum (maximum) of $f$.

### Def 1.1 Definite matrices
An $n \times n$ symmetric real matrix $A$ is called:
- Positive definite iff $x^TAx > 0$ for any $x \ne 0$.
- Positive semidefinite iff $x^TAx \ge 0$ for any $x$.
- Negative definite iff $x^TAx < 0$ for any $x \ne 0$.
- Negative semidefinite iff $x^TAx \le 0$ for any $x$.

#### Remark
In practice we check the above characteristics via:
- Sylvester's criterion:
	- $A$ positive definite iffall its leading principal minors are positive.
	- $A$ negative definite iffall its leading principal minors of odd size are negative and all of even size are positive.
	- $A$ positive semidefinite iff all its principal minors are nonnegative.
	- $A$ negative semidefinite iffall its principal minors of odd size are nonpositive and all of even size are nonnegative.
- Eigenvalue criterion:
	- $A$ positive (semi)definite iff all its eigenvalues are positive (nonnegative).
	- $A$ negative (semi)definite iff all its eigenvalues are negative (nonpositive).

### Def 1.2 Convexity and concavity
We say that a function $f: \mathbb{R}^n \rightarrow \mathbb{R}$ is convex, if for any $x, y \in \mathbb{R}^n$ and $\lambda \in (0, 1)$ we have
$$
f(\lambda x + (1 - \lambda)y) \le \lambda f(x) + (1-\lambda)f(y). 
$$
If for any $x, y \in \mathbb{R}^n$ the inequality above is strict, we say that $f$ is strictly convex.

Flip the inequality sign, and you get the definition of concave and strictly concave.

### Theorem 1.3
Suppose that $f: \mathbb{R}^n \rightarrow \mathbb{R}$ is twice continuously differentiable. Then:
- $f$ is convex iff for any $x \in \mathbb{R}^n$ $\nabla^2 f(x)$ is positive semidefinite
- $f$ is strictly convex iff for any $x \in \mathbb{R}^n$ $\nabla^2 f(x)$ is positive definite
- $f$ is concave iff for any $x \in \mathbb{R}^n$ $\nabla^2 f(x)$ is negative semidefinite
- $f$ is strictly concave iff for any $x \in \mathbb{R}^n$ $\nabla^2 f(x)$ is negative definite

### Theorem 1.4
Suppose $f: C \rightarrow \mathbb{R}$, where $C \subset \mathbb{R}^n$ is convex, is a convex function. Then the following statements are true:
- Any local minimum of $f$ is its global minimum.
- If $f$ has continuous first-order derivatives on $C$, each stationary point of $f$ is a global minimum.
- If, in addition, $f$ is strictly convex, there exists at most one global minimum of $f$.

#### Remark
Similar theorem goes for concave functions and maxima.

#### Remark
Because of these properties problems of minimisation of convex functions over convex sets (convex problems) are of special interest to optimisation theory.

### Def 1.3 Coercive function
We say that a function $f: \mathbb{R}^n \rightarrow \mathbb{R}$ is coercive if
$$
\lim\limits_{||x|| \rightarrow \infty}f(x) = \infty.
$$

### Theorem 1.5
Suppose $f: \mathbb{R}^n -\mathbb{R}$ is coercive. Then it has a global minimum.

#### Remark
In practice, this means that for a coercive function one of the local minimisers is a global minimiser, so we only need to search through them and compare their values.

# 2. Line Search Algorithms

### Theorem 2.1
Suppose the function $f: \mathbb{R} \rightarrow \mathbb{R}$ is unimodal on interval $[a, b]$. Then the sequences of both ends of the search interval $\{x_L^k\}$ and $\{x_U^k\}$ converge to the global minimiser of $f$ on $[a, b]$. Moreover, $x^*$ given by the golden section search method after $n$ iterations differs by at most $\frac{1}{2}K^n(b-a)$ from the real minimiser.

#### Remark
If the function has a finite number of local minima on $[a, b]$ (including possibly the points $a$ and $b$), the method will converge to one of these local minima.
Finding the global minimum will require partitioning of $[a, b]$ into subintervals where $f$ is unimodal.

### Theorem 2.2
Suppose that $f$ satisfies for some $a < b$ the condition that $f'(a) < 0$ and $f'(b) \ge 0$ or $f(b) \ge f(a)$, and that $f'$ is continuous on $[a, b]$. Then the sequence $x_k^*$  of approximations of line search based on cubic interpolation converges to some stationary point of $f$.

Bro no way I'm writing down the algorithms.

