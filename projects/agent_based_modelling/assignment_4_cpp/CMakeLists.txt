cmake_minimum_required(VERSION 3.30)
project(assignment_4_cpp)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(
    assignment_4_cpp
    main.cpp
    Car.cpp
    Car.h
        Road.cpp
        Road.h
        Model.cpp
        Model.h
        Params.cpp
        Params.h
)
