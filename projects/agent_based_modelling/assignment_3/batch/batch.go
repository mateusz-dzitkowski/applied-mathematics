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
	BaseSize     = 100
	BaseJ        = 0.5
	BaseMaxSteps = 100
	BaseRuns     = 10
)

func PlotNumOfIterationsPerPopulationSize() {
	p := plot.New()
	p.Title.Text = fmt.Sprintf("Number of iteration as a function of population size, averaged over %d runs", BaseRuns)
	p.X.Label.Text = "Population size"
	p.Y.Label.Text = "Number of iterations"

	if err := plotutil.AddScatters(
		p,
		"M=1", numOfIterationsPerPopulationSize(1),
		"M=2", numOfIterationsPerPopulationSize(2),
		"M=3", numOfIterationsPerPopulationSize(3),
	); err != nil {
		panic(err)
	}

	if err := p.Save(10*vg.Inch, 10*vg.Inch, "iteration_per_pop_size.png"); err != nil {
		panic(err)
	}
}

func numOfIterationsPerPopulationSize(mVal int) plotter.XYs {
	popMin := 250
	popMax := 4750
	step := 10

	mu := sync.Mutex{}
	amount := (popMax - popMin) / step
	todo := amount * BaseRuns
	xys := make(plotter.XYs, amount)
	functions := make([]func(), amount*BaseRuns)
	for i := range amount {
		pop := popMin + i*step
		xys[i].X = float64(pop)
		params := model.Params{
			Size:  BaseSize,
			Blues: pop,
			Reds:  pop,
			JBlue: BaseJ,
			JRed:  BaseJ,
			MBlue: mVal,
			MRed:  mVal,
		}
		for j := range BaseRuns {
			functions[BaseRuns*i+j] = func() {
				m := model.New(params)
				err := m.Run(BaseMaxSteps)
				if err != nil {
					panic(err)
				}
				mu.Lock()
				xys[i].Y += float64(m.StepNum) / float64(BaseRuns)
				todo -= 1
				if todo%10 == 0 {
					fmt.Println(todo)
				}
				mu.Unlock()
			}
		}
	}

	parallelize(functions)

	return xys
}

func PlotSegIndexPerM() {
	p := plot.New()
	p.Title.Text = fmt.Sprintf("Segregation index as a function of M, averaged over %d runs", BaseRuns)
	p.X.Label.Text = "M"
	p.Y.Label.Text = "Segregation index"
	p.Legend.Top = true
	p.Y.Max = 1

	if err := plotutil.AddScatters(
		p,
		"N=250", segIndexPerM(BaseJ, 250),
		"N=1500", segIndexPerM(BaseJ, 1500),
		"N=2500", segIndexPerM(BaseJ, 2500),
		"N=4000", segIndexPerM(BaseJ, 4000),
	); err != nil {
		panic(err)
	}

	if err := p.Save(10*vg.Inch, 10*vg.Inch, "seg_index_per_m.png"); err != nil {
		panic(err)
	}
}

func segIndexPerM(jVal float64, popVal int) plotter.XYs {
	minM := 1
	maxM := 6
	mu := sync.Mutex{}
	amount := maxM + 1 - minM
	xys := make(plotter.XYs, amount)
	functions := make([]func(), amount*BaseRuns)
	for i := range amount {
		currentM := minM + i
		xys[i].X = float64(currentM)
		params := model.Params{
			Size:  BaseSize,
			Blues: popVal,
			Reds:  popVal,
			JBlue: jVal,
			JRed:  jVal,
			MBlue: currentM,
			MRed:  currentM,
		}
		for j := range BaseRuns {
			functions[BaseRuns*i+j] = func() {
				m := model.New(params)
				err := m.Run(BaseMaxSteps)
				if err != nil {
					panic(err)
				}

				meanSegIndex, err := m.MeanSegIndex()
				if err != nil {
					panic(err)
				}

				mu.Lock()
				xys[i].Y += meanSegIndex / float64(BaseRuns)
				mu.Unlock()
			}
		}
	}

	parallelize(functions)

	return xys
}

func PlotSegIndexPerJ() {
	p := plot.New()
	p.Title.Text = fmt.Sprintf("Segregation index as a function of J, averaged over %d runs", BaseRuns)
	p.X.Label.Text = "J"
	p.Y.Label.Text = "Segregation index"
	p.Y.Max = 1

	if err := plotutil.AddScatters(
		p,
		"M=1, N=250", segIndexPerJ(1, 250),
		"M=1, N=2500", segIndexPerJ(1, 2500),
		"M=1, N=4000", segIndexPerJ(1, 4000),
		"M=3, N=250", segIndexPerJ(3, 250),
		"M=3, N=2500", segIndexPerJ(3, 2500),
		"M=3, N=4000", segIndexPerJ(3, 4000),
	); err != nil {
		panic(err)
	}

	if err := p.Save(10*vg.Inch, 10*vg.Inch, "seg_index_per_j.png"); err != nil {
		panic(err)
	}
}

func segIndexPerJ(mVal, popVal int) plotter.XYs {
	minJ := 0.1
	maxJ := 0.9
	step := 0.01
	mu := sync.Mutex{}
	amount := int((maxJ - minJ) / step)
	xys := make(plotter.XYs, amount)
	functions := make([]func(), amount*BaseRuns)
	for i := range amount {
		xys[i].X = minJ + float64(i)*(maxJ-minJ)/float64(amount)
		params := model.Params{
			Size:  BaseSize,
			Blues: popVal,
			Reds:  popVal,
			JBlue: xys[i].X,
			JRed:  xys[i].X,
			MBlue: mVal,
			MRed:  mVal,
		}
		for j := range BaseRuns {
			functions[BaseRuns*i+j] = func() {
				m := model.New(params)
				err := m.Run(BaseMaxSteps)
				if err != nil {
					panic(err)
				}

				meanSegIndex, err := m.MeanSegIndex()
				if err != nil {
					panic(err)
				}

				mu.Lock()
				xys[i].Y += meanSegIndex / float64(BaseRuns)
				mu.Unlock()
			}
		}
	}

	parallelize(functions)

	return xys
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
