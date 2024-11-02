package model

import (
	"errors"
	"fmt"
	"main/model/agent"
	"main/model/grid"
)

type Params struct {
	Size, Blues, Reds, JBlue, JRed, MBlue, MRed int
}

func (p Params) String() string {
	return fmt.Sprintf(
		"size=%d_blues=%d_reds=%d_jblue=%d_jred=%d_mblue=%d_mred=%d",
		p.Size, p.Blues, p.Reds, p.JBlue, p.JRed, p.MBlue, p.MRed,
	)
}

type Model struct {
	params  Params
	grid    *grid.Grid[agent.Agent]
	StepNum int
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
			return nil
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
	m.StepNum += 1
	return anyoneMoved, nil
}
