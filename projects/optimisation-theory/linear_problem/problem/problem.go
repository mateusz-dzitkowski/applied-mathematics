package problem

import (
	"gonum.org/v1/gonum/mat"
	"gonum.org/v1/gonum/optimize/convex/lp"
)

type Emission uint

const (
	EmissionSO2 Emission = iota
	EmissionParticulate
)

type EmissionStore interface {
	AllEmissions() []Emission
	Get(Emission) float64
}

type Emissions struct {
	SO2, Particulate float64
}

func (e Emissions) AllEmissions() []Emission {
	return []Emission{EmissionSO2, EmissionParticulate}
}

func (e Emissions) Get(emission Emission) float64 {
	output, _ := map[Emission]float64{
		EmissionSO2:         e.SO2,
		EmissionParticulate: e.Particulate,
	}[emission]
	return output
}

type Incinerator struct {
	DailyCapacityTons float64
	CostPerTon        float64
	EmissionsPerTon   EmissionStore
}

type Problem struct {
	TonsOfTrashPerDay    float64
	Incinerators         []Incinerator
	EmissionLimitsPerDay EmissionStore
	EmissionsCost        EmissionStore
}

func MainProblem() Problem {
	return Problem{
		TonsOfTrashPerDay: 7500,
		Incinerators: []Incinerator{
			{
				DailyCapacityTons: 1900,
				CostPerTon:        16,
				EmissionsPerTon: Emissions{
					SO2:         120,
					Particulate: 18,
				},
			},
			{
				DailyCapacityTons: 3000,
				CostPerTon:        13,
				EmissionsPerTon: Emissions{
					SO2:         230,
					Particulate: 20,
				},
			},
			{
				DailyCapacityTons: 1800,
				CostPerTon:        13,
				EmissionsPerTon: Emissions{
					SO2:         150,
					Particulate: 30,
				},
			},
			{
				DailyCapacityTons: 2300,
				CostPerTon:        13,
				EmissionsPerTon: Emissions{
					SO2:         250,
					Particulate: 29,
				},
			},
		},
		EmissionLimitsPerDay: Emissions{
			SO2:         1000000,
			Particulate: 100000,
		},
		EmissionsCost: Emissions{
			SO2:         100,
			Particulate: 400,
		},
	}
}

func (p Problem) Solve() ([]float64, error) {
	//	minimize cᵀ * x
	//	s.t      G * x <= h
	//	         A * x = b

	c, A, b := p.convert()
	_, optX, err := lp.Simplex(c, A, b, 1e-10, nil)
	if err != nil {
		return nil, err
	}
	return optX[:p.incinerators()], err
}

func (p Problem) convert() ([]float64, *mat.Dense, []float64) {
	return lp.Convert(p.getC(), p.getG(), p.getH(), p.getA(), p.getB())
}

func (p Problem) emissionTypes() int {
	return len(p.EmissionsCost.AllEmissions())
}

func (p Problem) incinerators() int {
	return len(p.Incinerators)
}

func (p Problem) n() int {
	return p.incinerators() + p.emissionTypes()
}

func (p Problem) getC() []float64 {
	output := make([]float64, p.n())
	for row, incinerator := range p.Incinerators { // x * x's costPerTon
		output[row] = incinerator.CostPerTon
	}
	for row, emissionType := range p.EmissionsCost.AllEmissions() { // excess emissions * excess emissions cost per ton
		row += p.incinerators()
		output[row] = p.EmissionsCost.Get(emissionType)
	}
	return output
}

func (p Problem) getG() mat.Matrix {
	rows := 2 * p.n()
	cols := p.n()

	G := mat.NewDense(rows, cols, nil)
	for row := range p.incinerators() { // x <= x's daily capacity
		insertedRow := make([]float64, cols)
		insertedRow[row] = 1
		G.SetRow(row, insertedRow)
	}
	for row, emissionType := range p.EmissionsCost.AllEmissions() { // x*emissions - excess emissions <= emissions limit
		row += p.incinerators()
		insertedRow := make([]float64, cols)
		for i, incinerator := range p.Incinerators {
			insertedRow[i] = incinerator.EmissionsPerTon.Get(emissionType)
		}
		insertedRow[row] = -1
		G.SetRow(row, insertedRow)
	}
	for row := range p.n() { // x >= 0, and excess emissions >= 0
		insertedRow := make([]float64, cols)
		insertedRow[row] = -1
		G.SetRow(row+p.n(), insertedRow)
	}

	return G
}

func (p Problem) getH() []float64 {
	n := 2 * p.n()
	output := make([]float64, n)
	for row, incinerator := range p.Incinerators { // x <= x's daily capacity
		output[row] = incinerator.DailyCapacityTons
	}
	for row, emissionType := range p.EmissionsCost.AllEmissions() { // x*emissions - excess emissions <= emissions limit
		row += p.incinerators()
		output[row] = p.EmissionLimitsPerDay.Get(emissionType)
	}
	// implicitly the rest is 0, due to x >= 0, and excess emissions >= 0
	return output
}

func (p Problem) getA() mat.Matrix {
	data := make([]float64, p.n())
	for i := range p.incinerators() { // sum of all xs = total tons of trash per day
		data[i] = 1
	}
	// the rest after the p.incinerators() is 0 because we only count the incinerators tons
	// not the emission excess, which are only support variables
	return mat.NewDense(1, p.n(), data)
}

func (p Problem) getB() []float64 {
	return []float64{p.TonsOfTrashPerDay} // sum of all xs = total tons of trash per day
}
