package main

import (
	"main/batch"
	"main/model"
	plot2 "main/plot"
)

const (
	BaseMaxVelocity = 5
	BaseRoadLength  = 100
)

func main() {
	plotGrid()
}

func run() {
	params := model.Params{
		MaxVelocity:           5,
		RoadLength:            100,
		CarDensity:            0.2,
		DecelerateProbability: 0.4,
	}
	steps := 100
	model.New(params).Run(steps)
}

func plotGraph() {
	batch.PlotMeanVelocities()
}

func plotGrid() {
	densities := []float64{0.1, 0.3, 0.6}
	probabilities := []float64{0.0, 0.3, 0.6}

	paramsGrid := make([][]model.Params, len(densities))
	for i, density := range densities {
		paramsRow := make([]model.Params, len(probabilities))
		for j, probability := range probabilities {
			paramsRow[j] = model.Params{
				MaxVelocity:           BaseMaxVelocity,
				RoadLength:            BaseRoadLength,
				CarDensity:            density,
				DecelerateProbability: probability,
			}
		}
		paramsGrid[i] = paramsRow
	}

	if err := plot2.GridSave(paramsGrid, "grid.png"); err != nil {
		panic(err)
	}
}
