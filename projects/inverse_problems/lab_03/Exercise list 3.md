Mateusz Dzitkowski 249777
# Problem 2
$$
f(x) = \int_0^1k(x, y)u(y)dy,
$$
with
$$
k(x, y) = 
\begin{cases}
	\frac{y}{T}(1-x),& y\in[0, x], \\
	\frac{x}{T}(1-y),& y\in[x,1],
\end{cases}
$$
and $T>0$.
Note that
$$
f(0) = f(1) = \int_0^10u(y)dy = 0.
$$
Let's compute the derivatives of $f$. We have
$$
\begin{aligned}
f'(x) &= \frac{1}{T}\frac{d}{dx}\left[\int_0^x(1-x)yu(y)dy + \int_x^1x(1-y)u(y)dy\right] = \\
&= \frac{1}{T}\frac{d}{dx}\left[\int_0^x(1-x)yu(y)dy - \int_1^xx(1-y)u(y)dy\right] = \\
&= \frac{1}{T}\left[(1-x)xu(x) - \int_0^xyu(y)dy - (1-x)xu(x) - \int_1^x(1-y)u(y)dy\right] = \\
&= \frac{1}{T}\left[-\int_0^xyu(y)dy - \int_1^x(1-y)u(y)dy\right],
\end{aligned}
$$
and
$$
\begin{aligned}
f''(x) = \frac{1}{T}\left[-xu(x) - (1-x)u(x)\right] = -\frac{1}{T}u(x).
\end{aligned}
$$
Then we obtain the equation
$$
Tf''(x) + u(x) = 0
$$
with boundary conditions
$$
f(0) = f(1) = 0.
$$
Let
$$
f(x) = (x-1)\sin(x),
$$
$$
n_\delta(x) = \delta(x-1)\sin\left(\frac{x}{\delta}\right),
$$
$$
n_\delta''(x) = 2\cos\left(\frac{x}{\delta}\right) - \frac{1}{\delta}(x-1)\sin\left(\frac{x}{\delta}\right),
$$
$$
f_\delta(x) = f(x) + n_\delta(x).
$$
Then we have
$$
||f - f_\delta||_{L^2}^2 = ||n_\delta||_{L^2}^2 = \delta^2\int_0^1(x-1)^2\sin\left(\frac{x}{\delta}\right)^2dx = \frac{\delta^2}{24}\left(3\delta^3\sin\left(\frac{2}{\delta}\right) - 6\delta^2 + 4\right),
$$
$$
||u-u_\delta||_{L^2}^2 = T^2||f'' - f_\delta''||_{L^2}^2 = T^2||n_\delta''||_{L^2}^2 = T^2\left(\frac{1}{6\delta^2} + \frac{5}{8}\delta\sin\left(\frac{2}{\delta}\right) + \frac{11}{4}\right),
$$
$$
||f - f_\delta||_{L^\infty} = T||n_\delta||_{L^\infty} = T\delta\max\limits_{x\in[0,1]}\left|(x-1)\sin\left(\frac{x}{\delta}\right)\right| \le T\delta,
$$
$$
\begin{aligned}
||u-u_\delta||_{L^\infty} &= T||n_\delta''||_{L^\infty} = \frac{T}{\delta^2}\max\limits_{x\in[0,1]}\left|2\cos\left(\frac{x}{\delta}\right) - \frac{1}{\delta}(x-1)\sin\left(\frac{x}{\delta}\right)\right| \ge \\
&\ge \frac{T}{\delta^2}\left|\max\limits_{x\in[0,1]}2\cos\left(\frac{x}{\delta}\right) - \max\limits_{x\in[0,1]}\frac{1}{\delta}(x-1)\sin\left(\frac{x}{\delta}\right)\right| \ge \frac{T}{\delta^2}\left|2 + \frac{1}{\delta}\right|.
\end{aligned}
$$
As we can see, even though $||f-f_\delta||$ stays small when $\delta$ is small, $||u-u_\delta||$ blows up, making the problem of determining $u$ from $f$ ill-posed.
# Problem 3
$$
f(x) = \int_{-1}^1k(x,y)u(y)dy,
$$
$$
k(x,y) = \frac{1}{\sqrt{2\pi}\sigma}\exp\left(-\frac{(x-y)^2}{2\sigma^2}\right).
$$
