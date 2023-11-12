#include <cstdlib>
#include <fstream>
#include <functional>
#include <iostream>
#include <map>
#include <regex>
#include <set>
#include <string>
#include <vector>

int main(void) {
    std::ifstream text_input("../day10.txt");
    std::string input;

    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            std::cout << "Line: '" << input << "'" << std::endl;
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    // parse input into sequences

    std::regex re("1+|2+|3+|4+|5+|6+|7+|8+|9+");
    std::smatch match{};
    std::string s("1321131112");

    unsigned int p1{}, p2{};

    for (int i = 0; i < 50; i++) {
        std::cout << "Iteration: " << i + 1 << std::endl;
        std::string new_string{};
        while (std::regex_search(s, match, re)) {
            for (auto &m : match) {
                char c = m.str()[0];
                unsigned int cnt = m.str().size();

                new_string += std::to_string(cnt) + c;
            }
            s = match.suffix().str();
        }
        s = new_string;
        // std::cout << "After round: '" << s << "' len: " << s.size() << std::endl;

        if (i == 39) {
            p1 = s.size();
        }

        if (i == 49) {
            p2 = s.size();
        }
    }

    std::cout << "Part 1:\nAnswer: " << p1 << std::endl;
    std::cout << "Part 2:\nAnswer: " << p2 << std::endl;
}
