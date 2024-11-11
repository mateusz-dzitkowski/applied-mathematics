package batch

import (
	"fmt"
	"gonum.org/v1/plot"
	"gonum.org/v1/plot/plotter"
	"gonum.org/v1/plot/plotutil"
	"gonum.org/v1/plot/vg"
	"image/color"
	"main/model"
	"sync"
)

const (
	BaseSize     = 100
	BaseJ        = 0.5
	BaseMaxSteps = 200
	BaseRuns     = 100
)

var (
	ColorRed  = color.RGBA{R: 255, A: 255}
	ColorBlue = color.RGBA{B: 255, A: 255}
)

type CParams struct {
	Blues, Reds, MBlue, MRed int
	JBlue, JRed              float64
}

func (p CParams) GetAllColors() []color.RGBA {
	return []color.RGBA{ColorRed, ColorBlue}
}

func (p CParams) GetColorParam(rgba color.RGBA) model.ColorParams {
	if rgba == ColorRed {
		return model.ColorParams{
			Population: p.Reds,
			M:          p.MRed,
			J:          p.JRed,
		}
	} else {
		return model.ColorParams{
			Population: p.Blues,
			M:          p.MBlue,
			J:          p.JBlue,
		}
	}
}

func PlotNumOfIterationsPerPopulationSize() {
	p := plot.New()
	p.Title.Text = fmt.Sprintf("Number of iteration as a function of population size, averaged over %d runs", BaseRuns)
	p.X.Label.Text = "Population size"
	p.Y.Label.Text = "Number of iterations"

	if err := plotutil.AddScatters(
		p,
		"M=1", numOfIterationsPerPopulationSize(1, 0.5),
		"M=2", numOfIterationsPerPopulationSize(2, 0.5),
		"M=3", numOfIterationsPerPopulationSize(3, 0.5),
	); err != nil {
		panic(err)
	}

	if err := p.Save(10*vg.Inch, 10*vg.Inch, "iteration_per_pop_size.png"); err != nil {
		panic(err)
	}
}

func numOfIterationsPerPopulationSize(mVal int, jVal float64) plotter.XYs {
	popMin := 50
	popMax := 4950
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
			Size: BaseSize,
			CParamsStore: CParams{
				Blues: pop,
				Reds:  pop,
				MBlue: mVal,
				MRed:  mVal,
				JBlue: jVal,
				JRed:  jVal,
			},
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
		"N=1000", segIndexPerM(BaseJ, 1000),
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
	maxM := 10
	mu := sync.Mutex{}
	amount := maxM + 1 - minM
	xys := make(plotter.XYs, amount)
	todo := amount * BaseRuns
	functions := make([]func(), amount*BaseRuns)
	for i := range amount {
		currentM := minM + i
		xys[i].X = float64(currentM)
		params := model.Params{
			Size: BaseSize,
			CParamsStore: CParams{
				Blues: popVal,
				Reds:  popVal,
				MBlue: currentM,
				MRed:  currentM,
				JBlue: jVal,
				JRed:  jVal,
			},
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

func PlotSegIndexPerJ() {
	p := plot.New()
	p.Title.Text = fmt.Sprintf("Segregation index as a function of J, averaged over %d runs", BaseRuns)
	p.X.Label.Text = "J"
	p.Y.Label.Text = "Segregation index"
	p.Legend.Top = true
	p.Y.Max = 1

	if err := plotutil.AddScatters(
		p,
		"N=1000", segIndexPerJ(1, 1000),
		"N=4000", segIndexPerJ(1, 4000),
	); err != nil {
		panic(err)
	}

	if err := p.Save(10*vg.Inch, 10*vg.Inch, "seg_index_per_j.png"); err != nil {
		panic(err)
	}
}

func segIndexPerJ(mVal, popVal int) plotter.XYs {
	minJ := 0.1
	maxJ := 0.91
	step := 0.01
	mu := sync.Mutex{}
	amount := int((maxJ - minJ) / step)
	xys := make(plotter.XYs, amount)
	todo := amount * BaseRuns
	functions := make([]func(), amount*BaseRuns)
	for i := range amount {
		xys[i].X = minJ + float64(i)*(maxJ-minJ)/float64(amount)
		params := model.Params{
			Size: BaseSize,
			CParamsStore: CParams{
				Blues: popVal,
				Reds:  popVal,
				MBlue: mVal,
				MRed:  mVal,
				JBlue: xys[i].X,
				JRed:  xys[i].X,
			},
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
