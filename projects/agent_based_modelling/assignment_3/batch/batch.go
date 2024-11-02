package batch

import (
	"fmt"
	"gonum.org/v1/plot"
	"gonum.org/v1/plot/plotter"
	"gonum.org/v1/plot/vg"
	"main/model"
	"sync"
)

const (
	BasePop      = 250
	BaseSize     = 100
	BaseM        = 8
	BaseJ        = 4
	BaseMaxSteps = 1000
)

func NumOfIterationsPerPopulationSize(popMin, popMax, runs int) {
	mu := sync.Mutex{}
	amount := popMax + 1 - popMin
	xys := make(plotter.XYs, amount)
	functions := make([]func(), amount*runs)
	for i := range amount {
		pop := popMin + i
		xys[i].X = float64(pop)
		params := model.Params{
			Size:  BaseSize,
			Blues: pop,
			Reds:  pop,
			JBlue: BaseJ,
			JRed:  BaseJ,
			MBlue: BaseM,
			MRed:  BaseM,
		}
		for j := range runs {
			functions[runs*i+j] = func() {
				m := model.New(params)
				err := m.Run(BaseMaxSteps)
				if err != nil {
					panic(err)
				}
				mu.Lock()
				xys[i].Y += float64(m.StepNum) / float64(runs)
				mu.Unlock()
			}
		}
	}

	parallelize(functions)

	p := plot.New()
	p.Title.Text = fmt.Sprintf("Number of iterations wrt population size, with, j=0.5, m=8, averaged over %d runs", runs)
	p.X.Label.Text = "Population size"
	p.Y.Label.Text = "Number of iterations"

	scatter, err := plotter.NewScatter(xys)
	if err != nil {
		panic(err)
	}
	p.Add(scatter)
	if err = p.Save(10*vg.Inch, 10*vg.Inch, "iterations_per_population_size.png"); err != nil {
		panic(err)
	}
}

func SegIndexPerM(minM, maxM, runs int) {
	mu := sync.Mutex{}
	amount := maxM + 1 - minM
	xys := make(plotter.XYs, amount)
	functions := make([]func(), amount*runs)
	for i := range amount {
		currentM := minM + i
		xys[i].X = float64(currentM)
		params := model.Params{
			Size:  BaseSize,
			Blues: BasePop,
			Reds:  BasePop,
			JBlue: currentM / 2,
			JRed:  currentM / 2,
			MBlue: currentM,
			MRed:  currentM,
		}
		for j := range runs {
			functions[runs*i+j] = func() {
				m := model.New(params)
				err := m.Run(BaseMaxSteps)
				if err != nil {
					panic(err)
				}
				segIndex, err := m.SegIndex()
				if err != nil {
					panic(err)
				}
				mu.Lock()
				xys[i].Y += segIndex / float64(runs)
				mu.Unlock()
			}
		}
	}

	parallelize(functions)

	p := plot.New()
	p.Title.Text = fmt.Sprintf("Segregation index wrt m, with j=0.5, averaged over %d runs", runs)
	p.X.Label.Text = "m"
	p.Y.Label.Text = "Segregation index"

	scatter, err := plotter.NewScatter(xys)
	if err != nil {
		panic(err)
	}
	p.Add(scatter)
	if err = p.Save(10*vg.Inch, 10*vg.Inch, "seg_index_per_m.png"); err != nil {
		panic(err)
	}
}

func SegIndexPerJFrac(minJFrac, maxJFrac float64, paramM, runs int) {
	mu := sync.Mutex{}
	minJ := int(float64(paramM) * minJFrac)
	maxJ := int(float64(paramM) * maxJFrac)
	amount := maxJ + 1 - minJ
	xys := make(plotter.XYs, amount)
	functions := make([]func(), amount*runs)
	for i := range amount {
		xys[i].X = minJFrac + float64(i)*(maxJFrac-minJFrac)/float64(amount)
		params := model.Params{
			Size:  BaseSize,
			Blues: BasePop,
			Reds:  BasePop,
			JBlue: minJ + i,
			JRed:  minJ + i,
			MBlue: paramM,
			MRed:  paramM,
		}
		for j := range runs {
			functions[runs*i+j] = func() {
				m := model.New(params)
				err := m.Run(BaseMaxSteps)
				if err != nil {
					panic(err)
				}
				segIndex, err := m.SegIndex()
				if err != nil {
					panic(err)
				}
				mu.Lock()
				xys[i].Y += segIndex / float64(runs)
				mu.Unlock()
			}
		}
	}

	parallelize(functions)

	p := plot.New()
	p.Title.Text = fmt.Sprintf("Segregation index wrt j, with m=%d, averaged over %d runs", paramM, runs)
	p.X.Label.Text = "j"
	p.Y.Label.Text = "Segregation index"

	scatter, err := plotter.NewScatter(xys)
	if err != nil {
		panic(err)
	}
	p.Add(scatter)
	if err = p.Save(10*vg.Inch, 10*vg.Inch, "seg_index_per_j.png"); err != nil {
		panic(err)
	}
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
