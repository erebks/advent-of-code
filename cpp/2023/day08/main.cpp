#include <array>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <ostream>
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

void parse_input(std::vector<std::string> str, std::map<std::string, std::array<std::string, 2>> &map, std::string &instructions) {
    instructions = str[0];

    str.erase(str.begin());

    for (auto s : str) {
        std::vector<std::string> v = resplit(s, std::regex(" = \\("));
        std::vector<std::string> w = resplit(v[1].substr(0, v[1].size() - 1), std::regex(", "));
        map.insert({v[0], {w[0], w[1]}});
    }
}

unsigned int part1(std::string const instructions, std::map<std::string, std::array<std::string, 2>> const map) {

    unsigned int steps = 0;
    std::string pos = "AAA";

    while (1) {
        for (auto i : instructions) {
            std::array<std::string, 2> neighbors = map.find(pos)->second;
            // std::cout << "At: " << pos << ", Next steps: " << neighbors[0] << ", " << neighbors[1] << std::endl;

            if (pos == "ZZZ") {
                // std::cout << "\tEnd found!" << std::endl;
                return steps;
            }

            switch (i) {
            case 'L':
                // std::cout << "\t Choosing L -> " << neighbors[0] << std::endl;
                pos = neighbors[0];
                steps++;
                break;

            case 'R':
                // std::cout << "\t Choosing R -> " << neighbors[1] << std::endl;
                pos = neighbors[1];
                steps++;
                break;
            default:
                // std::cout << "PROBLEM!" << std::endl;
                break;
            };
        }
    }
}

unsigned long long steps_till_end(std::string pos, std::string const instructions, std::map<std::string, std::array<std::string, 2>> const map) {
    unsigned long long steps = 0;

    while (1) {
        for (auto i : instructions) {
            std::array<std::string, 2> neighbors = map.find(pos)->second;
            // std::cout << "At: " << pos << ", Next steps: " << neighbors[0] << ", " << neighbors[1] << std::endl;

            if (pos[2] == 'Z') {
                // std::cout << "\tEnd found!" << std::endl;
                return steps;
            }

            switch (i) {
            case 'L':
                // std::cout << "\t Choosing L -> " << neighbors[0] << std::endl;
                pos = neighbors[0];
                steps++;
                break;

            case 'R':
                // std::cout << "\t Choosing R -> " << neighbors[1] << std::endl;
                pos = neighbors[1];
                steps++;
                break;
            default:
                // std::cout << "PROBLEM!" << std::endl;
                break;
            };
        }
    }
}

unsigned long long part2(std::string const instructions, std::map<std::string, std::array<std::string, 2>> const map) {

    // Find all nodes that END with A and calculate steps till end
    std::vector<unsigned long long> steps;

    for (auto it : map) {
        if (it.first[2] == 'A') {
            steps.push_back(steps_till_end(it.first, instructions, map));
            // std::cout << "Steps of " << it.first << ": " << *steps.rbegin() << std::endl;
        }
    }

    unsigned long long lcm = *steps.begin();
    for (auto it = steps.begin() + 1; it != steps.end(); it++) {
        // std::cout << "LCM(" << lcm;
        lcm = std::lcm(lcm, *it);
        // std::cout << ", " << *it << ") = " << lcm << std::endl;
    }

    // Now try to find smallest integer divisor
    return lcm;
}

int main(void) {
    std::ifstream text_input("../day08.txt");
    std::string input;
    std::vector<std::string> str;

    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            if (input != "")
                str.push_back(input);
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    // str.clear();
    // str = {
    //     "RL", "AAA = (BBB, CCC)", "BBB = (DDD, EEE)", "CCC = (ZZZ, GGG)", "DDD = (DDD, DDD)", "EEE = (EEE, EEE)", "GGG = (GGG, GGG)", "ZZZ = (ZZZ, ZZZ)",
    // };

    // str.clear();
    // str = {
    //     "LLR",
    //     "AAA = (BBB, BBB)",
    //     "BBB = (AAA, ZZZ)",
    //     "ZZZ = (ZZZ, ZZZ)",
    // };

    std::map<std::string, std::array<std::string, 2>> map;
    std::string instructions;
    parse_input(str, map, instructions);
    unsigned int p1_steps = part1(instructions, map);

    std::cout << "Part 1:\nAnswer: " << p1_steps << std::endl << std::endl;

    // str.clear();
    // map.clear();
    // instructions.clear();
    // str = {
    //     "LR",
    //     "11A = (11B, XXX)",
    //     "11B = (XXX, 11Z)",
    //     "11Z = (11B, XXX)",
    //     "22A = (22B, XXX)",
    //     "22B = (22C, 22C)",
    //     "22C = (22Z, 22Z)",
    //     "22Z = (22B, 22B)",
    //     "XXX = (XXX, XXX)",
    // };
    // parse_input(str, map, instructions);

    unsigned long long p2_steps = part2(instructions, map);
    std::cout << "Part 2:\nAnswer: " << p2_steps << std::endl << std::endl;
}
