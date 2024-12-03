#include <iostream>
#include <random>
#include <string>
#include <sstream>
#include "Model.h"


Model::Model(const Params &params): params(params), road(params.road_length) {
    rng_engine = std::mt19937(std::random_device{}());
    rng_distribution = std::uniform_real_distribution<>(0.0, 1.0);

    for (int i = 0; i < params.road_length; i++) {
        if (uniform() < params.car_density) {
            road.lane[i] = new Car(params.max_velocity);
        }
    }
}

void Model::step() {
    Car* next_lane[params.road_length];
    for (int i = 0; i < params.road_length; i++) {
        next_lane[i] = nullptr;
    }
    for (int i = 0; i < params.road_length; i++) {
        if (road.lane[i] == nullptr) {continue;}
        Car* car = road.lane[i];
        car->accelerate();
        car->velocity = max_possible_velocity(i, car->velocity);
        if (uniform() < params.decelerate_probability) {
            car->decelerate();
        }
        next_lane[(i + car->velocity)%params.road_length] = car;
    }
    for (int i = 0; i < params.road_length; i++) {
        road.lane[i] = next_lane[i];
    }
}

int Model::max_possible_velocity(const int i, const int velocity) const {
    for (int j = 0; j < velocity; j++) {
        if (road.is_occupied(i + j + 1)) {
            return j;
        }
    }
    return velocity;
}

double Model::uniform() {
    return rng_distribution(rng_engine);
}

std::string Model::to_string() const {
    std::ostringstream oss;
    oss << "[";
    for (int i = 0; i < params.road_length; i++) {
        if (road.lane[i] == nullptr) {
            oss << " ";
        } else {
            oss << std::format("{}", road.lane[i]->velocity);
        }
    }
    oss << "]\n";
    return oss.str();
}

void Model::run(const int steps) {
    std::cout << to_string();
    for (int i = 0; i < steps; i++) {
        step();
        std::cout << to_string();
    }
}

double Model::mean_velocity() const {
    int sum = 0;
    int cars = 0;

    for (int i = 0; i < params.road_length; i++) {
        if (road.lane[i] == nullptr) {continue;}
        sum += road.lane[i]->velocity;
        cars += 1;
    }
    return static_cast<double>(sum) / static_cast<double>(cars);
}

