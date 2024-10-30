package unique_rand

import "math/rand"

type Pair struct{ X, Y float64 }

type UniqueRand struct {
	generated map[Pair]bool
}

func New() UniqueRand {
	return UniqueRand{generated: make(map[Pair]bool)}
}

func (u *UniqueRand) PairN(n int) Pair {
	for {
		p := Pair{
			X: float64(rand.Intn(n)),
			Y: float64(rand.Intn(n)),
		}
		if !u.generated[p] {
			u.generated[p] = true
			return p
		}
	}
}
