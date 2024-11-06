package model

import (
	"errors"
	"fmt"
	"main/model/agent"
	"main/model/grid"
)

type Params struct {
	Size, Blues, Reds, MBlue, MRed int
	JRed, JBlue                    float64
}

func (p Params) String() string {
	return fmt.Sprintf(
		"size=%d_blues=%d_reds=%d_jblue=%f_jred=%f_mblue=%d_mred=%d",
		p.Size, p.Blues, p.Reds, p.JBlue, p.JRed, p.MBlue, p.MRed,
	)
}

type Model struct {
	params  Params
	Grid    *grid.Grid[agent.Agent]
	StepNum int
}

func New(params Params) *Model {
	model := Model{
		params: params,
		Grid:   grid.New[agent.Agent](params.Size),
	}

	for range params.Blues {
		model.Grid.Set(model.Grid.RandomUnoccupiedPos(), agent.Blue())
	}

	for range params.Reds {
		model.Grid.Set(model.Grid.RandomUnoccupiedPos(), agent.Red())
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

func (m *Model) MeanSegIndex() (float64, error) {
	meanSegIndex := 0.0

	agentsPos := m.Grid.OccupiedPositions()
	for _, pos := range agentsPos {
		segIndex, err := m.segIndex(pos)
		if err != nil {
			return 0, err
		}
		meanSegIndex += segIndex / float64(len(agentsPos))
	}

	return meanSegIndex, nil
}

func (m *Model) step() (bool, error) {
	anyoneMoved := false
	for _, pos := range m.Grid.OccupiedPositions() {
		a, ok := m.Grid.Get(pos)
		if !ok {
			return false, errors.New("cant find the agent")
		}

		var jColor float64
		switch a {
		case agent.ColorBlue:
			jColor = m.params.JBlue
		case agent.ColorRed:
			jColor = m.params.JRed
		}

		segIndex, err := m.segIndex(pos)
		if err != nil {
			return false, err
		}

		if segIndex < jColor {
			m.Grid.Set(m.Grid.RandomUnoccupiedPos(), a)
			m.Grid.Delete(pos)
			anyoneMoved = true
		}
	}
	m.StepNum += 1
	return anyoneMoved, nil
}

func (m *Model) segIndex(p grid.Pos) (float64, error) {
	a, ok := m.Grid.Get(p)
	if !ok {
		return 0, errors.New("cant find the agent")
	}

	var mColor int
	if a == agent.ColorBlue {
		mColor = m.params.MBlue
	} else {
		mColor = m.params.MRed
	}

	neighbours := m.Grid.GetClosestNeighbours(p, mColor)
	if len(neighbours) == 0 {
		return 0, nil
	}

	sameNeighbours := 0
	for _, nPos := range neighbours {
		val, ok := m.Grid.Get(nPos)
		if !ok {
			return 0, errors.New("cant find the agent")
		}
		if val == a {
			sameNeighbours += 1
		}
	}

	return float64(sameNeighbours) / float64(len(neighbours)), nil
}
