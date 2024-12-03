#ifndef CAR_H
#define CAR_H



class Car {
public:
    int max_velocity;
    int velocity = 0;
    explicit Car(int);
    void accelerate();
    void decelerate();
};



#endif //CAR_H
