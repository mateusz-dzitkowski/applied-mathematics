# 1. Summary of net and gross premiums
### Def 1.1 (Age of death)
Define $X$, a random variable, to be the age of death of a newborn. $X$ is assumed to be a continuous, non-negative random variable. 
We have:
- $F_X(x) = P(X \le x)$,
- $S(x) := 1 - F_X(x) = P(X \ge x)$ - survival function, probability that a newborn will survive to $x$,
- $f_x(x) = F'_X(x)$
Let us also define $(x)$ to be a life aged $(x)$, usually meant as a person aged $x$ years.
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
- $\mu_x = \frac{F'(x)}{1-F(x)} = \frac{f(x)}{\int_x^\infty f(s)ds} = -\frac{S'(x)}{S(x)}$
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
- $T(x)$ - insurances payable at the moment of death,
- $K(x)$ - insurances payable at the end of year of death.
