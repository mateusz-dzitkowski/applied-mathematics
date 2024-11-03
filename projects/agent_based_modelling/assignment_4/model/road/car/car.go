package car

type Car struct {
	Velocity, MaxVelocity int
}

func New(maxVelocity int) *Car {
	return &Car{MaxVelocity: maxVelocity}
}

func (c *Car) Accelerate() {
	if c.Velocity < c.MaxVelocity {
		c.Velocity += 1
	}
}

func (c *Car) Decelerate() {
	if c.Velocity > 0 {
		c.Velocity -= 1
	}
}
