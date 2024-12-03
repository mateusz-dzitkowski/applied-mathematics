package model

import (
	"fmt"
	"main/model/road"
	"main/model/road/car"
	"math/rand"
	"strings"
)

type Params struct {
	MaxVelocity           int
	RoadLength            int
	CarDensity            float64
	DecelerateProbability float64
}

type Model struct {
	params Params
	Road   *road.Road
}

func New(params Params) *Model {
	model := Model{
		params: params,
		Road:   road.New(params.RoadLength),
	}

	numCars := int(float64(params.RoadLength) * params.CarDensity)

	for range numCars {
		n := model.Road.RandomUnoccupiedSpace()
		model.Road.Lane[n] = car.New(params.MaxVelocity)
	}

	return &model
}

func (m *Model) Run(steps int) {
	fmt.Println(m)
	for range steps {
		m.Step()
		fmt.Println(m)
	}
}

func (m *Model) Step() {
	nextLane := make([]*car.Car, m.params.RoadLength)
	for i, c := range m.Road.Lane {
		if c == nil {
			continue
		}

		c.Accelerate()
		c.Velocity = m.getMaxPossibleSteps(i, c.Velocity)
		if rand.Float64() < m.params.DecelerateProbability {
			c.Decelerate()
		}

		nextLane[(i+c.Velocity)%m.params.RoadLength] = c
	}
	m.Road.Lane = nextLane
}

func (m *Model) getMaxPossibleSteps(i int, velocity int) int {
	for j := range velocity {
		if m.Road.IsOccupied(i + j + 1) {
			return j
		}
	}
	return velocity
}

func (m *Model) String() string {
	sb := strings.Builder{}
	sb.WriteString("[")
	for n := range m.params.RoadLength {
		if m.Road.IsOccupied(n) {
			sb.WriteString("C")
		} else {
			sb.WriteString(" ")
		}
	}
	sb.WriteString("]")
	return sb.String()
}
