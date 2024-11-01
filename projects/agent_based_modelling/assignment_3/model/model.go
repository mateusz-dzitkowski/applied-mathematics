package model

import (
	"errors"
	"main/model/agent"
	"main/model/grid"
)

type Params struct {
	Size, Blues, Reds, JBlue, JRed, MBlue, MRed int
}

type Model struct {
	params Params
	grid   *grid.Grid[agent.Agent]
}

func New(params Params) *Model {
	model := Model{
		params: params,
		grid:   grid.New[agent.Agent](params.Size),
	}

	for range params.Blues {
		model.grid.Set(model.grid.RandomUnoccupiedPos(), agent.Blue())
	}

	for range params.Reds {
		model.grid.Set(model.grid.RandomUnoccupiedPos(), agent.Red())
	}

	return &model
}

func (m *Model) step() (bool, error) {
	anyoneMoved := false
	for _, pos := range m.grid.OccupiedPositions() {
		a, ok := m.grid.Get(pos)
		if !ok {
			return false, errors.New("cant find the agent")
		}
		var sameNeighbours int
		var mColor int
		var jColor int

		switch a {
		case agent.ColorBlue:
			mColor = m.params.MBlue
			jColor = m.params.JBlue
		case agent.ColorRed:
			mColor = m.params.MRed
			jColor = m.params.JRed
		}

		neighbours := m.grid.GetClosestNeighbours(pos, mColor)
		for _, neighbourPos := range neighbours {
			neighbour, ok := m.grid.Get(neighbourPos)
			if !ok {
				return false, errors.New("cant find the agent")
			}
			if neighbour == a {
				sameNeighbours += 1
			}
		}

		if sameNeighbours < jColor {
			m.grid.Set(m.grid.RandomUnoccupiedPos(), a)
			m.grid.Delete(pos)
			anyoneMoved = true
		}
	}
	return anyoneMoved, nil
}
