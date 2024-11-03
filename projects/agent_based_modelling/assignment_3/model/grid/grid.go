package grid

import (
	"math"
	"math/rand"
)

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
	visited := make(map[Pos]struct{})
	var output []Pos

	for distSquared := range g.size * g.size {
		distSquared += 1
		for x := range int(math.Sqrt(float64(distSquared))) + 1 {
			ySquared := distSquared - x*x
			y := int(math.Sqrt(float64(ySquared)))
			if y*y != ySquared {
				continue
			}
			for _, dx := range []int{-x, x} {
				for _, dy := range []int{-y, y} {
					check := g.translatePos(p.add(Pos{X: dx, Y: dy}))
					_, wasVisited := visited[check]
					if wasVisited {
						continue
					}
					visited[check] = struct{}{}
					_, ok := g.Get(check)

					if !ok {
						continue
					}
					output = append(output, check)
					if len(output) >= k {
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
