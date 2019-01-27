cmake_minimum_required(VERSION 3.7)
project(Sudoku)

set(CMAKE_CXX_STANDARD 11)

set(SOURCE_FILES
        Board.cpp
        Board.h
        d_except.cpp
        d_except.h
        d_matrix.cpp
        d_matrix.h
        main.cpp)

add_executable(Sudoku ${SOURCE_FILES})