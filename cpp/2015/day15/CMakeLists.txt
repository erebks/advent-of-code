cmake_minimum_required (VERSION 2.6)
project (aoc)
include_directories( "../../libs/eigen-3.4.0/" )
add_executable(aoc main.cpp)
set (CMAKE_EXPORT_COMPILE_COMMANDS ON)
