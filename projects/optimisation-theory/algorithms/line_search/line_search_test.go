package line_search

import (
	"fmt"
	"math"
	"reflect"
	"runtime"
	"testing"
)

type LineSearchOptimiser = func(Params) (float64, error)

var optimisers = []LineSearchOptimiser{
	GoldenSection,
	QuadraticInterpolation,
}

var testCases = []struct {
	fStr     string
	f        func(float64) float64
	a        float64
	b        float64
	expected float64
}{
	{
		fStr:     "f(x)=(x-1)^2",
		f:        func(x float64) float64 { return math.Pow(x-1, 2) },
		a:        -10,
		b:        10,
		expected: 1,
	},
	{
		fStr:     "f(x)=x^3-3x^2+2x",
		f:        func(x float64) float64 { return math.Pow(x, 3) - 3*math.Pow(x, 2) + 2*x },
		a:        -1,
		b:        3,
		expected: 1 + 1/math.Sqrt(3),
	},
	{
		fStr:     "f(x)=sin(x)",
		f:        func(x float64) float64 { return math.Sin(x) },
		a:        0,
		b:        2 * math.Pi,
		expected: 1.5 * math.Pi,
	},
	{
		fStr:     "f(x)=e^x",
		f:        func(x float64) float64 { return math.Exp(x) },
		a:        -5,
		b:        5,
		expected: -5,
	},
	{
		fStr:     "f(x)=2x+5",
		f:        func(x float64) float64 { return 2*x + 5 },
		a:        -10,
		b:        10,
		expected: -10,
	},
	{
		fStr:     "f(x)=(x-2)^2+3",
		f:        func(x float64) float64 { return math.Pow(x-2, 2) + 3 },
		a:        -5,
		b:        5,
		expected: 2,
	},
	{
		fStr:     "f(x)=-cos(x)",
		f:        func(x float64) float64 { return -math.Cos(x) },
		a:        -1,
		b:        math.Pi / 2,
		expected: 0,
	},
	{
		fStr:     "f(x)=x^4-4x^3+6x^2",
		f:        func(x float64) float64 { return math.Pow(x, 4) - 4*math.Pow(x, 3) + 6*math.Pow(x, 2) },
		a:        -1,
		b:        3,
		expected: 0,
	},
	{
		fStr:     "f(x)=|x|",
		f:        func(x float64) float64 { return math.Abs(x) },
		a:        -5,
		b:        5,
		expected: 0,
	},
	{
		fStr:     "f(x)=1/x",
		f:        func(x float64) float64 { return 1 / x },
		a:        1,
		b:        10,
		expected: 10,
	},
	{
		fStr:     "f(x)=ln(x)",
		f:        func(x float64) float64 { return math.Log(x) },
		a:        1,
		b:        10,
		expected: 1,
	},
	{
		fStr:     "f(x)=x^2+4x-3",
		f:        func(x float64) float64 { return math.Pow(x, 2) + 4*x - 3 },
		a:        -4,
		b:        -1.5,
		expected: -2,
	},
	{
		fStr:     "f(x)=-e^(-x^2)",
		f:        func(x float64) float64 { return -math.Exp(-math.Pow(x, 2)) },
		a:        -3,
		b:        1,
		expected: 0,
	},
	{
		fStr:     "f(x)=(x+3)^2",
		f:        func(x float64) float64 { return math.Pow(x+3, 2) },
		a:        -10,
		b:        0,
		expected: -3,
	},
	{
		fStr:     "f(x)=xlog(x)",
		f:        func(x float64) float64 { return x * math.Log(x) },
		a:        0,
		b:        1,
		expected: 1 / math.E,
	},
	{
		fStr:     "f(x)=x^3-6x^2+9x+1",
		f:        func(x float64) float64 { return math.Pow(x, 3) - 6*math.Pow(x, 2) + 9*x + 1 },
		a:        0,
		b:        4,
		expected: 3,
	},
	{
		fStr:     "f(x)=tan(x)",
		f:        func(x float64) float64 { return math.Tan(x) },
		a:        0,
		b:        math.Pi / 2,
		expected: 0,
	},
	{
		fStr:     "f(x)=x^2-4x+4",
		f:        func(x float64) float64 { return math.Pow(x, 2) - 4*x + 4 },
		a:        0,
		b:        5,
		expected: 2,
	},
	{
		fStr:     "f(x)=cosh(x)",
		f:        func(x float64) float64 { return math.Cosh(x) },
		a:        -2,
		b:        2,
		expected: 0,
	},
}

func TestLineSearch(t *testing.T) {
	for _, tt := range testCases {
		for _, optimiser := range optimisers {
			testName := fmt.Sprintf("%s_%s", getNameOfFunc(optimiser), tt.fStr)
			t.Run(testName, func(t *testing.T) {
				result, err := optimiser(Params{tt.f, tt.a, tt.b, 0.0001, 1000})
				if err != nil {
					t.Errorf("got error: %s", err)
				} else {
					if math.Abs(result-tt.expected) > 0.001 {
						t.Errorf("got %f, want %f", result, tt.expected)
					}
				}
			})
		}
	}
}

func getNameOfFunc(f any) string {
	return runtime.FuncForPC(reflect.ValueOf(f).Pointer()).Name()
}
