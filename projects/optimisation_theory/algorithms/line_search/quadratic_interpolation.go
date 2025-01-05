package line_search

import (
	"errors"
	"fmt"
	"math"
)

func QuadraticInterpolation(p Params) (float64, error) {
	if err := p.validate(); err != nil {
		return 0, err
	}

	a, b, c, err := daviesSwannCampey(p.F, (p.A+p.B)/2, p.Eps, p.MaxIters)
	if err != nil {
		return 0, err
	}
	fmt.Println(a, b, c)

	xStar := b + p.Eps
	xDash := c
	var d float64

	for range p.MaxIters {
		if math.Abs(xStar-xDash) < p.Eps {
			return xDash, nil
		}

		xStar = xDash
		xDash = (math.Pow(b, 2)*p.F(a) + (math.Pow(c, 2)-math.Pow(a, 2))*p.F(b) + (math.Pow(a, 2)-math.Pow(b, 2))*p.F(c)) / 2 / ((b-c)*p.F(a) + (c-a)*p.F(b) + (a-b)*p.F(c))

		if xDash > c {
			d = xDash
		} else {
			d = c
			c = xDash
		}

		if p.F(c) < p.F(d) {
			b = d
		} else {
			a = c
			c = d
		}
	}

	return 0, errors.New("cant find the optimum")
}

func daviesSwannCampey(f func(float64) float64, x0 float64, eps float64, maxIters int64) (a float64, b float64, c float64, err error) {
	delta0 := 1.0
	K := 0.1
	keepGoing := true
	var d float64
	for range maxIters {
		if delta0 <= eps || !keepGoing {
			return a, b, c, nil
		}

		delta := delta0
		if f(x0) < f(x0-delta) && f(x0) < f(x0+delta) {
			a = x0 - delta
			b = x0 + delta
			c = x0
			keepGoing = false
		} else {
			if f(x0-delta) < f(x0+delta) {
				d = -1
			} else {
				d = 1
			}

			x0 = x0 - d*delta
			f1 := f(x0 + d*delta)
			f2 := f(x0 + 2*d*delta)

			for f2 < f1 && delta != math.Inf(int(d)) {
				delta *= 2
				f1 = f2
				f2 = f(x0 + 2*d*delta)
			}

			if delta != math.Inf(int(d)) {
				c = x0 + d*delta
				a = c - delta
				b = c + delta
				keepGoing = false
			} else {
				delta0 = K * delta0
			}
		}
	}
	return 0, 0, 0, errors.New("cant find c")
}
