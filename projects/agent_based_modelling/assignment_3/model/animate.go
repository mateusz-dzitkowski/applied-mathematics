package model

import (
	"fmt"
	"image"
	"image/color"
	"image/gif"
	"os"
)

type AnimateParams struct {
	CellSize,
	Delay,
	MaxSteps,
	SecondsWithFinalState int
}

func (m *Model) Animate(params AnimateParams) error {
	var err error
	var frames []*image.Paletted
	var delays []int

	for n := range params.MaxSteps {
		if n%10 == 0 {
			fmt.Println(n)
		}
		frame := m.renderFrame(params.CellSize)
		frames = append(frames, frame)
		delays = append(delays, params.Delay)
		anyoneMoved, err := m.step()
		if err != nil {
			return err
		}
		if !anyoneMoved {
			break
		}
	}

	finalFrame := m.renderFrame(params.CellSize)
	frames = append(frames, finalFrame)
	delays = append(delays, 100*params.SecondsWithFinalState)

	fileName := fmt.Sprintf("%s.gif", m.params)
	f, err := os.Create(fileName)
	if err != nil {
		return err
	}
	defer f.Close()

	err = gif.EncodeAll(
		f,
		&gif.GIF{
			Image: frames,
			Delay: delays,
		},
	)
	if err != nil {
		err = os.Remove(fileName)
		if err != nil {
			return err
		}
		return err
	}
	return nil
}

func (m *Model) renderFrame(cellSize int) *image.Paletted {
	palette := color.Palette{color.White}
	for _, c := range m.params.CParamsStore.GetAllColors() {
		palette = append(palette, c)
	}

	img := image.NewPaletted(image.Rect(0, 0, m.params.Size*cellSize, m.params.Size*cellSize), palette)

	for pos, c := range m.Grid.Grid {
		startX := pos.X * cellSize
		startY := pos.Y * cellSize

		for x := 0; x < cellSize; x++ {
			for y := 0; y < cellSize; y++ {
				img.Set(startX+x, startY+y, c)
			}
		}
	}

	return img
}
