Mateusz Dzitkowski 249777
# 1.1
$$
n^\delta(x) = \sqrt{2}\delta\sin(2\pi k x).
$$
$$
\left\Vert f - f^\delta \right\Vert = ||n^\delta||
$$
$$
\left\Vert f' - (f^\delta)' \right\Vert = ||(n^\delta)'||
$$
$$
||f-f^\delta||^2_{L^2} = \int_0^12\delta^2\sin(2\pi k x)^2dx = \delta^2\left(1 - \frac{1}{4\pi k}\sin(4\pi k)\right) \rightarrow 0.
$$
$$
||f' - (f^\delta)'||^2_{L^2} = \int_0^18\delta^2\pi^2k^2\cos(2\pi k x)dx = \pi \delta^2 k \left(4 \pi k + \sin(4\pi k)\right) \rightarrow \infty.
$$
$$
||f-f^\delta||_{L^\infty} = \max\limits_{x\in(0,1)}\left\{\sqrt{2}\delta\sin(2\pi k x)\right\} = \sqrt{2}\delta \rightarrow 0.
$$
$$
||f' - (f^\delta)'||_{L^\infty} = \max\limits_{x\in(0,1)}\left\{2\sqrt{2}\delta \pi k \cos(2\pi k x)\right\} = 2\sqrt{2}\delta \pi k \rightarrow \infty.
$$
# 1.2
![[sub_02.png]]
# 1.3
Let's estimate the error that we introduce when calculating the derivatives numerically using Euler central difference scheme, that is, let's estimate  
$$  
E_f = \left\Vert f'(x) - \frac{f(x+h) - f(x-h)}{2h}\right\Vert_{L^\infty}.  
$$
We know that 
$$
f(x+h) = f(x) + hf'(x) + \frac{h^2}{2}f''(\xi_+^x), \text{ where } \xi_+^x \in [x, x+h],
$$
and 
$$
f(x-h) = f(x) - hf'(x) + \frac{h^2}{2}f''(\xi_-^x), \text{ where } \xi_-^x \in [x-h, x].
$$
From that we get
$$
\begin{aligned}  
\frac{1}{2}\left\Vert f'(x) - \frac{f(x+h) - f(x)}{h}\right\Vert_{L^\infty}  &\le \left\Vert f'(x) - \frac{f(x+h) - f(x)}{h}\right\Vert_{L^\infty}  \le \frac{h}{2}|| f''(\xi_+)||_{L^\infty} \le \frac{h}{2}||f''||_{L^\infty} , \\  
\frac{1}{2}\left\Vert f'(x) - \frac{f(x) - f(x-h)}{h}\right\Vert_{L^\infty}  &\le \left\Vert f'(x) - \frac{f(x) - f(x-h)}{h}\right\Vert_{L^\infty}  \le \frac{h}{2}|| f''(\xi_-)||_{L^\infty} \le \frac{h}{2}||f''||_{L^\infty} ,  
\end{aligned}  
$$  
and, using the triangle equality we obtain an estimate  
$$  
\begin{aligned}  
E_f = \left\Vert f'(x) - \frac{f(x+h) - f(x-h)}{2h}\right\Vert_{L^\infty}  &= \left\Vert \frac{f'(x)}{2} - \frac{f(x+h) - f(x)}{2h} + \frac{f'(x)}{2} - \frac{f(x) - f(x-h)}{2h}\right\Vert_{L^\infty}  \le \\  
&\le \frac{h}{2}||f''||_{L^\infty}  + \frac{h}{2}||f''||_{L^\infty}  = h||f''||_{L^\infty}.
\end{aligned}  
$$  
Now, let's estimate the error when we differentiate data with noise, that is
$$
\begin{aligned}
&\left\Vert f'(x) - \frac{f^\delta(x + h) - f^\delta(x - h)}{2h} \right\Vert_{L^\infty} = \\=&\left\Vert f'(x) - \frac{f(x + h) - f(x - h)}{2h} - \frac{n^\delta(x + h) - n^\delta(x - h)}{2h} \right\Vert_{L^\infty} \le \\
\le &\left\Vert f'(x) - \frac{f(x + h) - f(x - h)}{2h}\right\Vert_{L^\infty} + \left\Vert\frac{n^\delta(x + h) - n^\delta(x - h)}{2h} \right\Vert_{L^\infty} \le \\
\le & h||f''||_{L^\infty} + \frac{1}{2h}\left\Vert n^\delta(x + h) - n^\delta(x - h) \right\Vert_{L^\infty}.
\end{aligned}
$$
Now, if we didn't know anything about the noise $n^\delta$, we would estimate this by using the Minkowski inequality, but in our scenario $n^\delta(x) = \sqrt{2}\delta\sin(2\pi k x)$, so
$$
n^\delta(x+h) - n^\delta(x-h) = 2\sqrt{2}\delta\cos(2 \pi k x)\sin(2 \pi k h),
$$
hence 
$$
\left\Vert n^\delta(x+h) - n^\delta(x-h) \right\Vert_{L^\infty} = 4\sqrt{2}\pi\delta kh,
$$
since $sin(x) \approx x$ for small $x$. Now the $L^\infty$ norm of the error can be estimated by
$$
\left\Vert f'(x) - \frac{f^\delta(x + h) - f^\delta(x - h)}{2h} \right\Vert_{L^\infty} \le h||f''||_{L^\infty} + 2\sqrt{2}\pi\delta k,
$$
which, in our concrete example, with 
$$
f(x) = \sin(2\pi x),
$$
becomes
$$
4\pi^2h + 2\sqrt{2}\pi\delta k.
$$
# 1.4

![[sub_04.png]]
As we can see, no matter how small $h$ we take, the differentiation error will not go down to zero, as expected.

# 1.5
![[sub_05a.png]]
![[sub_05b.png]]
# 1.6
![[sub_06a.png]]
![[sub_06b.png]]
# 1.7
The estimate given on the lecture says that the optimum value of $\alpha$ is
$$
\alpha = \frac{\delta}{\int_0^1\left|f''(x)\right|^2dx}.
$$
In our case $f(x) = \sin(2\pi x)$, so $f''(x)=-4\pi^2\sin(2\pi x)$, hence
$$
\int_0^1|f''(x)|^2dx = 4\pi^2\int_0^1|\sin(2\pi x)|^2dx = 2\pi^2.
$$
In our case, $\delta=0.01$, so 
$$
\alpha_{opt} = \frac{0.01}{2\pi^2} \approx 0.0005066.
$$
The numerical experiment yielded $0.0007939698492462312$, which is in the same order of magnitude.
