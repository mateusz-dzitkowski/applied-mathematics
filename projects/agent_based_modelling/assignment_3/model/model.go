package model

import (
	"bytes"
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

func (m *Model) Run(maxSteps int) error {
	for range maxSteps {
		anyoneMoved, err := m.step()
		if err != nil {
			return err
		}
		if !anyoneMoved {
			anyoneMoved, err = m.step() // check once more if no one truly wants to move
			if err != nil {
				return err
			}
			if !anyoneMoved {
				return nil
			}
		}
	}
	return nil
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

func (m *Model) String() string {
	var sb bytes.Buffer
	for x := range m.params.Size {
		for y := range m.params.Size {
			p := grid.Pos{X: x, Y: y}
			a, ok := m.grid.Get(p)
			if ok {
				sb.WriteString(a)
			} else {
				sb.WriteString(" ")
			}
		}
		sb.WriteString("\n")
	}
	return sb.String()
}
