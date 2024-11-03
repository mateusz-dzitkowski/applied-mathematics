package main

import (
	"fmt"
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
		CarDensity:            0.1,
		DecelerateProbability: 0.4,
	}
	m := model.New(params)
	for range 100 {
		fmt.Println(m)
		m.Step()
	}
}

func plot() {
	batch.PlotMeanVelocities()
}
