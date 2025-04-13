Mateusz Dzitkowski 249777
# Problem 4
$$
-\frac{d}{dx}\left(a(x)u'(x)\right) = f(x), \quad x \in (0, 1)
$$
Solving the equation for $a$:
$$
d\left(a(x)u'(x)\right) = -f(x)dx
$$
$$
\int_0^x d\left(a(s)u'(s)\right) = -\int_0^xf(x)dx
$$
Let $F(x) = \int_0^xf(s)ds$:
$$
a(x)u'(x) = A - F(x)
$$
We'll use the above equation to determine $A$ from the initial conditions. $a$ is defined by
$$
a(x) = \frac{A - F(x)}{u'(x)}.
$$
As we can see, the method may become unstable whenever $u$ is approximately constant in a given interval, due to denominator being close to zero.

Suppose
$$
f(x) = -1, \quad u(x) = x,
$$
and
$$
a(0)u'(0) = 0, \quad a(1)u'(1) = 1.
$$
Then
$$
F(x) = -x, \quad u'(x) = 1,
$$
and
$$
0 = A + 0, \quad 1 = A + 1,
$$
so $A = 0$, and we have an explicit expression for $a$:
$$
a(x) = x.
$$
Let's assume $u$ is perturbed by $n_\delta(x) = \delta\sin\left(\frac{x}{\delta^2}\right)$. Then $n_\delta'(x) = \frac{1}{\delta}\cos\left(\frac{x}{\delta^2}\right)$, and
$$
a_\delta(x) = \frac{x}{1 + \frac{1}{\delta}\cos\left(\frac{x}{\delta^2}\right)}.
$$
Let's investigate the limits of $u_\delta$ and $a_\delta$ when $\delta$ goes to zero. We have
$$
||u_\delta - u||_{L^\infty} = ||\delta\sin\left(\frac{x}{\delta^2}\right)||_{L^\infty} = \delta,
$$
and
$$
||a_\delta - a||_{L^\infty} = \left\Vert\frac{x}{1+\frac{1}{\delta}\cos\left(\frac{x}{\delta^2}\right)} - x\right\Vert_{L^\infty}.
$$
Notice that, given small enough $\delta$, the denominator $1+\frac{1}{\delta}\cos\left(\frac{x}{\delta^2}\right)$ will blow up at some point. It is enough for $\delta$ to be smaller than $\frac{1}{\sqrt{\pi}}$. Then the norm will also blow up to infinity.
Below are a few figures illustrating the issue with decreasing values of $\delta$
![[0401.png]]
![[0402.png]]
![[0403.png]]
![[0404.png]]

# Problem 5
$$
mu'' + cu' + ku = 0, \quad u(0)=u_0, \quad u'(0)=u_1
$$
transformed into
$$
u'' + au' + bu = 0, \quad u(0)=u_0, \quad u'(0)=u_1
$$
Let's analyse the uniqueness of the inverse problem of determining the coefficients $a$ and $b$ from data $u$:
Assume there are two $a$ parameters possible for the same data $u$: $a_1$ and $a_2$.
Then
$$
u'' + a_1u' + bu = 0,
$$
and 
$$
u'' + a_2u' + bu = 0.
$$
subtracting one equation from the other we get
$$
(a_1 - a_2)u' = 0,
$$
so either $u'=0$, in which case the solution is constant (trivial solution), or $a_1 = a_2$.
Same procedure applies to $b$.

Now, let's solve the equation. Assume $u = e^{rx}$. Then we get the characteristic equation:
$$
r^2 + ar + b = 0,
$$
which solutions are
$$
r_\pm = \frac{1}{2}\left(-a \pm \sqrt{a^2-4b}\right).
$$
So we get
$$
u(x) = Ae^{r_+x} + Be^{r_-x}.
$$
To find $A$ and $B$ for given initial conditions we compute the derivative
$$
u'(x) = Ar_+e^{r_+x} + Br_-e^{r_-x},
$$
and we get the equations for $A$ and $B$:
$$
A + B = u_0,
$$
$$
Ar_+ + Br_- = u_1.
$$
Solving these we obtain
$$
A = \frac{u_1 - u_0r_-}{r_+ - r_-}
$$
and
$$
B = \frac{u_0r_+ - u_1}{r_+ - r_-}.
$$
In our concrete example $a=2$, $b=5$, $u_0=1$, and $u_1=-1$. We have
$$
r_\pm = -1 \pm2i,
$$
so, using the Euler identity
$$
u(x) = e^{-x}\cos(2x).
$$
The function $u$ with the uniform noise on the interval $[-\delta, \delta]$ added is shown below
![[0501.png]]
Now, let's integrate the equation twice. First integration yields
$$
u'(x) - u_1 + a(u(x) - u_0) + \int_0^xu(s)ds = 0,
$$
the second integration yields
$$
u(x) - u_0 - u_1x + a\int_0^x(u(t) - u_0)dt + \int_0^x\int_0^su(t)dtds = 0.
$$
We can transform the last double integral into a single integral by flipping the order of the integrals, and changing the limits of the integrals. This yields the required result
$$
u(x) - u_0 - u_1x + a\int_0^x(u(t) - u_0)dt + \int_0^xu(t)(x-t)dt = 0.
$$
We wish do discretise the equation by using the midpoint rule. Let $I_1(x)=\int_0^x(u(s)-u_0)ds$, $I_2(x)=\int_0^xu(t)(x-t)dt$, and $f(x) = u_0 + u_1x - u(x)$. Then we can write
$$
I_1(x)a + I_2(x)b = f(x).
$$
By discretising all three functions, and writing
$$
\begin{aligned}
\vec{I_1} &= [I_1(x_0), I_1(x_1), \dots, I_1(x_n)]^T, \\
\vec{I_2} &= [I_2(x_0), I_2(x_1), \dots, I_2(x_n)]^T, \\
\vec{f} &= [f(x_0), f(x_1), \dots, f(x_n)]^T,
\end{aligned}
$$
we can express the equation for $a$ and $b$ as
$$
\left[\vec{I_1}, \vec{I_2}\right][a, b]^T = \vec{f}.
$$
The solution with all $u$ $u^\delta$, and $u_{back}$ being visible on one plot is visible below
![[0502.png]]
Below we can see the plot of the average of errors in euclidean norm with respect to $\delta$, over $100$ runs
![[0503.png]]

Let's consider the minimisation problem
$$
\min\limits_{a, b}\frac{1}{2}||u - u^\delta||^2
$$
subject to the original equation with $a$ and $b$.
A sample solution is shown below
![[0504.png]]