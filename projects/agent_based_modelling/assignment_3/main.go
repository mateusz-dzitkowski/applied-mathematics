package main

import (
	"fmt"
	"main/model"
)

func main() {
	params := model.Params{
		Size:  1000,
		Blues: 400000,
		Reds:  400000,
		JBlue: 6,
		JRed:  6,
		MBlue: 8,
		MRed:  8,
	}
	animateParams := model.AnimateParams{
		FileName:             "test.gif",
		CellSize:             1,
		Delay:                10,
		MaxSteps:             1000,
		FramesWithFinalState: 10,
	}

	err := model.New(params).Animate(animateParams)
	if err != nil {
		fmt.Println(err)
	}
}
