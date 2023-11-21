#include <fstream>
#include <iostream>
#include <string>

#include "Eigen/Dense"
#include "Eigen/src/Core/Matrix.h"

using Eigen::MatrixXi;

void print(MatrixXi m) {
    for (auto const r : m.rowwise()) {
        for (auto const light : r) {
            if (light == 0) {
                std::cout << '.';
            } else if (light == 1) {
                std::cout << '#';
            }
        }
        std::cout << std::endl;
    }
}

MatrixXi step_p1(MatrixXi m) {
    MatrixXi n = MatrixXi::Zero(m.rows(), m.cols());
    MatrixXi kernel = MatrixXi{{1, 1, 1}, {1, 0, 1}, {1, 1, 1}};

    // Let the kernel iterate over the matrix and set the pixels in the new 'n' Matrix
    for (int row = 0; row < m.rows() - 2; row++) {
        for (int col = 0; col < m.cols() - 2; col++) {

            // std::cout << "m:\n" << m.block<3, 3>(row, col) << std::endl;
            MatrixXi neighbors = m.block<3, 3>(row, col).array() * kernel.array();
            int sum_neighbors = neighbors.sum();

            int new_pixel = m(row + 1, col + 1);
            if (new_pixel == 1) {
                if (!(sum_neighbors == 2 || sum_neighbors == 3)) {
                    new_pixel = 0;
                }
            } else {
                if (sum_neighbors == 3) {
                    new_pixel = 1;
                }
            }
            n(row + 1, col + 1) = new_pixel;
        }
    }

    return n;
}

MatrixXi step_p2(MatrixXi m) {
    MatrixXi n = MatrixXi::Zero(m.rows(), m.cols());
    MatrixXi kernel = MatrixXi{{1, 1, 1}, {1, 0, 1}, {1, 1, 1}};

    // Let the kernel iterate over the matrix and set the pixels in the new 'n' Matrix
    for (int row = 0; row < m.rows() - 2; row++) {
        for (int col = 0; col < m.cols() - 2; col++) {

            // std::cout << "m:\n" << m.block<3, 3>(row, col) << std::endl;
            MatrixXi neighbors = m.block<3, 3>(row, col).array() * kernel.array();
            int sum_neighbors = neighbors.sum();

            int new_pixel = m(row + 1, col + 1);
            if (new_pixel == 1) {
                if (!(sum_neighbors == 2 || sum_neighbors == 3)) {
                    new_pixel = 0;
                }
            } else {
                if (sum_neighbors == 3) {
                    new_pixel = 1;
                }
            }
            n(row + 1, col + 1) = new_pixel;

            // Corners are stuck
            n(1, 1) = 1;
            n(1, n.cols() - 2) = 1;
            n(n.rows() - 2, 1) = 1;
            n(n.rows() - 2, n.cols() - 2) = 1;
        }
    }

    return n;
}

int main(void) {
    std::ifstream text_input("../day18.txt");
    std::string input;

    MatrixXi lights = MatrixXi::Zero(1, 1);

    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            std::cout << "Line: '" << input << "'" << std::endl;
            // Add a new row
            lights.conservativeResize(lights.rows() + 1, input.size() + 2);
            lights.row(lights.rows() - 1).setZero();

            int i = 1;
            for (auto const light : input) {
                if (light == '#') {
                    lights.row(lights.rows() - 1)[i++] = 1;

                } else if (light == '.') {
                    lights.row(lights.rows() - 1)[i++] = 0;
                }
            }
        }
        lights.conservativeResize(lights.rows() + 1, lights.cols());
        lights.row(lights.rows() - 1).setZero();

        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    // Example hand compiled
    // lights = MatrixXi{{0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 1, 0, 1, 0, 1, 0}, {0, 0, 0, 0, 1, 1, 0, 0}, {0, 1, 0, 0, 0, 0, 1, 0},
    //                   {0, 0, 0, 1, 0, 0, 0, 0}, {0, 1, 0, 1, 0, 0, 1, 0}, {0, 1, 1, 1, 1, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0}};

    std::cout << "lights: " << lights.rows() << "x" << lights.cols() << std::endl << std::endl;

    std::cout << "Initial:\n" << std::endl;
    print(lights);

    MatrixXi lights_p1(lights);

    for (int i = 0; i < 100; i++) {
        lights_p1 = step_p1(lights_p1);
        // std::cout << i + 1 << ":\n" << std::endl;
        // print(lights_p1);
    }

    std::cout << std::endl << "Part 1:\nAnswer: " << lights_p1.sum() << std::endl << std::endl;

    MatrixXi lights_p2(lights);
    lights_p2(1, 1) = 1;
    lights_p2(1, lights_p2.cols() - 2) = 1;
    lights_p2(lights_p2.rows() - 2, 1) = 1;
    lights_p2(lights_p2.rows() - 2, lights_p2.cols() - 2) = 1;

    for (int i = 0; i < 100; i++) {
        lights_p2 = step_p2(lights_p2);
        // std::cout << i + 1 << ":\n" << std::endl;
        // print(lights_p2);
    }

    std::cout << std::endl << "Part 2:\nAnswer: " << lights_p2.sum() << std::endl << std::endl;
}
