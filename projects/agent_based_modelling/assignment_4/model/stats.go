package model

func (m *Model) MeanVelocity() float64 {
	var carCount int
	var velocitySum int

	for _, c := range m.Road.Lane {
		if c == nil {
			continue
		}

		velocitySum += c.Velocity
		carCount += 1
	}

	if carCount == 0 {
		return 0
	}
	return float64(velocitySum) / float64(carCount)
}
