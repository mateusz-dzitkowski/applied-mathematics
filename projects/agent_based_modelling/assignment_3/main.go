package main

import (
	"fmt"
	"main/model/grid"
)

func main() {
	g := grid.New[string](5)
	g.Set(grid.Pos{X: 1, Y: 2}, "a")
	g.Set(grid.Pos{X: 3, Y: 4}, "a")
	g.Set(grid.Pos{X: 4, Y: 4}, "a")
	fmt.Println(g.GetClosestNeighbours(grid.Pos{X: 1, Y: 1}, 2))
}
