package plot

import (
	"fmt"
	"gonum.org/v1/plot"
	"gonum.org/v1/plot/vg"
	"gonum.org/v1/plot/vg/draw"
	"gonum.org/v1/plot/vg/vgimg"
	"main/model"
	"os"
)

const (
	TileX    = 500
	TileY    = 500
	PaddingX = 10
	PaddingY = 10
)

func GridSave(paramsGrid [][]model.Params, filename string) error {
	plots := make([][]*plot.Plot, len(paramsGrid))

	for i, row := range paramsGrid {
		for _, params := range row {
			m := model.New(params)
			heatMap := m.ToHeatMap(params.RoadLength)

			p := plot.New()
			p.Title.Text = fmt.Sprintf("density=%.1f, probability=%.1f", params.CarDensity, params.DecelerateProbability)
			p.Add(heatMap)
			p.HideAxes()

			plots[i] = append(plots[i], p)
		}
	}

	img := vgimg.New(vg.Length(TileX*len(paramsGrid[0])), vg.Length(TileY*len(paramsGrid)))
	canvases := plot.Align(
		plots,
		draw.Tiles{
			Rows: len(paramsGrid),
			Cols: len(paramsGrid[0]),
			PadX: PaddingX,
			PadY: PaddingY,
		},
		draw.New(img),
	)

	for i := range plots {
		for j := range plots[i] {
			plots[i][j].Draw(canvases[i][j])
		}
	}

	w, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer w.Close()

	png := vgimg.PngCanvas{Canvas: img}
	_, err = png.WriteTo(w)
	return err
}
