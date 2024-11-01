package batch

import (
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
	scatter, err := plotter.NewScatter(xys)
	if err != nil {
		panic(err)
	}
	p.Add(scatter)
	if err = p.Save(10*vg.Inch, 10*vg.Inch, "seg_index_per_m.png"); err != nil {
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
