package agent

const (
	ColourRed  = Colour("red")
	ColourBlue = Colour("blue")
)

type Colour string

type Agent struct {
	X, Y   float64
	Colour Colour
}

func NewRed(x, y float64) Agent {
	return Agent{
		X:      x,
		Y:      y,
		Colour: ColourRed,
	}
}

func NewBlue(x, y float64) Agent {
	return Agent{
		X:      x,
		Y:      y,
		Colour: ColourBlue,
	}
}

func (a Agent) Dimensions() int {
	return 2
}

func (a Agent) Dimension(i int) float64 {
	if i == 0 {
		return a.X
	}
	return a.Y
}
