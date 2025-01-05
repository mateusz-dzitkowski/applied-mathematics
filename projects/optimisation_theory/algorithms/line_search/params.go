package line_search

import "errors"

const BadDomainConstraints string = "bad domain constraints"
const EpsIsNotPositive string = "eps is not positive"
const MaxItersIsNotPositive string = "maxIters is not positive"

type Params struct {
	F        func(float64) float64
	A        float64
	B        float64
	Eps      float64
	MaxIters int64
}

func (p Params) validate() error {
	if p.B < p.A {
		return errors.New(BadDomainConstraints)
	}
	if p.Eps <= 0 {
		return errors.New(EpsIsNotPositive)
	}
	if p.MaxIters <= 0 {
		return errors.New(MaxItersIsNotPositive)
	}
	return nil
}
