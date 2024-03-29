# 1. Metric spaces and Banach's FPT (Fixed Point Theorem)

### Def 1.1 (Metric and Metric Space)
Let $X$ be a nonempty set, and $d: X^2 \rightarrow \mathbb{R}$ be a function satisfying:
- $d(x, y) = 0$ iff $x=y$
- $d(x, y) = d(y, x)$
- $d(x, y) \le d(x, z) + d(z, y)$
Then the function $d$ is called the metric, the pair $(X, d)$ is called the metric space, and the number $d(x, y)$ is called the distance between $x$ and $y$ in $X$.
#### Examples
- $(\mathbb R^n, d)$, with $d(x, y) = \left(\sum_{i=1}^n(x_i-y_i)^2\right)^{\frac{1}{2}}$
- $(\mathbb R^n, d)$, with $d(x, y) = \max\limits_{i\le n}|x_i-y_i|$
- $(C[a,b], d)$, with $d(f, g) = \left(\int_a^b|f(x)-g(x)|^2dx\right)^{\frac{1}{2}}$
- $(C[a,b], d)$, with $d(f, g) = \sup\limits_{a\le x \le b}|f(x) - g(x)|$
- $(L^p[a, b], d)$, with $d(f, g) = \left(\int_a^b|f(x) - g(x)|^pdx\right)^\frac{1}{p}$
### Def 1.2 (Fixed Point)
A fixed point of the mapping $T:X \rightarrow X$ is the point $x^*\in X$ such that $T(x^*) = x^*$.
### Def 1.3 (Contraction)
Let $(X, d)$ be a [[#Def 1.1 (Metric and Metric Space)|metric space]]. A mapping $T: X\rightarrow X$ is called a contraction on $X$ of there exists a constant $0\lt k\lt1$ such that $$d(T(x), T(y)) \le kd(x, y)$$ for all $x, y \in X$.
### Theorem 1.1 (Banach's FPT)
Let $(X, d)$  be a complete [[#Def 1.1 (Metric and Metric Space)|metric space]] and let $T:X\rightarrow X$ be a [[#Def 1.3 (Contraction)|contraction]] on $X$. Then $T$ has a unique [[#Def 1.2 (Fixed Point)|fixed point]] $x^*\in X$.
#### Corollary 1.1 (Banach's FPT)
The iterative sequence $x_{n+1} = T(x_n)$ for $n=1, 2, ...$ with arbitrary starting point $x_0 \in X$ converges, under assumptions of [[#Theorem 1.1 (Banach's FPT)|Banach's FPT]], to the unique [[#Def 1.2 (Fixed Point)|fixed point]] of $T$. Moreover, the following estimates hold: 
- $d(x_m,x^*) \le \frac{k^m}{1-k}d(x_1, x_0)$ - the prior estimate,
- $d(x_m, x^*) \le \frac{k}{1-k}d(x_{m-1}, x_m)$ - the posterior estimate.
# 2. Applications of [[#Theorem 1.1 (Banach's FPT)|Banach's FPT]]
## 2.1 Applications to real-valued functions
Let $g \in C^1[a, b]$, and suppose we want to find the solution to the equation $g(x)=0$ on $[a, b]$. We note that we can always rewrite this equation as $x = g(x) + x$, and then out problem is equivalent with finding a fixed point of the function $f(x) = x + g(x)$.
### Theorem 2.1 (Differentiable Contraction)
Let $(\mathbb R,d)$  be a metric space of real numbers with the [[#Def 1.1 (Metric and Metric Space)|metric]] $d(x, y) = |x - y|$ and let $[a, b]$ be a closed interval in $\mathbb R$. Moreover, let $f: [a, b] \rightarrow [a, b]$ be a continuous and differentiable function such that $\sup\limits_{x\in[a,b]}|f'(x)| \le k \lt 1$. Then there exists a unique [[#Def 1.2 (Fixed Point)|fixed point]] $x^*\in[a,b]$ of $f$.
#### Example 2.1
We want to find the solution to the equation $cos(x) - 2x = 0$ on $[0, \pi]$. Then we can write this equation as $x=\frac{1}{2}cos(x)$, and try to find the fixed point of the function $f(x)=\frac{1}{2}cos(x)$ on $[0,\pi]$. We have to show that $f$ is a [[#Def 1.3 (Contraction)|contraction]] on $[0, \pi]$. To do so, we apply the [[#Theorem differentiable contraction|theorem 2.1]]. We have 
$$
\sup\limits_{x\in[0,\pi]}|f'(x)| = \sup\limits_{x\in[0,\pi]}\left|-\frac{1}{2}sin(x)\right|=\frac{1}{2}\lt1.
$$
We have shown that $f$ is a [[#Def 1.3 (Contraction)|contraction]] and, by the [[#Theorem 1.1 (Banach's FPT)|Banach's FPT]], it has a [[#Def 1.2 (Fixed Point)|fixed point]] $x^*$ that is the limit of the sequence $\{x_n\}$ generated by the scheme $x_{n+1} = f(x_n)$ with any starting point $x_0\in[0,\pi]$.
Note that to show that $f$ is a contraction we could also directly apply the definition: 
$$
\begin{aligned}
|f(x)-f(y)|&=\left|\frac{1}{2}cos(x) - \frac{1}{2}sin(x)\right| =\left|sin\left(\frac{x+y}{2}\right)sin\left(\frac{x-y}{2}\right)\right|\\
&\leq\sup\limits_{x,y\in[0,\pi]}\left|sin\left(\frac{x+y}{2}\right)\frac{1}{2}|x-y|\right|=\frac{1}{2}|x-y|\le|x-y|.
\end{aligned}
$$
## 2.2 Applications to integral equations
We consider integral equations in the following form
$$
f(x) = g(x) + \mu\int_a^bk(x,y)f(y)dy,
$$
where $f:[a,b]\rightarrow\mathbb R$ is an unknown function, $g: [a,b] \rightarrow \mathbb R$, and $k:[a,b]^2\rightarrow\mathbb R$ are given functions, and $\mu$ is a parameter.
The above integral equation can be considered in various function spaces. Here we consider this equation only in $(C[a, b], d)$ with $d(f, g) = \sup\limits_{x\in[a,b]}|f(x)-g(x)|$. 
We assume that $g\in C[a,b]$, and that the kernel $k$ is continuous on the square $[a,b]^2$, which implies that $k$ is bounded on $[a,b]^2$, meaning that there exists a constant $c$, such that $|k(x, y)| \le c$ for all $(x, y)\in[a,b]^2$.
### Theorem 2.2
The metric space $(C[a, b], d)$ is complete

Note that our integral equation can be rewritten as $T(f) = f$, where 
$$
T(f)(x) = g(x)+\mu\int_a^bk(x,y)f(y)dy.
$$
First we have to show that the mapping $T:C[a,b]\rightarrow C[a,b]$ is well-defined, but this is obvious, as $g$ and $k$ are both continuous on their domains. Let us now determine for which values of $\mu$ the map $T$ is a [[#Def 1.3 (Contraction)|contraction]]. We have
$$
\begin{aligned}
d(T(f_1), T(f_2)) &= \sup\limits_{x\in[a,b]}\left|T(f_1)(x)-T(f_2)(x)\right| = \sup\limits_{x\in[a,b]}|\mu|\left|\int_a^bk(x,y)(f_1(y)-f_2(y))dy\right| \le \\
&\le |\mu|\sup\limits_{x\in[a,b]}\int_a^b|k(x,y)||f_1(y)-f_2(y)|dy \le c|\mu|\sup\limits_{x\in[a,b]}|f_1(x)-f_2(x)|\int_a^bdy = \\
&=c|\mu|(b-a)d(f_1,f_2).
\end{aligned}
$$
It is now required that $c|\mu|(b-a)\lt1$, or $|\mu|\lt\frac{1}{c(b-a)}$, for $T$ to be a contraction. Applying the [[#Theorem 1.1 (Banach's FPT)|Banach's FPT]], we see that the map $T$ has a unique [[#Def 1.2 (Fixed Point)|fixed point]] $f^*\in C[a,b]$.
### Theorem 2.3 (Integral equation)
Consider the integral equation
$$
f(x) = g(x) + \mu \int_a^bk(x,y)f(y)dy.
$$
Suppose that $k$ and $g$ are continuous on $[a,b]^2$ and $[a,b]$ respectively, and assume that the parameter $\mu$ satisfies $|\mu| \lt \frac{1}{c(b-a)}$ with the constant $c$ such that $|k(x,y)| \lt c$ for all $(x,y) \in [a,b]^2$. Then the integral equation has a unique solution $f \in C[a, b]$. Moreover, this solution is a limit of the sequence $\{f_n\}$ where $f_0$ is a continuous function on $[a,b]$, and
$$
f_{n+1} = g(x) + \mu\int_a^bk(x,y)f_n(y)dy.
$$
## 2.3 Applications to differential equations
Let's consider the initial value problem
$$
\begin{aligned}
x'(t) &= f(t, x(t)) \\
x(t_0) &= x_0
\end{aligned}
$$
where $f:A \subset \mathbb{R}^2 \rightarrow \mathbb{R}$ is a given function and $x(t)$ is an unknown function that we want to find.
### Theorem 2.4 (Picard-Lindelöf)
Let $f$ be continuous on the rectangle 
$$
R = \left\{(t,x) \in \mathbb{R}_+ \times \mathbb{R}: |t-t_0| \le a, |x - x_0| \le b\right\}
$$
and thus bounded on $R$, say $|f(t, x)| \le c$ for all $(t, x) \in R$. Suppose that $f$ satisfies the Lipschitz condition on $R$ with respect to the second argument, i.e., there exists a constant $k$ such that
$$
|f(t,x) - f(t,y)| \le k|x-y|
$$
for all $(t,x), (t,y) \in R$.
Then the initial value problem has a unique solution, which exists on the interval $[t_0-\beta, t_0+\beta]$, where
$$
\beta = \min\left\{a, \frac{b}{c}, \frac{1}{k}\right\}.
$$
### Corollary 2.1 (Picard-Lindelöf)
Under the assumptions of [[#Theorem 2.4 (Picard-Lindelöf)|Picard-Lindelöf theorem]], the sequence given by
$$
\begin{aligned}
x_0(t) &= x_0\\ 
x_{n+1}(t) &= T(x_n)(t) = x_0 + \int_{t_0}^tf(s, x_n(s))ds
\end{aligned}
$$
converges uniformly to the unique solution $x(t)$ on $J=[t_0-\beta,t_0+\beta]$.
#### Example 2.2
Consider the differential equation
$$
x'(t) = \sqrt{x(t)} + x^3(t), \quad x(1) = 2.
$$
We have 
$$
\begin{aligned}
x_1(t) &= 2 + \int_1^t\left(\sqrt{2}+2^2\right)ds = 2 + \left(\sqrt{2} + 8\right)(t-1) \\
x_2(t) &= 2 + \int_1^t\left(\sqrt{x_1(s)} + x_1(s)^3\right)ds = *\textrm{hot mess}*
\end{aligned}
$$
## 2.4 Applications to matrix equations
Suppose we want to find a solution of the matrix equation
$$
Ax = B
$$
where $A \in \mathbb{R}^{n \times m}, b \in \mathbb{R}^n$.
We note that this equation can be rewritten as 
$$
x = (I-A)x + b
$$
where $I$ is the identity matrix.
Let's define the map $T: \mathbb{R}^n \rightarrow \mathbb{R}^n$ by
$$
Tx = (I-A)x + b.
$$
Then the problem of solving the matrix equation $Ax=b$ is equivalent with finding a [[#Def 1.2 (Fixed Point)|fixed point]] of $T$. 
Let's define $\alpha_{ij} = \delta_{ij} - a_{ij}$ where $a_{ij}$ are elements of the matrix $A$, and $\delta_{ij}$ is the Kronecker delta. Using this notation we have 
$$
(Tx)_i = \sum_{j=1}^n\alpha_{ij}x_j + b_i
$$
We will show that $Ax=b$ has a unique solution if
$$
\sum_{j=1}^n|\alpha_{ij}| \le \alpha \lt 1.
$$
for all $i=1,2,\dots,n$. Consider the matrix space $(\mathbb{R}^n, d)$, with $d(x, y) = \max\limits_{1 \le i \le n}|x_i-y_i|$ for $x,y \in \mathbb{R}^n$. We have
$$
\begin{aligned}
d(Tx, Ty) &= \max\limits_i \left|(Tx)_i - (Ty)_i\right| = \\ 
&= \max\limits_i \left|\sum_{j=1}^n\alpha_{ij}(x_j-y_j)\right| \le \\
&\le \max\limits_i \sum_{j=1}^n|\alpha_{ij}||x_j-y_j| \le \\
&\le \max\limits_i \sum_{j=1}^n|\alpha_{ij}| \cdot \max\limits_j|x_j-y_j| = \\
&= \max\limits_i \sum_{j=1}^n|\alpha_{ij}| \cdot d(x, y).
\end{aligned}
$$
We notice that if $\sum_{j=1}^n|\alpha_{ij}| \lt 1$, for all $i=1,2,\dots,n$, then $\max\limits_i\sum_{j=1}^n|\alpha_{ij}|\lt1$. We have
$$
\sum_{j=1}^n|\alpha_{ij}| = |a_{i1}| + |a_{i2}| + \dots + |1-a_{ii}| + \dots + |a_{in}| \lt 1,
$$
so
$$
\sum_{j=1, j \ne i}^n|a_{ij}| \lt 1 - |1-a_{ii}| \lt |a_{ii}|.
$$
We get the condition for the matrix $A$ for which $T$ is a [[#Def 1.3 (Contraction)|contraction]]]. This condition is given by
$$
|a_{ii}| \gt \sum_{j=1, j \ne i}^n|a_{ij}|,
$$
or, in other words, matrix $A$ should be strictly diagonally dominant.
### Theorem 2.5 (Matrix equation)
The matrix equation $Ax=b$ with $A \in \mathbb{R}^{n \times n}$ an $b \in \mathbb{R}^n$ has a unique solution $x \in \mathbb{R}^n$ if $A$ is strictly diagonally dominant. The iteration method is as follows
$$
x_{n+1} = (I - A)x_n + b, \quad x_0 \in \mathbb{R}^n.
$$
In general, we can rewrite the equation $Ax=b$ as $Qx = (Q-A)x + b$, where $Q \in \mathbb{R}^{n \times n}$. We then have the following iterative scheme
$$
Qx_{n+1} = (Q-A)x_n + b.
$$
Examples:
- $Q = I$ - Richardson method,
- $Q$ diagonal, with $q_{ii} = a_{ii}$ - Jacobi method,
- $Q = D - L$ with $D$ diagonal, and $L$ lower triangular - Gauss-Seidel method.
# 3. Normed spaces
### Def 3.1 (Norm and normed space)
A norm on a vector space $X$ is a real-valued function denoted by $||\cdot||$ which satisfies the following conditions:
- $||x|| \ge 0$ for all $x$. $||x|| = 0$ iff $x=0$,
- $||\alpha x|| = |\alpha|||x||$ for any $\alpha$, and $x \in X$,
- $||x + y|| \le ||x|| + ||y||$ for all $x, y \in X$.
A normed space is a vector space equipped with a norm, depicted by $(X, ||\cdot||)$, or with a shorthand $X$.
#### Remark 3.1.1
A [[#Def 3.1 (Norm and normed space)|norm]] on $X$ defines the [[#Def 1.1 (Metric and Metric Space)|metric]] $d(\cdot, \cdot)$ on $X \times X$, which is defined by $d(x, y) = ||x - y||$, and is called the metric induced by the norm $||\cdot||$.
#### Remark 3.1.2
Every [[#Def 3.1 (Norm and normed space)|normed space]] $X$ is a [[#Def 1.1 (Metric and Metric Space)|metric space]], converse might not be true.
For example, a [[#Def 1.1 (Metric and Metric Space)|metric]] defined by 
$$
d(x, y) = 
	\begin{cases} 
	1,& \quad x=y, \\
	0,& \quad x \ne y,
	\end{cases}
$$
then $||\alpha(x-y)|| = d(\alpha x, \alpha y) \ne |\alpha|d(x,y) = |\alpha|||x-y||$.
### Lemma 3.1 (Norm continuity)
The [[#Def 3.1 (Norm and normed space)|norm]] $|| \cdot ||$ defined on $X$ is a continuous mapping of $X$ into $\mathbb{R}$.
#### Examples of normed spaces
- $(\mathbb{R}^n, ||\cdot||_2)$, with $||x||_2 = \left(\sum_{m=1}^nx_i^2\right)^\frac{1}{2}$,
- $(C[a,b], ||\cdot||)$, with $||f|| = \max\limits_{x \in [a,b]}|f(x)|$,
- $(L^p(\Omega), ||\cdot||_{L^p(\Omega)})$, with $\Omega \subset \mathbb{R}$, $p \ge 1$ and 
	$$
	||f||_{L^p(\Omega)} = 
		\begin{cases}
		\left(\int_\Omega f(x)^pdx \right)^\frac{1}{p},& \quad 1 \le p \lt \infty, \\
		ess\sup\limits_{x \in \Omega}|f(x)|,& \quad p = \infty.
		\end{cases}
	$$
### Def 3.2 (Norm equivalence)
Two [[#Def 3.1 (Norm and normed space)|normed spaces]] $(X, ||\cdot||_1)$, $(X, ||\cdot||_2)$ are called topologically equivalent, or two [[#Def 3.1 (Norm and normed space)|norms]] $||\cdot||_1$, and  $||\cdot||_2$ are called equivalent if there exist positive constants $C_1$, and $C_2$, such that 
$$
C_1||x||_2 \le ||x||_1 \le C_2||x||_2
$$
for all $x \in X$.
### Theorem 3.1 (Equivalence of norms in finite dimensional spaces)
All [[#Def 3.1 (Norm and normed space)|norms]] of finite dimensional space $X$ are equivalent.
### Def 3.3 (Convergence in normal spaces)
A sequence $\{x_n\}$ in a [[#Def 3.1 (Norm and normed space)|normed space]] $(X, ||\cdot||)$ is convergent if there exists $x \in X$ such that $\lim\limits_{n \rightarrow \infty}||x_n - x|| = 0$.
### Def 3.4 (Cauchy sequence)
A sequence $\{x_n\}$ in a [[#Def 3.1 (Norm and normed space)|normed space]] $(X, ||\cdot||)$ is a Cauchy sequence if
$$
\lim\limits_{m,n \rightarrow \infty}||x_n - x_m|| = 0.
$$
### Def 3.5 (Complete space)
We say that a [[#Def 3.3 (Convergence in normal spaces)|normal space]] $(X, ||\cdot||)$ is complete if every [[#Def 3.4 (Cauchy sequence)|Cauchy sequence]] $\{x_n\}$ in $X$ is convergent to some $x \in X$.
### Def 3.6 (Banach space)
A [[#Def 3.5 (Complete space)|complete]] [[#Def 3.1 (Norm and normed space)|normed]] space is called a Banach space.
### Theorem 3.2 (Euclidean space is complete)
The space $(\mathbb{R}^N, ||\cdot||_2)$ with the standard Euclidean norm is [[#Def 3.5 (Complete space)|complete]].
### Theorem 3.3 ()
Let $\Omega$ be a compact subset of $\mathbb{R}^n$. Then the set $C(\Omega)$ of all continuous functions on $\Omega$ equipped with the norm $||f|| = \max\limits_{x \in \Omega}|f(x)|$ is a [[#Def 3.6 (Banach space)|Banach space]].
# 4. Hilbert spaces
### Def 4.1 (Inner product and inner product space)
Let $X$ be a vector space over the field $\mathbb{F}$ over the real or complex numbers. A mapping $\langle\cdot, \cdot\rangle:X^2 \rightarrow \mathbb{F}$ is called an inner product if for all $x,y \in X$ the following conditions are satisfied
1. $\langle x, x\rangle \ge 0$, and $\langle x, x\rangle=0 \iff x=0$,
2. $\langle x,y \rangle = \overline{\langle y,x \rangle}$,
3. $\langle \alpha x,y \rangle = \alpha\langle x,y \rangle$ for $\alpha \in \mathbb{F}$,
4. $\langle x+x',y\rangle = \langle x,y \rangle + \langle x',y\rangle$.
The vector space $X$ together with an inner product $\langle\cdot,\cdot\rangle$ is called an inner product space or pre-Hilbert space and is denoted $(X, \langle\cdot,\cdot\rangle)$.
#### Remark 4.1
- $\overline{\langle x,y \rangle}$ denoted the complex conjugate of $\langle x,y \rangle$,
- The condition $2$ implies that $\langle x,x \rangle$ must be a real number,
- If $\mathbb{F} = \mathbb{R}$ then $\langle x,y \rangle = \langle y,x \rangle$,
- Conditions $3$ and $4$ imply that the function $\langle \cdot,\cdot \rangle$ is linear in the first variable. It is easy to see that $\langle \cdot,\cdot \rangle$ is also linear in the second variable if $\mathbb{F}=\mathbb{R}$,
#### Examples
- $\mathbb{R}^N$, with $\langle x,y \rangle = \sum_{i=1}^Nx_iy_i$,
- $C(\Omega)$, with $\langle f,g \rangle = \int_\Omega f(x)\overline{g(x)}dx$,
- $L_2(\Omega)$, with $\langle f,g \rangle = \int_\Omega f(x)g(x)dx$.
### Theorem 4.1 (Cauchy-Schwarz-Bunyakowski inequality)
For all $x, y \in (X, \langle \cdot,\cdot \rangle)$ we have
$$
|\langle x,y \rangle|^2 \le \langle x,x \rangle\langle y,y \rangle.
$$
### Theorem 4.2 (Inner product space is normed)
Every [[#Def 4.1 (Inner product and inner product space)|inner product space]] $(X, \langle \cdot,\cdot \rangle)$ is a [[#Def 3.1 (Norm and normed space)|normed space]] with respect to the norm $||x|| = \sqrt{|\langle x,x \rangle|}$.
### Def 4.2 (Hilbert space)
An [[#Def 4.1 (Inner product and inner product space)|inner product space]] $(X, \langle \cdot,\cdot \rangle)$ is called a Hilbert space if the normed space $(X, ||\cdot||)$ with the [[#Def 3.1 (Norm and normed space)|norm]] induced by the inner product is a [[#Def 3.6 (Banach space)|Banach space]].
