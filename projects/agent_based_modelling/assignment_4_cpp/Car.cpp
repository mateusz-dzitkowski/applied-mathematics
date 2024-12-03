#include "Car.h"


Car::Car(const int max_velocity): max_velocity(max_velocity) {}

void Car::accelerate() {
    if (velocity < max_velocity) {
        velocity++;
    }
}

void Car::decelerate() {
    if (velocity > 0) {
        velocity = velocity - 1;
    }
}
