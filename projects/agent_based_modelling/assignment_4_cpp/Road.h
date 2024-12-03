#ifndef ROAD_H
#define ROAD_H
#include "Car.h"


class Road {
public:
    int length;
    Car** lane;
    explicit Road(int);
    [[nodiscard]] bool is_occupied(int) const;
};



#endif //ROAD_H
