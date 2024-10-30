package main

import (
	"fmt"
	"main/model"
)

func main() {
	m := model.New(model.Params{Size: 100, Blues: 250, Reds: 250})
	fmt.Println(m.Tree.Points())
}
