package main

import (
	"fmt"
	"main/problem"
)

func main() {
	solution, err := problem.MainProblem().Solve()
	if err != nil {
		panic(err)
	}
	fmt.Println(solution)
}
