package main

import (
	"main/model"
)

func main() {
	params := model.Params{
		Size:  1000,
		Blues: 400000,
		Reds:  400000,
		JBlue: 30,
		JRed:  30,
		MBlue: 50,
		MRed:  50,
	}
	animateParams := model.AnimateParams{
		CellSize:             1,
		Delay:                5,
		MaxSteps:             100,
		FramesWithFinalState: 10,
	}
	if err := model.New(params).Animate(animateParams); err != nil {
		panic(err)
	}
}
