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

bool is_valid(MatrixXi m) {
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

bool generate_selection(unsigned int seed, MatrixXi &selection, Eigen::VectorXi &unknowns) {

    selection = MatrixXi::Zero(selection.rows(), selection.cols());

    // std::cout << "Seed: " << seed << std::endl;

    uint8_t j = 0;
    for (int row = 0; row < (selection.rows() - 1); row++) {
        int col = row + 1;
        for (; col < selection.cols() - 1; col++) {
            unknowns[j] = (seed >> j) & 0x1;
            selection(row, col) = unknowns[j];
            selection(col, row) = unknowns[j];
            j++;
        }
        switch ((int)selection.row(row).sum()) {
        case 2:
            break;
        case 1:
            selection(row, col) = 1;
            selection(col, row) = 1;
            break;
        default:
            return false;
        }
    }

    // std::cout << "Selection:\n" << selection << std::endl <<std::endl;

    return is_valid(selection);
}

int old_try(void) {
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

    MatrixXi weights = MatrixXi::Zero(names.size(), names.size());

    unsigned int row = 0;
    unsigned int col = 0;
    for (auto &n : names) {
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

    // weights = MatrixXd{{{0, 54, -79, -2}, {83, 0, -7, -63}, {-62, 60, 0, 55}, {46, -7, 41, 0}}};

    std::cout << "Weights: \n" << weights << std::endl << std::endl;

    MatrixXi selection = MatrixXi::Zero(weights.rows(), weights.cols());

    int permutations = 0;
    for (int i = 1; i < weights.cols(); i++) {
        permutations += i;
    }
    permutations -= (weights.cols() - 1);

    std::cout << "Permutations: " << permutations << std::endl;

    std::set<int> happiness;

    for (unsigned int seed = 0; seed < (0x1 << permutations); seed++) {
        Eigen::VectorXi unknowns(permutations);

        // Not very pretty but will do the job

        if (generate_selection(seed, selection, unknowns)) {
            // std::cout << "Selection:\n" << selection << std::endl << std::endl;
            MatrixXi m = weights.array() * selection.array();
            // std::cout << m << std::endl << std::endl;
            int s = m.sum();
            // std::cout << s << std::endl;
            happiness.insert(s);
            std::cout << ((float)seed / (0x1 << permutations)) * 100 << " % done\r";
        }
    }
    std::cout << std::endl;

    std::cout << "Part 1:\n Happiness: " << *happiness.rbegin();

    weights.conservativeResize(weights.cols() + 1, weights.rows() + 1);
    weights.row(weights.rows() - 1).setZero();
    weights.col(weights.cols() - 1).setZero();
    std::cout << "Weights: \n" << weights << std::endl << std::endl;

    selection = MatrixXi::Zero(weights.rows(), weights.cols());

    permutations = 0;
    for (int i = 1; i < weights.cols(); i++) {
        permutations += i;
    }
    permutations -= (weights.cols() - 1);

    std::cout << "Permutations: " << permutations << std::endl;

    happiness.clear();

    for (unsigned int seed = 0; seed < (0x1 << permutations); seed++) {
        Eigen::VectorXi unknowns(permutations);

        // Not very pretty but will do the job

        if (generate_selection(seed, selection, unknowns)) {
            // std::cout << "Selection:\n" << selection << std::endl << std::endl;
            MatrixXi m = weights.array() * selection.array();
            // std::cout << m << std::endl << std::endl;
            int s = m.sum();
            // std::cout << s << std::endl;
            happiness.insert(s);
            std::cout << ((float)seed / (0x1 << permutations)) * 100 << " % done\r";
        }
    }
    std::cout << std::endl;

    std::cout << "Part 2:\n Happiness: " << *happiness.rbegin();

    // 634 too high
    // 618 too high
    return 0;
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

    MatrixXi weights = MatrixXi::Zero(names.size(), names.size());

    unsigned int row = 0;
    unsigned int col = 0;
    for (auto &n : names) {
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

    // weights = MatrixXi{{{0, 54, -79, -2}, {83, 0, -7, -63}, {-62, 60, 0, 55}, {46, -7, 41, 0}}};

    std::cout << "Weights: \n" << weights << std::endl << std::endl;

    MatrixXi selection = MatrixXi::Zero(weights.rows(), weights.cols());

    // Generate first line (A sits beside B and the LAST element)
    Eigen::RowVectorXi arrange = Eigen::RowVectorXi::Zero(weights.rows());
    arrange[1] = 1;
    arrange[arrange.size() - 1] = 1;

    selection.row(0) = arrange;

    for (int i = 1; i < selection.rows(); i++) {
        int carry = arrange[arrange.size() - 1];

        Eigen::RowVectorXi shift = arrange.head(arrange.size() - 1);

        arrange.segment(1, arrange.size() - 1) = shift;
        arrange[0] = carry;

        std::cout << arrange << std::endl;
        selection.row(i) = arrange;
    }

    // //    MatrixXd selection{{{0, 1, 0, 0, 1}, {1, 0, 1, 0, 0}, {0, 1, 0, 1, 0}, {0, 0, 1, 0, 1}, {1, 0, 0, 1, 0}}};
    // //    MatrixXd selection{{{0, 0, 1, 1}, {0, 0, 1, 1}, {1, 1, 0, 0}, {1, 1, 0, 0}}};

    std::cout << "Selection: \n" << selection << std::endl << std::endl;
    MatrixXi x = weights.array() * selection.array();
    // std::cout << m << std::endl << std::endl;
    int s = x.sum();
    std::cout << s << std::endl;

    int cnt = 0;

    for (int i = 0; i < selection.rows() - 1; i++) {
        for (int j = i + 1; j < selection.rows(); j++) {
            MatrixXi m = switchSeats(selection, i, j);

            // std::cout << "Matrix (#" << cnt + 1 << "):\n" << m << std::endl << std::endl;
            // cnt++;

            MatrixXi x = weights.array() * m.array();
            // std::cout << m << std::endl << std::endl;
            int s = x.sum();
            std::cout << s << std::endl;
            //            happiness.insert(s);
        }
    }

    return 0;
}
