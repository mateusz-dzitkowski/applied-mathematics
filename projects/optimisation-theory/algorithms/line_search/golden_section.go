package line_search

import (
	"errors"
	"math"
)

func GoldenSection(p Params) (float64, error) {
	if err := p.validate(); err != nil {
		return 0, err
	}

	xL := p.A
	xU := p.B
	K := (math.Sqrt(5) - 1) / 2

	xA := xU - K*(xU-xL)
	xB := xL + K*(xU-xL)
	fA := p.F(xA)
	fB := p.F(xB)

	for range p.MaxIters {
		if xU-xL < p.Eps {
			return (xU + xL) / 2, nil
		}

		if fA <= fB {
			xU = xB
			xB = xA
			xA = xU - K*(xU-xL)
			fB = fA
			fA = p.F(xA)
		} else {
			xL = xA
			xA = xB
			xB = xL + K*(xU-xL)
			fA = fB
			fB = p.F(xB)
		}
	}

	return 0, errors.New("cant find the optimum")
}
