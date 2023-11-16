#include <array>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

#include "Eigen/Dense"
#include "Eigen/src/Core/Matrix.h"

using Eigen::MatrixXi;

int main(void) {
    std::ifstream text_input("../day15.txt");
    std::string input;
    MatrixXi ingredients;

    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            std::cout << "Line: '" << input << "'" << std::endl;
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    ingredients = MatrixXi{{-1, -2, 6, 3}, {2, 3, -2, -1}}.transpose();

    std::cout << "Ingredients: \n" << ingredients << std::endl << std::endl;

    for (int i = 0; i <= 100; i++) {
        MatrixXi v{{i}, {100 - i}};

        MatrixXi s = ingredients * v;

        int ans = 1;

        for (auto const &col : s.col(0)) {
            if (col > 0) {
                ans *= col;
            } else {
                ans = 0;
                break;
            }
        }

        std::cout << "Answer: " << ans << std::endl;
    }
}
