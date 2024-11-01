package model

import (
	"errors"
	"main/model/agent"
)

func (m *Model) SegIndex() (float64, error) {
	output := 0.0

	var mColor int
	for pos, a := range m.grid.Grid {
		if a == agent.ColorBlue {
			mColor = m.params.MBlue
		} else {
			mColor = m.params.MRed
		}
		neighbours := m.grid.GetClosestNeighbours(pos, mColor)
		sameNeighboursFraction := 0.0

		for _, nPos := range neighbours {

			val, ok := m.grid.Get(nPos)
			if !ok {
				return 0, errors.New("cant find the agent")
			}
			if val == a {
				sameNeighboursFraction += 1 / float64(len(neighbours))
			}
		}
		output += sameNeighboursFraction / float64(len(m.grid.Grid))
	}

	return output, nil
}
