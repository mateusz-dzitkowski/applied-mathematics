package main

import (
	"fmt"
	"main/tree"
)

const (
	BLUE = "blue"
	RED  = "red"
)

type Agent struct {
	color string
}

func main() {
	t := tree.New[Agent]()
	agents := []tree.Object[Agent]{
		{Pos: tree.Position{X: 3, Y: 3}, Props: Agent{color: RED}},
		{Pos: tree.Position{X: 2, Y: 4}, Props: Agent{color: BLUE}},
		{Pos: tree.Position{X: 3, Y: 5}, Props: Agent{color: RED}},
		{Pos: tree.Position{X: 1, Y: 2}, Props: Agent{color: BLUE}},
		{Pos: tree.Position{X: 3, Y: 1}, Props: Agent{color: RED}},
		{Pos: tree.Position{X: 4, Y: 3}, Props: Agent{color: RED}},
		{Pos: tree.Position{X: 5, Y: 1}, Props: Agent{color: RED}},
	}
	for _, agent := range agents {
		t.Insert(agent)
	}
	fmt.Println(t.FindKNearestNeighbours(tree.Position{X: 3, Y: 4}, 9))
}
