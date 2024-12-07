package model

import (
	"gonum.org/v1/gonum/mat"
	"gonum.org/v1/plot/plotter"
	"image/color"
)

func (m *Model) ToHeatMap(steps int) *plotter.HeatMap {
	dense := mat.NewDense(steps, m.params.RoadLength, nil)

	for r := range steps {
		row := make([]float64, m.params.RoadLength)
		for i, c := range m.Road.Lane {
			if c != nil {
				row[i] = 1
			}
		}
		dense.SetRow(steps-r-1, row)
		m.Step()
	}

	return plotter.NewHeatMap(unitGrid{d: dense}, myPalette{})
}

type unitGrid struct{ d *mat.Dense }

func (g unitGrid) Dims() (c, r int)   { r, c = g.d.Dims(); return c, r }
func (g unitGrid) Z(c, r int) float64 { return g.d.At(r, c) }
func (g unitGrid) X(c int) float64 {
	_, n := g.d.Dims()
	if c < 0 || c >= n {
		panic("index out of range")
	}
	return float64(c)
}
func (g unitGrid) Y(r int) float64 {
	m, _ := g.d.Dims()
	if r < 0 || r >= m {
		panic("index out of range")
	}
	return float64(r)
}

type myPalette struct{}

func (mp myPalette) Colors() []color.Color {
	return []color.Color{color.White, color.Black}
}
