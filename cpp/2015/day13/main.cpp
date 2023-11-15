#include <array>
#include <cstdint>
#include <cstdio>
#include <fstream>
#include <iostream>
#include <map>
#include <ostream>
#include <regex>
#include <set>
#include <string>
#include <unordered_set>
#include <vector>

#include "Eigen/Dense"
#include "Eigen/src/Core/Matrix.h"

using Eigen::MatrixXi;

// Hat-tip to https://stackoverflow.com/a/28142357
std::vector<std::string> resplit(const std::string &s, const std::regex &sep_regex = std::regex{"\\s+"}) {
    std::sregex_token_iterator iter(s.begin(), s.end(), sep_regex, -1);
    std::sregex_token_iterator end;
    return {iter, end};
}

MatrixXi switchSeats(MatrixXi matrix, unsigned int a, unsigned int b) {
    MatrixXi m(matrix);
    // Switch seats a and b

    MatrixXi ra(m.row(a));
    MatrixXi rb(m.row(b));

    m.row(a) = rb;
    m.row(b) = ra;

    MatrixXi ca(m.col(a));
    MatrixXi cb(m.col(b));

    m.col(a) = cb;
    m.col(b) = ca;

    return m;
}

std::set<int> recursive(MatrixXi const &weights, MatrixXi selection, int depth) {
    std::set<int> total_happiness;

    // std::cout << "Entering recursive with depth: " << depth << " selection: \n" << selection << std::endl << std::endl;

    if (depth == weights.rows() - 1) {
        // Now we calculate!
        // std::cout << "Calc..." << std::endl;

        MatrixXi x = weights.array() * selection.array();
        int s = x.sum();
        total_happiness.insert(s);

    } else {
        for (int i = depth; i < weights.rows(); i++) {
            MatrixXi m = switchSeats(selection, depth, i);
            std::set<int> tmp = recursive(weights, m, depth + 1);
            total_happiness.insert(tmp.begin(), tmp.end());
        }
    }

    return total_happiness;
}

MatrixXi get_default_selection(int size) {
    MatrixXi selection = MatrixXi::Zero(size, size);

    // Generate first line (A sits beside B and the LAST element)
    Eigen::RowVectorXi arrange = Eigen::RowVectorXi::Zero(size);
    arrange[1] = 1;
    arrange[arrange.size() - 1] = 1;

    selection.row(0) = arrange;

    for (int i = 1; i < selection.rows(); i++) {
        int carry = arrange[arrange.size() - 1];

        Eigen::RowVectorXi shift = arrange.head(arrange.size() - 1);

        arrange.segment(1, arrange.size() - 1) = shift;
        arrange[0] = carry;

        selection.row(i) = arrange;
    }

    return selection;
}

MatrixXi populate_weights(std::map<std::string, std::map<std::string, int>> happiness_per_name) {
    MatrixXi weights = MatrixXi::Zero(happiness_per_name.size(), happiness_per_name.size());

    // Will fill the weights matrix
    unsigned int row = 0;
    unsigned int col = 0;
    for (auto &n : happiness_per_name) {
        col = 0;
        for (auto &a : n.second) {
            if (row == col) {
                col++;
            }
            weights(row, col) = a.second;
            col++;
        }
        row++;
    }

    return weights;
}

int main(void) {
    std::ifstream text_input("../day13.txt");
    std::string input;

    std::map<std::string, std::map<std::string, int>> names;

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

            auto n = names.find(a);
            if (n == names.end()) {
                std::cout << "Adding: " << a << std::endl;
                names.insert({a, {}});
            }

            names.at(a).insert({b, happiness});

            for (auto &n : names) {
                std::cout << n.first << ": ";
                for (auto &a : n.second) {
                    std::cout << "(" << a.first << " -> " << a.second << "), ";
                }
                std::cout << std::endl;
            }
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    MatrixXi weights = populate_weights(names);

    // weights = MatrixXi{{{0, 54, -79, -2}, {83, 0, -7, -63}, {-62, 60, 0, 55}, {46, -7, 41, 0}}};

    MatrixXi selection = get_default_selection(weights.rows());

    std::cout << "Weights: \n" << weights << std::endl << std::endl;

    std::set<int> tot_happiness = recursive(weights, selection, 0);

    std::cout << "Part 1:\n Happiness: " << *tot_happiness.rbegin() << std::endl << std::endl;

    // Now add "me" with 0 on every side
    weights.conservativeResize(weights.cols() + 1, weights.rows() + 1);
    weights.row(weights.rows() - 1).setZero();
    weights.col(weights.cols() - 1).setZero();
    std::cout << "Weights: \n" << weights << std::endl << std::endl;

    selection = get_default_selection(weights.rows());

    tot_happiness.clear();

    tot_happiness = recursive(weights, selection, 0);

    std::cout << "Part 2:\n Happiness: " << *tot_happiness.rbegin() << std::endl << std::endl;

    return 0;
}
