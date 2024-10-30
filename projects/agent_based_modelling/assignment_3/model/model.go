package model

import (
	"github.com/kyroy/kdtree"
	"main/model/agent"
	"main/model/unique_rand"
)

type Params struct{ Size, Reds, Blues, JRed, JBlue, MRed, MBlue int }

type Model struct {
	Params Params
	Tree   *kdtree.KDTree
}

func New(params Params) *Model {
	model := Model{
		Params: params,
		Tree:   kdtree.New([]kdtree.Point{}), // initialize as empty
	}

	uniqueRand := unique_rand.New()

	for range params.Reds {
		pair := uniqueRand.PairN(model.Params.Size)
		var p kdtree.Point = agent.NewRed(pair.X, pair.Y)
		model.Tree.Insert(p)
	}

	for range params.Blues {
		pair := uniqueRand.PairN(model.Params.Size)
		var p kdtree.Point = agent.NewBlue(pair.X, pair.Y)
		model.Tree.Insert(p)
	}

	model.Tree.Balance()
	return &model
}
