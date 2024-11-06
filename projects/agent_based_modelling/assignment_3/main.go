package main

import (
	"main/batch"
	"main/model"
)

func main() {
	plot()
}

func run() {
	params := model.Params{
		Size:  1000,
		Blues: 400000,
		Reds:  400000,
		JBlue: 0.7,
		JRed:  0.7,
		MBlue: 3,
		MRed:  3,
	}
	animateParams := model.AnimateParams{
		CellSize:             1,
		Delay:                10,
		MaxSteps:             300,
		FramesWithFinalState: 10,
	}
	if err := model.New(params).Animate(animateParams); err != nil {
		panic(err)
	}
}

func plot() {
	batch.PlotNumOfIterationsPerPopulationSize()
}
