# Applied Functional Analysis - Exercise sheet 2
Mateusz Dzitkowski, 249777
## Exercise 1
We are presented with the following function
$$
u(x) = \int_0^1K(x, y)f(y)dy,
$$
for $x \in (0,1)$, and
$$
K(x, y) = \begin{cases}
\frac{1}{T}y(1-x), y \in [0, x], \\
\frac{1}{T}x(1-y), y \in [x, 1].
\end{cases}
$$
We have
$$
\begin{aligned}
u(x) &= \frac{1}{T}\left((1-x)\int_0^xyf(y)dy + x\int_x^1(1-y)f(y)dy\right), \\
u'(x) &= \frac{1}{T}\left(\int_0^1yf(y)dy + \int_x^1f(y)dy\right), \\
u''(x) &= -\frac{1}{T}f(x),
\end{aligned}
$$
rearranging, we get
$$
Tu''(x) + f(x) = 0,
$$
or
$$
f(x) = -Tu''(x).
$$
moreover, it is apparent from the definition of $u$, that $u(0) = u(1) = 0$.
Now let $u(x) = (x-1)\sin(x)$, and let a small perturbation be defined as $n_\delta(x) = \delta(x-1)\sin\left(\frac{x}{\delta}\right)$, and define $u_\delta(x) = u(x) + n_\delta(x)$. We have
$$
\begin{aligned}
||u - u_\delta|| &= ||n_\delta||, \\
||f - f_\delta|| &= T||n'_\delta||.
\end{aligned}
$$
Let's now compute the $L^2$ and $L^\infty$ norms of both of these:
$$
\begin{aligned}
||u - u_\delta||_2^2 &= \int_0^1\left|\delta\sin\left(\frac{x}{\delta}\right)\right|^2dx = \frac{\delta^2}{24}\left(3\delta^3\sin\left(\frac{2}{\delta}\right) - 6\delta^2 + 4\right), \\

||f - f_\delta||_2^2 &= \int_0^1\left|T\left(\frac{1}{\delta}(x-1)\sin\left(\frac{x}{\delta}\right) - \cos\left(\frac{x}{\delta}\right)\right)\right|^2dx = T^2\left(\frac{1}{6\delta^2} + \frac{1}{8}\sin\left(\frac{2}{\delta}\right) + \frac{3}{4}\right), \\

||u-u_\delta||_\infty &= \max\limits_{0 \le x \le 1}\left|\delta(x-1)\sin\left(\frac{x}{\delta}\right)\right| \le \delta, \\

||f - f_\delta||_\infty &= \max\limits_{0 \le x \le 1}\left|T\left(\frac{1}{\delta}(x-1)\sin\left(\frac{x}{\delta}\right) - \cos\left(\frac{x}{\delta}\right)\right)\right| \ge \\ &\ge \left|\max\limits_{0 \le x \le 1}\left(\frac{T}{\delta}(x-1)\sin\left(\frac{x}{\delta}\right)\right) - \max\limits_{0 \le x \le 1}\left(T\cos\left(\frac{x}{\delta}\right)\right)\right| \ge T\left|-\frac{1}{\delta} - 1\right| = \\
&= T\left(\frac{1}{\delta} + 1\right).
\end{aligned}
$$
As we can see, in both cases, $L^2$, and $L^\infty$, the norm of $u-u_\delta$ approaches zero when $\delta$ approaches zero, on the other hand the norm of $f - f_\delta$ gets arbitrarily large when $\delta$ approaches zero, this means that the problem of finding $f$ when we have perturbations in initial data $u$ is ill-posed.
## Exercise 2
We are presented with a problem of calculating the derivative of noisy data, that is
$$
f_\delta(x) = f(x) + n_\delta(x),
$$
for $x \in (0, 1)$, and $f_\delta(0) = f(0) = 0 = f_\delta(1) = f(1) = 0$, with
$$
n_\delta(x) = \sqrt{2}\delta\sin(2\pi kx)
$$
with a fixed, small $\delta$. Obviously we have
$$
\begin{aligned}
||f-f_\delta|| &= ||n_\delta||, \\
||f' - f'_\delta|| &= ||n'_\delta||,
\end{aligned}
$$
so, calculating the $L^2$ and $L^\infty$ norms we get (omitting the messy details this time)
$$
\begin{aligned}
||f - f_\delta||_2^2 &= ||n_\delta||_2^2 = \delta^2\left(1 - \frac{\sin(4\pi k)}{4\pi k}\right), \\

||f' - f'_\delta||_2^2 &= ||n'_\delta||_2^2 = \pi^2k^2\delta^2, \\

||f - f_\delta||_\infty &= ||n_\delta||_\infty = \sqrt{2}\delta, \\

||f' - f'_\delta||_\infty &= ||n'_\delta||_\infty = 2\sqrt{2}\pi k \delta.
\end{aligned}
$$
Again, we have the same situation as in the first exercise, where the norm of the difference $f-f_\delta$ stays small, due to $\delta$ being small, even when $k$ goes to infinity. On the other hand, the norm of the difference $f' - f'_\delta$ diverges to infinity when $k$ goes to infinity. This proves that the problem of differentiating noisy data is ill-posed.
## Exercise 3
We are presented with a Fredholm integral equation of the form
$$
u(x) = \int_0^1K(x, y)f(y)dy,
$$
for $x \in (0, 1)$.The function $f$ represents the true image, kernel $K$ characterises the blurring effect, and $u$ is the blurred image. We wish to recover $f$ from a previously blurred image $u$. Assume that the kernel $K$ is a gaussian kernel, that is
$$
K(x, y) = \frac{1}{\sigma\sqrt{2\pi}}\exp\left(-\frac{1}{2\sigma^2}(x-y)^2\right),
$$
where $\sigma > 0$ is a parameter. Let's approximate the equation by constructing vectors
$$
\begin{aligned}
\vec{x} &= [x_1, x_2, \dots, x_M]^T, \\
\vec{y} &= [y_1, y_2, \dots, y_N]^T, \\
\vec{u} &= [u(x_1), u(x_2), \dots, u(x_M)]^T, \\
\vec{f} &= [f(y_1), f(y_2), \dots, f(y_N)]^T,
\end{aligned}
$$
and the matrix
$$
A = [w_jK(x_i, y_j)]_{M \times K}.
$$
The equation now becomes
$$
A\vec{f} = \vec{u}.
$$
Let's calculate the condition number of some matrices $A$ for various numbers of $N$. Let's fix $\sigma = 0.05$, and $M = 500$. The plots of $\log(C(A_N))$, where $C(A)$ is the condition number of $A$, are displayed below.
![[ex_3_condition.png]]
$N$s are varying from $2$ to $1000$, we can see a peak at $N=500$, where the matrix becomes a square matrix. Also the curve changes regime at $N = 60$, $N = 270$, and $N = 915$.

We can see that the matrix is ill-conditioned due to its enormous condition number, even for small $N$, so we will not be able to find the vector $\vec{f}$ from our linear system.

We will use a method of truncated singular value decomposition. We factorise the matrix $A$ as 
$$
A = U \Sigma V,
$$
where $U$ and $V$ are square unitary matrices, and $\Sigma$ is a rectangular diagonal matrix. Due to the fact that $\Sigma$ contains very small numbers we choose a cutoff point $a$, and we set all of the values  We then "invert" the matrix $A$ as follows
$$
A^{-1} = \left(U \Sigma V\right)^{-1} = V^{-1} \Sigma^{-1} U^{-1} = V^T \Sigma^{-1} U^T, 
$$
since the transpose of a unitary matrix is its inverse. To "invert" $\Sigma$ we decide on a cutoff point $a$, and we set $\Sigma^{-1}_{m, n}$  to be $\frac{1}{\Sigma_{m, n}}$ if $\Sigma_{m, n} \gt a$, and $0$ otherwise. We can then find $\vec{f}$ with
$$
\vec{f} = A^{-1}\vec{u}.
$$
Assume that $f(x) = H(x - 0.3) - H(x - 0.5)$, where $H$ is the Heavyside function. We will obtain $u$ by directly convolving $f$ and $K$, then we will get $f$ back using the described discretisation scheme.

![[ex_3_lines_1.png]]

![[ex_3_lines_2.png]]

![[ex_3_lines_3.png]]

![[ex_3_lines_4.png]]

![[ex_3_lines_5.png]]

Also, just for fun, I included a few cases where I modified $f$ a little bit:
$$
f(x) = H(x - 0.3) - H(x - 0.5) + H(x - 0.9) + 3x
$$
![[ex_3_lines_6.png]]

$$
f(x) = H(x - 0.2) + H(x - 0.5) + H(x - 0.7) + H(x - 0.9)
$$
![[ex_3_lines_7.png]]

$$
f(x) = -x + \sin(8x) + H(x - 0.2) + H(x - 0.5) - H(x - 0.8)
$$
![[ex_3_lines_8.png]]

As we can see the discretisation and the singular value decomposition do a really good job at deblurring the images.
