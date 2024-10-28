package main

import "main/tree"

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
		{1, 2, Agent{color: RED}},
		{1, 3, Agent{color: BLUE}},
		{2, 2, Agent{color: RED}},
		{3, 0, Agent{color: BLUE}},
		{3, 1, Agent{color: RED}},
	}
	for _, agent := range agents {
		t.Insert(agent)
	}
}
