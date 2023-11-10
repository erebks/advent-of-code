#include <cstdlib>
#include <fstream>
#include <functional>
#include <iostream>
#include <regex>
#include <set>
#include <string>
#include <vector>

// Hat-tip to https://stackoverflow.com/a/28142357
std::vector<std::string> resplit(const std::string &s, const std::regex &sep_regex = std::regex{"\\s+"}) {
    std::sregex_token_iterator iter(s.begin(), s.end(), sep_regex, -1);
    std::sregex_token_iterator end;
    return {iter, end};
}

struct Present {

    unsigned int dimensions[3] = {};

    Present(unsigned int length, unsigned int width, unsigned int height) {
        std::multiset<unsigned int> dims{};
        dims.insert(length);
        dims.insert(width);
        dims.insert(height);

        size_t i{0};
        for (unsigned int dim : dims) {
            dimensions[i++] = dim;
        }
    }

    Present(std::string dimensions) {
        std::vector<std::string> v = resplit(dimensions, std::regex{"x"});
        std::multiset<unsigned int> dims{};

        for (const auto &dim : v) {
            dims.insert(std::stoi(dim));
        }

        size_t i{0};
        for (unsigned int dim : dims) {
            this->dimensions[i++] = dim;
        }
    }

    unsigned int get_surface_area(void) { return 2 * (dimensions[0] * dimensions[1] + dimensions[0] * dimensions[2] + dimensions[1] * dimensions[2]); }

    unsigned int get_needed_wrapping_paper(void) { return get_surface_area() + dimensions[0] * dimensions[1]; }

    unsigned int get_needed_ribbon(void) {
        unsigned int ribbon_wrap = dimensions[0] * 2 + dimensions[1] * 2;
        unsigned int ribbon_bow = dimensions[0] * dimensions[1] * dimensions[2];
        return ribbon_bow + ribbon_wrap;
    }
};

int main(void) {

    unsigned int tot_area_paper{0};
    unsigned int tot_len_ribbon{0};
    std::ifstream text_input("../day02.txt");
    std::string input;
    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            Present p = Present(input);
            tot_area_paper += p.get_needed_wrapping_paper();
            tot_len_ribbon += p.get_needed_ribbon();
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    std::cout << "Part 1:" << std::endl;
    std::cout << "Answer: " << tot_area_paper << std::endl;
    std::cout << "Part 2:" << std::endl;
    std::cout << "Answer: " << tot_len_ribbon << std::endl;

    return 0;
}
