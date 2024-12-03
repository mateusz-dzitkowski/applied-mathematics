#include <iostream>
#include "Model.h"
#include "Params.h"


int main() {
    constexpr Params params {
        .max_velocity = 5,
        .road_length = 100,
        .car_density = 0.4,
        .decelerate_probability = 0.4,
    };

    auto model = Model(params);
    model.run(100);
    std::cout << std::format("{}", model.mean_velocity());

    return 0;
}
