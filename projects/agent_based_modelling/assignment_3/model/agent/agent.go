package agent

import "github.com/fatih/color"

var (
	ColorRed  = color.New(color.FgRed).SprintFunc()("█")
	ColorBlue = color.New(color.FgBlue).SprintFunc()("█")
)

type Agent = string

func Red() Agent {
	return ColorRed
}

func Blue() Agent {
	return ColorBlue
}
