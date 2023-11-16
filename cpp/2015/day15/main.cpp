#include <array>
#include <fstream>
#include <iostream>
#include <ostream>
#include <set>
#include <string>
#include <vector>

#include "Eigen/Dense"
#include "Eigen/src/Core/Matrix.h"

using Eigen::MatrixXi;

void recursive_calc(MatrixXi const &ingredients, int depth, std::vector<int> mixes, int left, std::set<int> &scores, std::set<int> &scores_500cal) {
    // std::cout << "Depth: " << depth << ", Left: " << left << std::endl;
    if (depth == ingredients.cols() - 1) {
        // calc

        MatrixXi v = MatrixXi::Zero(ingredients.cols(), 1);

        int i = 0;
        for (auto m : mixes) {
            v(i++, 0) = m;
        }

        v(i, 0) = left;

        // std::cout << "v: (" << v.rows() << "x" << v.cols() << ")\n" << v << std::endl << std::endl;

        // std::cout << "ing:\n" << ingredients << std::endl << std::endl;

        MatrixXi s = ingredients * v;

        int ans = 1;

        for (int i = 0; i < 4; i++) {
            if (s.col(0)[i] > 0) {
                ans *= s.col(0)[i];
            } else {
                ans = 0;
                break;
            }
        }

        scores.insert(ans);

        if (s.col(0)[4] == 500) {
            scores_500cal.insert(ans);
        }

    } else {
        // Go deeper
        for (int i = 0; i < left; i++) {

            std::vector<int> mixes_new(mixes);

            mixes_new.push_back(i);

            recursive_calc(ingredients, depth + 1, mixes_new, left - i, scores, scores_500cal);
        }
    }

    return;
}

// Hat-tip to https://stackoverflow.com/a/28142357
#include <regex>
#include <vector>
std::vector<std::string> resplit(const std::string &s, const std::regex &sep_regex = std::regex{"\\s+"}) {
    std::sregex_token_iterator iter(s.begin(), s.end(), sep_regex, -1);
    std::sregex_token_iterator end;
    return {iter, end};
}

int main(void) {
    std::ifstream text_input("../day15.txt");
    std::string input;
    MatrixXi ingredients; // = MatrixXi::Zero(5, 4);

    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            std::cout << "Line: '" << input << "'" << std::endl;

            std::vector<std::string> s = resplit(input, std::regex(" "));

            MatrixXi col = MatrixXi::Zero(5, 1);
            col(0, 0) = std::stoi(s[2].substr(0, s[2].size() - 1));
            col(1, 0) = std::stoi(s[4].substr(0, s[4].size() - 1));
            col(2, 0) = std::stoi(s[6].substr(0, s[6].size() - 1));
            col(3, 0) = std::stoi(s[8].substr(0, s[8].size() - 1));
            col(4, 0) = std::stoi(s[10]);

            ingredients.conservativeResize(5, ingredients.cols() + 1);
            ingredients.col(ingredients.cols() - 1) = col;
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    // ingredients = MatrixXi{{-1, -2, 6, 3, 8}, {2, 3, -2, -1, 3}}.transpose();

    std::cout << "Ingredients: \n" << ingredients << std::endl << std::endl;
    std::vector<int> mixes;
    std::set<int> scores;
    std::set<int> scores_500cal;
    recursive_calc(ingredients, 0, mixes, 100, scores, scores_500cal);

    std::cout << "Part 1\nAnswer: " << *scores.rbegin() << std::endl;
    std::cout << "Part 2\nAnswer: " << *scores_500cal.rbegin() << std::endl;
}
