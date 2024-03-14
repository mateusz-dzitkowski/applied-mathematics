# 1. Compounding
### Def 1.1 (Present and Future Values)
Define the following:
- Discrete time $t \in \{0, 1, 2, \dots \}$,
- One period compounding - the interest is compounded every year,
- $PV$ - present value,
- $FV$ - future value,
- $r$ - interest rate (e.g. $5\%$).
Then for $t=1$:
$$
FV = PV + rPV = PV(1+r),
$$
for $t=2$:
$$
FV = (1+r)(1+r)PV = PV(1+r)^2,
$$
for $t=n$:
$$
FV = PV(1+r)^n.
$$
### Def 1.2 (Frequent compounding)
Let $f$ be the number of times that interest rate is calculated within a unit time. For example, if we do it every third month, then $f=4$. We have
$$
FV = PV\left(1 + \frac{r}{f}\right)^{nf}.
$$
If we let $f \rightarrow \infty$, so that $nf -> t$, we get the continuous compounding formula
$$
FV = PVe^{rt}.
$$
### Def 1.3 (Discounting)
Discounting works the other way around:
$$
PV = FV\left(1 + \frac{r}{f}\right)^{-nf},
$$
and for the continuous case:
$$
PV = FVe^{-rt}.
$$
### Def 1.4 (Risk-Free Instrument)
A risk-free instrument is defined by
$$
B_t = B_0e^{rt},
$$
where $r$ is a risk-free interest rate. For discrete time we have
$$
B_n = B_0\left(1 + \frac{r}{f}\right)^{nf}.
$$
#### The goal
We want to find the fair price of some financial instrument/derivative, which is often defined with a function (called a payout function) of the asset price. For example, in the european call option
$$
C_T = (S_T - K)^+ = f(S_T),
$$
where $T$ is called the maturity date, $K$ is given and called the strike price, and $(x)^+ = \max\{x, 0\}$.
### Def 1.5 (Hedging)
A replication/hedging strategy is given by the following
$$
\varphi_t = (\alpha_t, \beta_t),
$$
where $\alpha_t$ is the amount of assets existing in the portfolio at time $t$, and $\beta_t$ is the amount of risk-free instruments $B_t$ in the portfolio at time $t$.
Note: $\alpha_t$ and $\beta_t$ can be negative, which corresponds to borrowing.
#### Example
Let $X$ be a derivative, for example 
$$
X = (S_1 - K)^+  = 
	\begin{cases}
	(S^u - K)^+ ,& \omega = \omega_1, \\
	(S^d - K)^+ ,& \omega = \omega_2.
	\end{cases}
$$
Let $x = V_1(\varphi)$ be the value of the portfolio. Let $B_0 = 1$. We have
$$
x = \alpha_1S_1 + B_1(1+r).
$$
Let $\alpha = \alpha_1$, and $\beta = \beta_1$. Looking for replication strategy $\varphi = (\alpha, \beta)$, we obtain the following equations:
$$
\begin{aligned}
\alpha S^u + B(1+r) &= x^u = (S^u - K)^+ \\
\alpha S^d + B(1+r) &= x^d = (S^d - K)^+.
\end{aligned}
$$
Then, solving for $\alpha$ and $\beta$, we have
$$
\alpha = \frac{x^u - x^d}{S^u - S^d}, \quad \beta = \frac{x^dS^u - x^uS^d}{(1 + r)(S^u - S^d)}.
$$
Hence the price equals (bruh, how?)
$$
\Pi(X) = \Pi_0(x) = \alpha S_0 + \beta.
$$
