package problem

type Emissions[T any] struct {
	SO2, Particulate T
}

type EmissionsPerTon Emissions[int]
type EmissionsPerDay Emissions[int]
type EmissionsCost Emissions[int]

type Incinerator struct {
	Name              string
	DailyCapacityTons int
	CostPerTon        int
	EmissionsPerTon
}

type Problem struct {
	TonsOfTrashPerDay    int
	Incinerators         []Incinerator
	EmissionLimitsPerDay EmissionsPerDay
	EmissionsCost
}

func MainProblem() Problem {
	return Problem{
		TonsOfTrashPerDay: 7500,
		Incinerators: []Incinerator{
			{
				Name:              "Incinerator 1",
				DailyCapacityTons: 1900,
				CostPerTon:        16,
				EmissionsPerTon: EmissionsPerTon{
					SO2:         120,
					Particulate: 18,
				},
			},
			{
				Name:              "Incinerator 2",
				DailyCapacityTons: 3000,
				CostPerTon:        13,
				EmissionsPerTon: EmissionsPerTon{
					SO2:         230,
					Particulate: 20,
				},
			},
			{
				Name:              "Incinerator 3",
				DailyCapacityTons: 1800,
				CostPerTon:        13,
				EmissionsPerTon: EmissionsPerTon{
					SO2:         150,
					Particulate: 30,
				},
			},
			{
				Name:              "Incinerator 4",
				DailyCapacityTons: 2300,
				CostPerTon:        13,
				EmissionsPerTon: EmissionsPerTon{
					SO2:         250,
					Particulate: 29,
				},
			},
		},
		EmissionLimitsPerDay: EmissionsPerDay{
			SO2:         1000000,
			Particulate: 100000,
		},
		EmissionsCost: EmissionsCost{
			SO2:         100,
			Particulate: 400,
		},
	}
}