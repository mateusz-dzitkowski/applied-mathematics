package main

import (
	"fmt"
	"main/line_search"
	"math"
)

func main() {
	opt, _ := line_search.GoldenSection(
		line_search.Params{
			func(x float64) float64 { return math.Pow(x, 2) },
			-1,
			2,
			0.001,
			100,
		},
	)
	fmt.Println(opt)
}
