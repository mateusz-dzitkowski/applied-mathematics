package road

import (
	"main/model/road/car"
	"math/rand"
)

type Road struct {
	length int
	Lane   []*car.Car
}

func New(length int) *Road {
	return &Road{
		length: length,
		Lane:   make([]*car.Car, length),
	}
}

func (r *Road) IsOccupied(n int) bool {
	return r.Lane[n%r.length] != nil
}

func (r *Road) RandomUnoccupiedSpace() int {
	for {
		n := rand.Intn(r.length)
		if !r.IsOccupied(n) {
			return n
		}
	}
}
