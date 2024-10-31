package main

import (
	"fmt"
	"main/model"
)

func main() {
	params := model.Params{
		Size:  100,
		Blues: 4999,
		Reds:  4999,
		JBlue: 4,
		JRed:  4,
		MBlue: 8,
		MRed:  8,
	}
	m := model.New(params)

	fmt.Println(m)
	_ = m.Run(100)
	fmt.Println(m)
}
