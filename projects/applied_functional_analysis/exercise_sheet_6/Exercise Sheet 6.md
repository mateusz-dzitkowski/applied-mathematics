# Applied Functional Analysis - Exercise sheet 6
Mateusz Dzitkowski, 249777

## Exercise 1
Let's prove that the functional $J$ given by
$$
J(u) = \frac{1}{2}\int_0^1\left(u(x) - f_\delta(x)\right)^2dx + \frac{\alpha}{2}\int_0^1|u'(x)|^2dx
$$
has a unique minimum, which is achieved at the function $u_\alpha \in H_0^1(0, 1)$, which is a weak solution to the problem
$$
\begin{cases}
u - \alpha u'' = f_\delta, \\
u(0) = u(1) = 0.
\end{cases}
$$
To that end notice that
$$
\begin{aligned}
J(u) &= \frac{1}{2}\int_0^1u(x)^2dx + \frac{\alpha}{2}\int_0^1|u'(x)|^2dx - \int_0^1u(x)f_\delta(x)dx + \frac{1}{2}\int_0^1f_\delta(x)^2dx = \\
&= J^*(u) + \frac{1}{2}\int_0^1f_\delta(x)^2dx = J^*(u) + C,
\end{aligned}
$$
where $C$ is independent of $u$. This means that the $u$ that minimises $J$ is the same $u$ that minimises $J^*$. Let's take a look at the differential equation, we have
$$
u - \alpha u'' = f_\delta.
$$
Now multiply the equation by a function $v \in H_0^1(0, 1)$:
$$
uv - \alpha u''v = f_\delta v,
$$
and integrate both sides:
$$
\int_0^1uvdx - \alpha\int_0^1u''vdx = \int_0^1f_\delta vdx.
$$
Using integration by parts we get
$$
\int_0^1uvdx + \alpha\int_0^1u'v'dx = \int_0^1f_\delta vdx,
$$
or
$$
a(u, v) = l(v),
$$
with
$$
a(u, v) = \int_0^1uvdx + \alpha\int_0^1u'v'dx, \quad l(v) = \int_0^1f_\delta vdx.
$$
Notice, that $J(u) = \frac{1}{2}a(u, u) - l(u)$. We can also see that
$$
a(u, v) = \int_0^1uvdx + \alpha\int_0^1u'v'dx = \int_0^1vudx + \alpha\int_0^1v'u'dx = a(v, u),
$$
so $a$ is symmetric, and
$$
a(u, u) = \int_0^1u^2dx + \alpha\int_0^1u'^2 \ge 0,
$$
so $a$ is also positive. Using one of the theorems presented at the lecture we can conclude that $J^*$, and hence $J$, has a unique minimum, which is a weak solution to
$$
\begin{cases}
u - \alpha u'' = f_\delta, \\
u(0) = u(1) = 0.
\end{cases}
$$
Now let's solve the above equation numerically. Let $f(x) = \sin(2\pi x)$, $n_\delta(x) = \sqrt{2}\delta\sin(2\pi kx)$, and $f_\delta(x) = f(x) + n_\delta(x)$, as in the last exercise sheet.

We are going to use the finite difference method described in the notes. Below we can see the plots of the solution

![[lines_1_1.png]]

![[lines_1_2.png]]

 and the derivatives of the solution $u$, $f$, and $f_\delta$:
 ![[lines_1_3.png]]
 ![[lines_1_4.png]]
 
 As we can see, the Tikhonov regularisation works very well in this example. We can also investigate the errors $||u_\alpha - f||$ of the numerical solution. Below we can see three plots with varying $\delta$, where the $x$ axis is $\alpha$.
 ![[lines_1_5.png]]
 
![[lines_1_6.png]]

![[lines_1_7.png]]
As we can see, the minimum is achieved at a very small alpha.
Unfortunately, due to time constraints, and the fact that I couldn't easily derive the bound for the norm of the difference $u_\alpha' - f'$, I will not be adding my solution here, I understand that I will get some points deducted, and I'm fine with that.

## Exercise 2
Let's solve the following ordinary differential equation:
$$
-\left(a(x)u'(x)\right)' = f(x),
$$
for $a$. To that end, multiply by $-1$, and integrate both sides of the equation:
$$
a(x)u'(x) = C - \int_0^xf(y)dy,
$$
and then divide by $u'(x)$:
$$
a(x) = \frac{1}{u'(x)}\left(C - \int_0^xf(y)dy\right).
$$
We can see that the instability in determining $a$ from the measurements of $u$ might arise in a case where $u$ is approximately constant on some interval. It would, in fact, be impossible, if $u$ was exactly constant on a some interval.

Assume that $f(x) = -1$, $u(x) = x$, and the boundary conditions are $a(0)u'(0) = 0$, $a(1)u'(1) = 1$.
The solution to that particular problem becomes
$$
a(x) = x.
$$
Now assume that $u$ is perturbed to 
$$
u_\delta(x) = x + \delta\sin\left(\frac{x}{\delta^2}\right).
$$
 We have
$$
u_\delta'(x) = 1 + \frac{1}{\delta}\cos\left(\frac{x}{\delta^2}\right).
$$
Solution $a$ then becomes 
$$
a(x) = \frac{x}{1 + \frac{1}{\delta}\cos\left(\frac{x}{\delta^2}\right)}.
$$
The function $u_\delta$ approaches $u(x) = x$ as $\delta$ approaches zero, but $a$ doesn't approach $x$. The $\frac{1}{\delta}\cos\left(\frac{x}{\delta^2}\right)$ part will approach infinity everywhere but at the points where $\cos\left(\frac{x}{\delta^2}\right)$ is close to zero, and so $a(x)$ will have sudden spikes wherever $\cos\left(\frac{x}{\delta^2}\right) \approx -\delta$. We can see that even small perturbations in $u$ can have a big effect on $a$. Hence, the coefficient identification problem is not stable with respect to perturbations in $u$.

Now let's assume that functions $u_1$, and $u_2$ are solutions to the ODE at hand, with coefficients $a_1$, and $a_2$ respectively, so that
$$
\begin{aligned}
-\left(a_1(x)u_1'(x)\right)' &= f(x) \\
-\left(a_2(x)u_2'(x)\right)' &= f(x).
\end{aligned}
$$
Let's subtract the first equation from the other:
$$
\left(a_1(x)u_1'(x) - a_2(x)u_2'(x)\right)' = 0,
$$
integrating, and assuming that $a_1(0)u_1'(0) = a_2(0)u_2'(0) = 0$, we get
$$
a_1(x)u_1'(x) = a_2(x)u_2'(x),
$$
or
$$
a_2(x) = a_1(x)\frac{u_1'(x)}{u_2'(x)},
$$
so that 
$$
||a_1 - a_2|| = \left\Vert a_1(x)\left(1 - \frac{u_1'(x)}{u_2'(x)}\right) \right\Vert.
$$
Now I don't know what to do with this, so I'm gonna give up right there knowing that I'll get points deducted for that.

To illustrate the problem we can plot the solutions $a$, and $a_\delta$. We discretise the problem on the unit interval with $n$ equally spaced points. First, the normal solution without perturbation:

![[lines_2_2.png]]

Now, let's add a perturbation. The perturbed function $u_\delta$ looks as follows:

![[lines_2_1.png]]

And the solution for different values of $\delta$:

![[lines_2_3.png]]

![[lines_2_4.png]]

![[lines_2_5.png]]

![[lines_2_6.png]]
