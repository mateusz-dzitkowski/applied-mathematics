package grid

import (
	"fmt"
	"github.com/stretchr/testify/assert"
	"testing"
)

const (
	Size = 5
	Test = "test"
)

func makeGrid(vals map[Pos]string) *Grid[string] {
	g := New[string](Size)
	for k, v := range vals {
		g.Grid[k] = v
	}
	return g
}

func TestSet(t *testing.T) {
	g := makeGrid(make(map[Pos]string))
	p := Pos{X: 2, Y: 3}

	g.Set(p, Test)

	val, ok := g.Grid[p]
	assert.Equal(t, true, ok)
	assert.Equal(t, Test, val)
}

func TestGet(t *testing.T) {
	p := Pos{X: 2, Y: 3}
	g := makeGrid(map[Pos]string{p: Test})

	val, ok := g.Get(p)
	assert.Equal(t, true, ok)
	assert.Equal(t, Test, val)
}

func TestPos(t *testing.T) {
	var tests = []struct {
		input Pos
		check Pos
	}{
		{Pos{X: 0, Y: 0}, Pos{X: 0, Y: 0}},
		{Pos{X: 2, Y: 3}, Pos{X: 2, Y: 3}},
		{Pos{X: Size, Y: Size}, Pos{X: 0, Y: 0}},
		{Pos{X: Size + 1, Y: Size + 2}, Pos{X: 1, Y: 2}},
		{Pos{X: -2, Y: -3}, Pos{X: 3, Y: 2}},
		{Pos{X: -2 - Size, Y: -Size - Size}, Pos{X: 3, Y: 0}},
	}
	g := makeGrid(make(map[Pos]string))
	for _, tt := range tests {
		t.Run(fmt.Sprintf("%v=%v", tt.input, tt.check), func(t *testing.T) {
			assert.Equal(t, tt.check, g.translatePos(tt.input))
		})
	}
}

func TestDelete(t *testing.T) {
	p := Pos{X: 0, Y: 0}
	g := makeGrid(map[Pos]string{
		p: Test,
	})

	g.Delete(p)

	val, ok := g.Get(p)
	assert.Equal(t, false, ok)
	assert.Equal(t, "", val)
}

func TestDeleteNonExistingPosDoesNothing(t *testing.T) {
	g := makeGrid(map[Pos]string{})

	assert.Equal(t, len(g.Grid), 0)
	g.Delete(Pos{X: 0, Y: 0})
	assert.Equal(t, len(g.Grid), 0)
}

func TestClosestNeighbours(t *testing.T) {
	tests := []struct {
		setup    map[Pos]string
		p        Pos
		k        int
		expected []Pos
	}{
		{
			setup: map[Pos]string{
				Pos{X: 1, Y: 1}: Test,
				Pos{X: 1, Y: 2}: Test,
				Pos{X: 3, Y: 1}: Test,
			},
			p: Pos{X: 0, Y: 0},
			k: 1,
			expected: []Pos{{
				X: 1,
				Y: 1,
			}},
		},
		{
			setup: map[Pos]string{
				Pos{X: 1, Y: 1}: Test,
				Pos{X: 1, Y: 2}: Test,
				Pos{X: 3, Y: 1}: Test,
			},
			p: Pos{X: 0, Y: 0},
			k: 2,
			expected: []Pos{
				{
					X: 1,
					Y: 1,
				}, {
					X: 1,
					Y: 2,
				},
			},
		},
		{
			setup: map[Pos]string{
				Pos{X: 4, Y: 4}: Test,
				Pos{X: 3, Y: 4}: Test,
				Pos{X: 4, Y: 3}: Test,
			},
			p: Pos{X: 0, Y: 0},
			k: 1,
			expected: []Pos{{
				X: 4,
				Y: 4,
			}},
		},
		{
			setup: map[Pos]string{
				Pos{X: 4, Y: 4}: Test,
				Pos{X: 3, Y: 4}: Test,
				Pos{X: 3, Y: 3}: Test,
			},
			p: Pos{X: 0, Y: 0},
			k: 2,
			expected: []Pos{
				{
					X: 4,
					Y: 4,
				},
				{
					X: 3,
					Y: 4,
				},
			},
		},
		{
			setup: map[Pos]string{
				Pos{X: 2, Y: 2}: Test,
				Pos{X: 2, Y: 3}: Test,
				Pos{X: 3, Y: 3}: Test,
			},
			p: Pos{X: 0, Y: 0},
			k: 2,
			expected: []Pos{
				{
					X: 2,
					Y: 2,
				},
				{
					X: 3,
					Y: 3,
				},
			},
		},
		{
			setup: map[Pos]string{
				Pos{X: 1, Y: 2}: Test,
				Pos{X: 2, Y: 4}: Test,
				Pos{X: 3, Y: 4}: Test,
			},
			p: Pos{X: 1, Y: 1},
			k: 2,
			expected: []Pos{
				{
					X: 1,
					Y: 2,
				},
				{
					X: 2,
					Y: 4,
				},
			},
		},
	}
	for n, tt := range tests {
		t.Run(fmt.Sprintf("%d", n), func(t *testing.T) {
			g := makeGrid(tt.setup)
			assert.Equal(t, tt.expected, g.GetClosestNeighbours(tt.p, tt.k))
		})
	}
}

func TestRandomUnoccupiedPos(t *testing.T) {
	setup := make(map[Pos]string)
	for x := range 5 {
		for y := range 5 {
			setup[Pos{X: x, Y: y}] = Test
		}
	}
	g := makeGrid(setup)
	g.Delete(Pos{X: 0, Y: 0})

	assert.Equal(t, Pos{X: 0, Y: 0}, g.RandomUnoccupiedPos())
}
