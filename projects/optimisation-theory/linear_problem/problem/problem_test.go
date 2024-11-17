package problem

import (
	"github.com/stretchr/testify/assert"
	"math"
	"testing"
)

type TestEmissionsStore float64

func (es TestEmissionsStore) AllEmissions() []Emission {
	return []Emission{EmissionSO2}
}

func (es TestEmissionsStore) Get(_ Emission) float64 {
	return float64(es)
}

var tests = []struct {
	name     string
	p        Problem
	expected []float64
}{
	{
		name: "basic case with one incinerator",
		p: Problem{
			TonsOfTrashPerDay: 10,
			Incinerators: []Incinerator{
				{
					DailyCapacityTons: 10,
					CostPerTon:        5,
					EmissionsPerTon:   TestEmissionsStore(0),
				},
			},
			EmissionLimitsPerDay: TestEmissionsStore(5),
			EmissionsCost:        TestEmissionsStore(10),
		},
		expected: []float64{10},
	},
	{
		name: "an obviously better incinerator",
		p: Problem{
			TonsOfTrashPerDay: 10,
			Incinerators: []Incinerator{
				{
					DailyCapacityTons: 10,
					CostPerTon:        5,
					EmissionsPerTon:   TestEmissionsStore(0),
				},
				{
					DailyCapacityTons: 10,
					CostPerTon:        10,
					EmissionsPerTon:   TestEmissionsStore(0),
				},
			},
			EmissionLimitsPerDay: TestEmissionsStore(5),
			EmissionsCost:        TestEmissionsStore(10),
		},
		expected: []float64{10, 0},
	},
	{
		name: "they have to sum to TonsOfTrashPerDay",
		p: Problem{
			TonsOfTrashPerDay: 10,
			Incinerators: []Incinerator{
				{
					DailyCapacityTons: 5,
					CostPerTon:        5,
					EmissionsPerTon:   TestEmissionsStore(10),
				},
				{
					DailyCapacityTons: 5,
					CostPerTon:        10,
					EmissionsPerTon:   TestEmissionsStore(0),
				},
			},
			EmissionLimitsPerDay: TestEmissionsStore(5),
			EmissionsCost:        TestEmissionsStore(10),
		},
		expected: []float64{5, 5},
	},
	{
		name: "full send on the better one and leftovers for the second one",
		p: Problem{
			TonsOfTrashPerDay: 10,
			Incinerators: []Incinerator{
				{
					DailyCapacityTons: 8,
					CostPerTon:        5,
					EmissionsPerTon:   TestEmissionsStore(0),
				},
				{
					DailyCapacityTons: 10,
					CostPerTon:        5,
					EmissionsPerTon:   TestEmissionsStore(10),
				},
			},
			EmissionLimitsPerDay: TestEmissionsStore(10),
			EmissionsCost:        TestEmissionsStore(10),
		},
		expected: []float64{8, 2},
	},
}

func TestProblem(t *testing.T) {
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			solution, err := tt.p.Solve()
			assert.Nil(t, err)
			assert.Equal(t, len(solution), len(tt.expected))
			for n := range solution {
				assert.True(t, isCLose(solution[n], tt.expected[n]))
			}
		})
	}
}

func isCLose(x, y float64) bool {
	return math.Abs(x-y) < 1e-7
}
