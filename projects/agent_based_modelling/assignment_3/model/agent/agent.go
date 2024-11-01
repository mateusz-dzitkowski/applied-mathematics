package agent

import "image/color"

var (
	ColorRed  = color.RGBA{R: 255, A: 255}
	ColorBlue = color.RGBA{B: 255, A: 255}
)

type Agent = color.RGBA

func Red() Agent {
	return ColorRed
}

func Blue() Agent {
	return ColorBlue
}
