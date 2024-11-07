package model

import (
	"errors"
	"fmt"
	"image/color"
	"main/model/grid"
)

type ColorParams struct {
	Population int
	M          int
	J          float64
}

type ColorParamsStore interface {
	GetColorParam(rgba color.RGBA) ColorParams
	GetAllColors() []color.RGBA
}

type Params struct {
	Size         int
	CParamsStore ColorParamsStore
}

func (p Params) String() string {
	return fmt.Sprintf("size=%d_cparams=%v", p.Size, p.CParamsStore)
}

type Model struct {
	params  Params
	Grid    *grid.Grid[color.RGBA]
	StepNum int
}

func New(params Params) *Model {
	model := Model{
		params: params,
		Grid:   grid.New[color.RGBA](params.Size),
	}

	for _, c := range params.CParamsStore.GetAllColors() {
		for range params.CParamsStore.GetColorParam(c).Population {
			model.Grid.Set(model.Grid.RandomUnoccupiedPos(), c)
		}
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

		segIndex, err := m.segIndex(pos)
		if err != nil {
			return false, err
		}

		if segIndex < m.params.CParamsStore.GetColorParam(a).J {
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

	neighbours := m.Grid.GetClosestNeighbours(p, m.params.CParamsStore.GetColorParam(a).M)
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
