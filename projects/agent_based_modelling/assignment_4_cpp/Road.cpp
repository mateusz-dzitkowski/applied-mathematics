#include "Road.h"


Road::Road(const int length): length(length) {
    lane = new Car*[length];
    for (int i = 0; i < length; i++) {
        lane[i] = nullptr;
    }
}

bool Road::is_occupied(const int n) const {
    return lane[n % length] != nullptr;
}
