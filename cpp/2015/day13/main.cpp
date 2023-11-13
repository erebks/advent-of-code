#include <array>
#include <cstdint>
#include <cstdio>
#include <fstream>
#include <iostream>
#include <map>
#include <regex>
#include <set>
#include <string>
#include <unordered_set>
#include <vector>

#include "Eigen/Dense"
#include "Eigen/src/Core/Matrix.h"

using Eigen::MatrixXd;

bool is_valid(MatrixXd m) {
    if (m.sum() != 2 * m.rows()) {
        return false;
    }

    if (m.diagonal().sum() != 0) {
        return false;
    }

    for (auto const &row : m.rowwise()) {
        if (row.sum() != 2) {
            return false;
        }
    }

    for (auto const &col : m.colwise()) {
        if (col.sum() != 2) {
            return false;
        }
    }

    for (int i = 0; i < m.rows(); i++) {
        for (int i2 = 0; i2 < m.rows(); i2++) {
            if (m.row(i)[i2] != m.col(i)[i2]) {
                return false;
            }
        }
    }

    return true;
}

// Hat-tip to https://stackoverflow.com/a/28142357
std::vector<std::string> resplit(const std::string &s, const std::regex &sep_regex = std::regex{"\\s+"}) {
    std::sregex_token_iterator iter(s.begin(), s.end(), sep_regex, -1);
    std::sregex_token_iterator end;
    return {iter, end};
}

int main(void) {
    std::ifstream text_input("../day13.txt");
    std::string input;

    std::map<std::string, std::map<std::string, int>> names;

    MatrixXd weights;

    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            std::cout << "Line: '" << input << "'" << std::endl;
            std::vector<std::string> line = resplit(input, std::regex(" "));

            std::string a = line[0];
            std::string b = line[10].substr(0, line[10].size() - 1);
            int happiness;
            if (line[2] == "gain") {
                happiness = std::stoi(line[3]);
            } else {
                happiness = -1 * std::stoi(line[3]);
            }
            std::cout << "A: " << a << ", B: " << b << ", Happiness: " << happiness << std::endl;
            std::map<std::string, int> x;
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    MatrixXd selection{{{0, 0, 1, 1}, {0, 0, 1, 1}, {1, 1, 0, 0}, {1, 1, 0, 0}}};

    //    MatrixXd weights{{{0, 54, -79, -2}, {83, 0, -7, -63}, {-62, 60, 0, 55}, {46, -7, 41, 0}}};

    int permutations = 0;
    for (int i = 0; i < weights.cols(); i++) {
        permutations += i;
    }

    std::cout << "Permutations: " << permutations << std::endl;

    std::set<int> happiness;

    for (int seed = 0; seed < (0x1 << permutations); seed++) {

        Eigen::VectorX<bool> unknowns(permutations);

        int j = 0;
        for (int row = 0; row < (selection.rows() - 1); row++) {
            for (int col = row + 1; col < selection.cols(); col++) {
                unknowns[j] = (seed >> j) & 0x1;
                selection(row, col) = unknowns[j];
                selection(col, row) = unknowns[j];
                j++;
            }
        }
        if (is_valid(selection)) {
            // std::cout << "Seed: " << seed << "\nUnknowns: \n" << unknowns << std::endl;
            // std::cout << "Selection:\n" << selection << std::endl << std::endl;
            MatrixXd m = weights.array() * selection.array();
            // std::cout << m << std::endl << std::endl;
            int s = m.sum();
            // std::cout << s << std::endl;
            happiness.insert(s);
        }
    }

    std::cout << "Happiness: " << *happiness.rbegin();

    // std::cout << selection << std::endl << std::endl;
    // std::cout << weights << std::endl << std::endl;

    // MatrixXd m = weights.array() * selection.array();

    // std::cout << m << std::endl << std::endl;
    // std::cout << m.sum() << std::endl;
}
