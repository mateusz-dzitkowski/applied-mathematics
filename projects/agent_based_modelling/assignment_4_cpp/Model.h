#ifndef MODEL_H
#define MODEL_H
#include <random>
#include "Params.h"
#include "Road.h"



class Model {
public:
    Params params;
    Road road;
    std::mt19937 rng_engine;
    std::uniform_real_distribution<> rng_distribution;

    explicit Model(const Params &);

    void step();
    void run(int);
    std::string to_string() const;
    double mean_velocity() const;
private:
    [[nodiscard]] int max_possible_velocity(int, int) const;
    double uniform();
};



#endif //MODEL_H
