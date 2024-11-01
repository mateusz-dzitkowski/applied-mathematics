package grid

import "math/rand"

type Pos struct{ X, Y int }

func (p Pos) add(other Pos) Pos {
	return Pos{
		X: p.X + other.X,
		Y: p.Y + other.Y,
	}
}

func (p Pos) times(a int) Pos {
	return Pos{
		X: p.X * a,
		Y: p.Y * a,
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
	// naive as hell but oh well, it gets the job done
	var output []Pos
	for layer := range g.size / 2 {
		layer += 1
		for a := range layer + 1 {
			for _, d := range []struct {
				outward Pos
				side    Pos
			}{
				{Pos{X: 1, Y: 0}, Pos{X: 0, Y: 1}},
				{Pos{X: 0, Y: 1}, Pos{X: 1, Y: 0}},
				{Pos{X: -1, Y: 0}, Pos{X: 0, Y: 1}},
				{Pos{X: 0, Y: -1}, Pos{X: 1, Y: 0}},
			} {
				for _, sign := range []int{-1, 1} {
					check := p.add(d.outward.times(layer)).add(d.side.times(a).times(sign)) // p + layer*outward +- a*side
					if a == layer && (d.side == Pos{X: 0, Y: 1}) || a == 0 && sign == -1 {
						continue // don't check the corners twice, don't check the vertical/horizontal twice
					}
					_, ok := g.Get(check)
					if ok {
						output = append(output, g.translatePos(check))
					}
					if len(output) == k {
						return output
					}
				}
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
