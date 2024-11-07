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
	Blues, Reds, Greens, MBlue, MRed, MGreen int
	JBlue, JRed, JGreen                      float64
}

func (p CParams) GetAllColors() []color.RGBA {
	return []color.RGBA{ColorRed, ColorBlue, ColorGreen}
}

func (p CParams) GetCParam(rgba color.RGBA) model.ColorParams {
	if rgba == ColorRed {
		return model.ColorParams{
			Population: p.Reds,
			M:          p.MRed,
			J:          p.JRed,
		}
	} else if rgba == ColorGreen {
		return model.ColorParams{
			Population: p.Greens,
			M:          p.MGreen,
			J:          p.JGreen,
		}
	} else {
		return model.ColorParams{
			Population: p.Blues,
			M:          p.MBlue,
			J:          p.JBlue,
		}
	}
}

func main() {
	run()
}

func run() {
	params := model.Params{
		Size: 100,
		CParamsStore: CParams{
			Blues:  3000,
			Reds:   3000,
			Greens: 3000,
			MBlue:  1,
			MRed:   1,
			MGreen: 1,
			JBlue:  0.6,
			JRed:   0.6,
			JGreen: 0.6,
		},
	}
	animateParams := model.AnimateParams{
		CellSize:             10,
		Delay:                5,
		MaxSteps:             1000,
		FramesWithFinalState: 10,
	}
	if err := model.New(params).Animate(animateParams); err != nil {
		panic(err)
	}
}

func plot() {
	batch.PlotNumOfIterationsPerPopulationSize()
}
