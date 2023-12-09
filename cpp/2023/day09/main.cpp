#include <fstream>
#include <iostream>
#include <string>
#include <vector>

// Hat-tip to https://stackoverflow.com/a/28142357
#include <regex>
#include <type_traits>
#include <vector>
std::vector<std::string> resplit(const std::string &s, const std::regex &sep_regex = std::regex{"\\s+"}) {
    std::sregex_token_iterator iter(s.begin(), s.end(), sep_regex, -1);
    std::sregex_token_iterator end;
    return {iter, end};
}

bool is_line_zero(std::vector<int> &l) {
    for (auto it : l) {
        if (it != 0)
            return false;
    }
    return true;
}

int part1(std::vector<int> const measurement) {
    std::vector<std::vector<int>> extrapolation({measurement});

    // until last line in extrapolation is all 0
    auto prev = extrapolation.rbegin();

    while (!is_line_zero(*prev)) {

        extrapolation.push_back({});
        auto it = extrapolation.rbegin();
        prev = it + 1; // prev needs to point to new memory space!

        for (int i = 0; i + 1 < prev->size(); i++) {
            int v = prev->at(i + 1) - prev->at(i);
            // std::cout << v << ", ";
            it->push_back(v);
        }

        prev = it;

        // std::cout << std::endl;
    }

    // Now calculate the next element of measurement
    for (auto it = extrapolation.rbegin(); it + 1 != extrapolation.rend(); it++) {
        auto next = it + 1;
        int next_val = it->back() + next->back();
        // std::cout << "Next val: " << next_val << std::endl;
        next->push_back(next_val);
    }

    return extrapolation.begin()->back();
}

int part2(std::vector<int> const measurement) {
    std::vector<std::vector<int>> extrapolation({measurement});

    // until last line in extrapolation is all 0
    auto prev = extrapolation.rbegin();

    while (!is_line_zero(*prev)) {

        extrapolation.push_back({});
        auto it = extrapolation.rbegin();
        prev = it + 1; // prev needs to point to new memory space!

        for (int i = 0; i + 1 < prev->size(); i++) {
            int v = prev->at(i + 1) - prev->at(i);
            // std::cout << v << ", ";
            it->push_back(v);
        }

        prev = it;

        // std::cout << std::endl;
    }

    std::vector<int> answer({extrapolation.rbegin()->front()});
    // Now calculate the prev element of measurement
    for (auto next = extrapolation.rbegin() + 1; next != extrapolation.rend(); next++) {
        int next_val = next->front() - answer.back();
        // std::cout << "Next val: " << next_val << std::endl;
        answer.push_back(next_val);
    }

    return *answer.rbegin();
}

int main(void) {
    std::ifstream text_input("../day09.txt");
    std::string input;
    std::vector<std::vector<int>> measurements;

    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            std::vector<std::string> v = resplit(input, std::regex(" +"));
            measurements.push_back({});
            auto it = measurements.rbegin();
            for (auto m : v) {
                it->push_back(std::stoi(m));
            }
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    // measurements.clear();
    // measurements = {{0, 3, 6, 9, 12, 15}, {1, 3, 6, 10, 15, 21}, {10, 13, 16, 21, 30, 45}};

    int p1 = 0;
    int i = 1;
    for (auto it : measurements) {
        p1 += part1(it);
    }

    std::cout << "Part 1:\nAnswer: " << p1 << std::endl << std::endl;

    int p2 = 0;
    i = 1;
    for (auto it : measurements) {
        // std::cout << i++ << ": (";
        for (auto v : it) {
            // std::cout << v << ", ";
        }
        // std::cout << ")" << std::endl;
        p2 += part2(it);
    }

    std::cout << "Part 2:\nAnswer: " << p2 << std::endl << std::endl;
}
