#include <array>
#include <fstream>
#include <iostream>
#include <string>

// Hat-tip to https://stackoverflow.com/a/28142357
#include <regex>
#include <type_traits>
#include <vector>
std::vector<std::string> resplit(const std::string &s, const std::regex &sep_regex = std::regex{"\\s+"}) {
    std::sregex_token_iterator iter(s.begin(), s.end(), sep_regex, -1);
    std::sregex_token_iterator end;
    return {iter, end};
}

struct Crucible {
    std::array<unsigned int, 2> pos;

    unsigned int straight_steps = 0; // Maximum of 3
    std::vector<std::array<unsigned int, 2>> visited;

    std::string str() { return "At (" + std::to_string(pos[0]) + ", " + std::to_string(pos[1]) + ")"; };
    void print() { std::cout << this->str() << std::endl; };
};

Crucible step(std::vector<std::string> const map, Crucible c) { return c; }

void print_map(std::vector<std::string> map, Crucible c) {
    for (auto pos : c.visited) {
        map[pos[0]][pos[1]] = '#';
    }

    for (auto line : map) {
        std::cout << line << std::endl;
    }
}

int main(void) {
    std::ifstream text_input("../day17.txt");
    std::string input;

    std::vector<std::string> map;

    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            map.push_back(input);
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    map = {
        "2413432311323", "3215453535623", "3255245654254", "3446585845452", "4546657867536", "1438598798454", "4457876987766",
        "3637877979653", "4654967986887", "4564679986453", "1224686865563", "2546548887735", "4322674655533",
    };

    Crucible cart;

    print_map(map, cart);
}
