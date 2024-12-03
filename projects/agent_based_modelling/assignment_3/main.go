package main

import (
	"image/color"
	"main/batch"
	"main/model"
)

var (
	ColorRed   = color.RGBA{R: 255, A: 255}
	ColorBlue  = color.RGBA{B: 255, A: 255}
	ColorGreen = color.RGBA{G: 255, A: 255}
)

type CParams struct {
	Red, Green, Blue model.ColorParams
}

func (p CParams) GetAllColors() []color.RGBA {
	return []color.RGBA{ColorRed, ColorBlue, ColorGreen}
}

func (p CParams) GetColorParam(rgba color.RGBA) model.ColorParams {
	if rgba == ColorRed {
		return p.Red
	} else if rgba == ColorGreen {
		return p.Green
	} else {
		return p.Blue
	}
}

func main() {
	plot()
}

func run() {
	params := model.Params{
		Size: 100,
		CParamsStore: CParams{
			Red: model.ColorParams{
				Population: 4000,
				M:          1,
				J:          3.0 / 8.0,
			},
			Green: model.ColorParams{
				Population: 0,
				M:          0,
				J:          0,
			},
			Blue: model.ColorParams{
				Population: 4000,
				M:          1,
				J:          6.0 / 8.0,
			},
		},
	}
	animateParams := model.AnimateParams{
		CellSize:              10,
		Delay:                 10,
		MaxSteps:              100,
		SecondsWithFinalState: 2,
	}
	if err := model.New(params).Animate(animateParams); err != nil {
		panic(err)
	}
}

func plot() {
	batch.PlotSegIndexPerJ()
}
