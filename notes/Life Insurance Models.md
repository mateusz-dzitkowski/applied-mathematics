# 1. Summary of net and gross premiums
### Def 1.1 (Age of death)
Define $X$, a random variable, to be the age of death of a newborn. $X$ is assumed to be a continuous, non-negative random variable. 
We have:
- $F_X(x) = P(X \le x)$,
- $S(x) = 1 - F_X(x) = P(X \ge x)$ - survival function, probability that a newborn will survive to $x$,
- $f_x(x) = F'_X(x)$
Let us also define $(x)$ to be a life aged $x$, usually meant as a person aged $x$ years.
### Def 1.2 (Future lifetime)
Define $T(x)$ to be the future lifetime of $(x)$, the amount of time that a person aged $x$ will live starting now. $T(x)$ is also a continuous, non-negative random variable, similar to $X$.
We have:
 - $G(t) = G_{T(x)}(t) = P(T(x) \le t)$
### Def 1.3 (Probability symbols)
Define the following:
- $_tp_x = P(T(x) \ge t) = P(X-x \ge t | X \ge x)$ 
- $_tq_x = 1 - _tp_x = G(t)$
- $K(x)$ - curtate future lifetime of $(x)$, $k(x) = \lfloor T(x) \rfloor$,
- $_{t|u}q_x = P(t \le T(x) \leq t + u) = _{t+u}q_x - _tq_x$ - probability that $(x)$ will survive $t$ years, and die within the following $u$ years.
Let us also define a convention regarding $p$ and $q$ functions:
- $_1p_x = p_x$,
- $_1q_x = q_x$.
### Def 1.4 (Force of mortality)
Define $\mu_x$ to be the force of mortality at age $x$. $\mu_x = -\frac{S'(x)}{S(x)}, \mu_x \ge  0$.
### Theorem 1.1 (Relationships)
The following equalities are true:
- $F(x) = \int_0^\infty f(s)ds = 1 - s(x) = 1 - \exp(-\int_0^x\mu_sds)$,
- $f(x) = F'(x) = -S'(x) = \mu_x\exp(-\int_0^x\mu_sds)$,
- $S(x) = 1 - F(x) = 1 - \int_0^\infty f(s)ds = \exp(-\int_0^x\mu_sds)$,
- $\mu_x = \frac{F'(x)}{1-F(x)} = \frac{f(x)}{\int_x^\infty f(s)ds} = -\frac{S'(x)}{S(x)}$.
### Def 1.5 (UDD)
The uniform distribution of deaths (UDD) assumption assumes the following:
$$
S(x+1) = (1-t)S(x) + tS(x+1), 0 \leq t \leq 1.
$$
It also implies that
$$
_tq_x = tq_x, 0 \leq t \leq 1,
$$
and that $K(x)$ and $S(x)$ are independent.
### Def 1.6 (Life insurance products)
Typical life insurance products:
1) Whole life insurance,
2) $n$-year term insurance,
3) $n$-year pure endearment,
4) $n$ - year endearment,
5) annuities,
6) unit - united life insurance.
We have:
- $T = T(x)$ - insurances payable at the moment of death,
- $K = K(x)$ - insurances payable at the end of year of death.
### Def 1.7 (Net single premium)
Let $A_x$, and $\overline{A}_x$ indicate the life insurance benefit of $1$ payable at the end of the year of death, and at the time of death, respectively. These two cases correspond to discrete, and continuous models. Let $b_t$ be the benefit function, $v_t$ be the discount function. Let $Z = Z_t = b_tv_t$.
Then the net single premium is defined as
$$
NSP = E[Z] = \overline{A}_x = \int_0^\infty v_tg(t)dt.
$$
Usually we take $b_t = 1$, and $v_t = v^t$, with a fixed $v$. Then the $NSP$ takes the following form
$$
NSP = \int_0^\infty v^t{}_tp_x\mu_{x+t}dt,
$$
with $v=e^{-\delta}$.
In the discrete case, substitute $t=k+1$, and $v=\frac{1}{1+i}$, then we have
$$
NSP = \sum_{k=0}^\infty v^{k+1}{}_kp_xq_{x+k}.
$$
Now let's explicitly define the life insurance benefits:
$$
\begin{aligned}
\overline{A}_x &= \int_0^\infty v^t{}_tp_x\mu_{x+t}dt, \\
\overline{A}_{x:\overline{n}|} &= \int_0^nv^t{}_tp_x\mu_{x+t}dt
\end{aligned}
$$
### Def 1.8 (Life annuity)
A life annuity is a series of periodic or continuous payments provided that the insured is alive. We have $Y$ - present value of future whole life annuity
$$
\begin{aligned}
Y &= \int_0^Tv^tdt = \overline{a}_{\overline{T}|}, \\
v &= e^{-\delta}, \\
\overline{a}_{\overline{T}|} &= \frac{1 - v^T}{\delta}.
\end{aligned}
$$
