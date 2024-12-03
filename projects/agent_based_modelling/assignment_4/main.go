package main

import (
	"main/batch"
	"main/model"
)

func main() {
	run()
}

func run() {
	params := model.Params{
		MaxVelocity:           5,
		RoadLength:            100,
		CarDensity:            0.4,
		DecelerateProbability: 0.4,
	}
	steps := 100

	model.New(params).Run(steps)
}

func plot() {
	batch.PlotMeanVelocities()
}
