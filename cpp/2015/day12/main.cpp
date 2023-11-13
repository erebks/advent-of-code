#include "json.hpp"
#include <cstdarg>
#include <fstream>
#include <iostream>
#include <regex>
#include <string>

// for convenience
using json = nlohmann::json;

bool is_valid(json &j) {
    std::cout << "Working on: " << j << std::endl;
    for (auto &e : j) {
        if (e.is_array()) {
            // std::cout << e << "\n\t->Is Array" << std::endl;
            is_valid(e);
        } else if (e.is_object()) {
            // std::cout << e << "\n\t->Is Object" << std::endl;
            if (!is_valid(e)) {
                std::cout << "Deleting: " << e << std::endl;
                e = {};
            }
        } else if (e.is_string()) {
            if (e == "red" && j.is_object()) {
                // std::cout << "\n\t\t->Is invalid!!" << std::endl;
                return false;
            }
        } else {
            continue;
        }
    }

    return true;
}

int main(void) {
    std::ifstream text_input("../day12.txt");
    std::string input;

    if (text_input.is_open()) {
        if (std::getline(text_input, input)) {
            std::cout << "Line: '" << input << "'" << std::endl;
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    //    input = "{\"a\":2,\"b\":4}";

    // Part1: Find all numbers and add together
    unsigned int sum = 0;

    std::regex re("(-?|\\+?)\\d+");
    std::smatch match{};

    for (std::string inner(input); std::regex_search(inner, match, re); inner = match.suffix().str()) {
        std::cout << "Match: " << match.str() << std::endl;
        sum += std::stoi(match.str());
    }

    std::cout << "Part 1:\nAnswer: " << sum << std::endl;

    // input = "[1,\"red\",5]";
    // input = "{\"d\":\"red\",\"e\":[1,2,3,4],\"f\":5}";
    // input = "[1,{\"c\":\"red\",\"b\":2},3]";

    json j = json::parse(input);

    bool valid = is_valid(j);

    std::cout << "Is valid?: " << valid << std::endl;

    // Part1: Find all numbers and add together
    sum = 0;

    if (valid) {
        for (std::string inner(j.dump()); std::regex_search(inner, match, re); inner = match.suffix().str()) {
            sum += std::stoi(match.str());
        }
    }

    std::cout << "Part 2:\nAnswer: " << sum << std::endl;
}
