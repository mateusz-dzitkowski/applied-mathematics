package batch

import (
	"fmt"
	"gonum.org/v1/plot"
	"gonum.org/v1/plot/plotter"
	"gonum.org/v1/plot/plotutil"
	"gonum.org/v1/plot/vg"
	"main/model"
	"sync"
)

const (
	MaxVelocity = 5
	Steps       = 20
	RoadLength  = 1000
	NumPoints   = 1000
	Runs        = 100
)

func PlotMeanVelocities() {
	p := plot.New()
	p.Title.Text = fmt.Sprintf("Mean velocity as a function of the density of cars, over %d runs", Runs)
	p.X.Label.Text = "Car density"
	p.Y.Label.Text = "Mean velocity"
	p.Legend.Top = true

	if err := plotutil.AddScatters(
		p,
		"p=0.0", getMeanVelocities(0.0),
		"p=0.2", getMeanVelocities(0.2),
		"p=0.4", getMeanVelocities(0.4),
		"p=0.6", getMeanVelocities(0.6),
		"p=0.8", getMeanVelocities(0.8),
	); err != nil {
		panic(err)
	}

	if err := p.Save(10*vg.Inch, 10*vg.Inch, "mean_velocity.png"); err != nil {
		panic(err)
	}
}

func getMeanVelocities(decelerateProbability float64) plotter.XYs {
	xys := make(plotter.XYs, NumPoints)
	functions := make([]func(), NumPoints)
	for i := range NumPoints {
		carDensity := float64(i+1) / float64(NumPoints)
		xys[i].X = carDensity
		functions[i] = func() {
			xys[i].Y = meanVelocityOverNRuns(Runs, carDensity, decelerateProbability)
		}
	}
	parallelize(functions)
	return xys
}

func meanVelocityOverNRuns(n int, carDensity, decelerateProbability float64) float64 {
	var output float64
	mu := sync.Mutex{}

	functions := make([]func(), n)
	for i := range n {
		functions[i] = func() {
			m := model.New(model.Params{
				MaxVelocity:           MaxVelocity,
				RoadLength:            RoadLength,
				CarDensity:            carDensity,
				DecelerateProbability: decelerateProbability,
			})
			for range Steps {
				m.Step()
			}

			mu.Lock()
			output += m.MeanVelocity() / float64(n)
			mu.Unlock()
		}
	}

	parallelize(functions)

	return output
}

func parallelize(functions []func()) {
	var wg sync.WaitGroup
	wg.Add(len(functions))

	defer wg.Wait()

	for _, function := range functions {
		go func(f func()) {
			defer wg.Done()
			f()
		}(function)
	}
}
