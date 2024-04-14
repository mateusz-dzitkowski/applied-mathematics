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
# 2. Whole life insurance
### Def 2.1 (L)
Let $L$ be the loss of insurance company, so $L=$ the present value of venefits-present value of premiums.
### Def 2.2 (Equivalence principle)
Net premium is calculated in such a way that $E[L] = 0$. So if
$$
L = v^{k+1} - p\ddot{a}_{\overline{k+1}|},
$$
then
$$
p_x = \frac{A_x}{\ddot{a}_x}.
$$
### Def 2.3 (Endowment)
Since $p_x = \frac{A_x}{\ddot{a}_x}$ describes the whole life premium, then let's define
$$
p_{x:\overline{n}|}^1 = \frac{A_{x:\overline{n}|}^1}{\ddot{a}_{x:\overline{n}|}} \text{ - term (?)},
$$
and
$$
p_{x:\overline{n}|} = \frac{A_{x:\overline{n}|}}{\ddot{a}_{x:\overline{n}|}} \text{ - endowment}.
$$
### Def 2.4 (Fully continuous case)
Let
$$
\overline{a}_t = \int_0^tv^sds,
$$
then
$$
L = v^T - \overline{p}_{\overline{a}_{\overline{T}|}},
$$
and
$$
\overline{p}_x = \frac{\overline{A}_x}{\overline{a}_x}.
$$
### Def 2.5 (gross premiums)
The continuous-discrete case:
$$
\begin{aligned}
p(\overline{A}_x) &= \frac{\overline{A}_x}{\ddot{a}_x}, \\
p(\overline{A}_{x:\overline{n}|}^1) &= \frac{\overline{A}_{x:\overline{n}|}^1}{\ddot{a}_{x:\overline{n}|}}, \\
p(\overline{A}_{x:\overline{n}|}) &= \frac{\overline{A}_{x:\overline{n}|}}{\ddot{a}_{x:\overline{n}|}}.\\
\end{aligned}
$$
The discrete-continuous case:
$$
\begin{aligned}
\overline{p} &= \frac{A_x}{\overline{a}_x}, \\
\overline{p}_{x:\overline{n}|}^1 &= \frac{A_{x:\overline{n}|}}{a_{x:\overline{n}|}}, \\
\overline{p}_{x:\overline{n}|} &= \frac{A_{x:\overline{n}|}}{\overline{a}_{x:\overline{n}|}}.\\
\end{aligned}
$$
### Def 2.6 (Gross premiums costs)
The costs of gross premiums consist of:
- Acquisition costs,
- Agent's common,
- Collection expenses,
- Administration costs,
- Claim hedging expenses.
### Def 2.7 (Equivalence principle)
Let $p_a = A$ (net premium), and $b_a = A + \cos{As}$ (gross premium).
Then ${}_tL$ - financial loss of an insurance company,
$$
{}_tL = Z - PY,
$$
where $Y$ - present value of future payments, $P$ - net premium, $Z$ - present value of future payments of the benefits.
Then the net reserve equals
$$
E[{}_tL] = {}_tV.
$$
### Def 2.8 (recursive formulas for net reserves)
Let:
- $b_k$ - sum insured in $k$-th year of the policy,
- $\pi_0, \pi_1, \dots, \pi_k$ - annual premiums paid up to the moment $k$,
- $L = Z - \sum_{m=0}^kz_mv^m =  b_{k+1}v^{k+1} - \sum_{m=0}^kz_mv^m$.
The recursive formula:
$$
{}_kV + \pi_k = V(b_{k+1}q{x+k} + {}_{k+1}Vp_{x+k}).
$$
Another form:
$$
{}_kV + \pi_k = v({}_{k+1}V + (b_{k+1} - {}_{k+1}V)q_{x+k}).
$$
This gives us a division of the premium $\pi_k$:
$$
\begin{aligned}
\pi_k &= \pi_k^s + \pi_k^r, \\
\pi_k^s &= {}_{k+1}V_{v} - {}_{k}V, \\
\pi_k^r &= (b_{k+1} - {}_{k+1}V)Vq_{x+k}.
\end{aligned}
$$
