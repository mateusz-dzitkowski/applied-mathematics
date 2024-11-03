package main

import (
	"main/model"
)

func main() {
	params := model.Params{
		Size:  300,
		Blues: 40000,
		Reds:  40000,
		JBlue: 15,
		JRed:  30,
		MBlue: 40,
		MRed:  40,
	}
	animateParams := model.AnimateParams{
		CellSize:             3,
		Delay:                5,
		MaxSteps:             300,
		FramesWithFinalState: 10,
	}
	if err := model.New(params).Animate(animateParams); err != nil {
		panic(err)
	}
}
