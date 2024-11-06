package grid

import (
	"math/rand"
)

type Pos struct{ X, Y int }

func (p Pos) add(other Pos) Pos {
	return Pos{
		X: p.X + other.X,
		Y: p.Y + other.Y,
	}
}

type Grid[T any] struct {
	size int
	Grid map[Pos]T
}

func New[T any](size int) *Grid[T] {
	return &Grid[T]{
		size: size,
		Grid: make(map[Pos]T),
	}
}

func (g *Grid[T]) Get(p Pos) (T, bool) {
	val, ok := g.Grid[g.translatePos(p)]
	return val, ok
}

func (g *Grid[T]) Set(p Pos, val T) {
	g.Grid[g.translatePos(p)] = val
}

func (g *Grid[T]) Delete(p Pos) {
	delete(g.Grid, p)
}

func (g *Grid[T]) GetClosestNeighbours(p Pos, k int) []Pos {
	var output []Pos
	for x := range 2*k + 1 {
		for y := range 2*k + 1 {
			check := p.add(Pos{X: -k + x, Y: -k + y})
			if check == p {
				continue
			}
			_, ok := g.Get(check)
			if ok {
				output = append(output, g.translatePos(check))
			}
		}
	}
	return output
}

func (g *Grid[T]) RandomUnoccupiedPos() Pos {
	for {
		p := Pos{
			X: rand.Intn(g.size),
			Y: rand.Intn(g.size),
		}
		_, occupied := g.Get(p)
		if !occupied {
			return p
		}
	}
}

func (g *Grid[T]) OccupiedPositions() []Pos {
	positions := make([]Pos, 0, len(g.Grid))
	for gridPos := range g.Grid {
		positions = append(positions, gridPos)
	}
	return positions
}

func (g *Grid[T]) translatePos(p Pos) Pos {
	xResult := p.X % g.size
	if xResult < 0 {
		xResult += g.size
	}
	yResult := p.Y % g.size
	if yResult < 0 {
		yResult += g.size
	}
	return Pos{
		X: xResult,
		Y: yResult,
	}
}
