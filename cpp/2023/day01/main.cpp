#include <fstream>
#include <iostream>
#include <map>
#include <regex>
#include <string>
#include <vector>

std::string find_first_digit(std::string string) {
    std::map<std::string, int> replaces = {{"one", 1}, {"two", 2}, {"three", 3}, {"four", 4}, {"five", 5}, {"six", 6}, {"seven", 7}, {"eight", 8}, {"nine", 9}};

    // std::cout << "string: " << string << std::endl;

    for (int i = 0; i < string.size(); i++) {
        std::string subs = string.substr(0, i + 1);
        // std::cout << "\tSubstring: " << subs << std::endl;

        char digit(string[i]);

        if (digit >= '0' && digit <= '9') {
            // std::cout << "\tDigit found via direct match! " << digit << std::endl;
            std::string dig{digit};
            return dig;
        }

        for (auto re : replaces) {
            std::string after = std::regex_replace(subs, std::regex(re.first), std::to_string(re.second));
            digit = after[after.size() - 1];
            if (digit >= '0' && digit <= '9') {
                // std::cout << "\tDigit found via replace! " << digit << std::endl;
                std::string dig{digit};
                return dig;
            }
        }
    }
    return "";
}

std::string find_last_digit(std::string string) {
    std::map<std::string, int> replaces = {{"one", 1}, {"two", 2}, {"three", 3}, {"four", 4}, {"five", 5}, {"six", 6}, {"seven", 7}, {"eight", 8}, {"nine", 9}};

    // std::cout << "string: " << string << std::endl;

    for (int i = string.size() - 1; i >= 0; i--) {
        std::string subs = string.substr(i, string.size());
        // std::cout << "\tSubstring: " << subs << std::endl;

        char digit(string[i]);

        if (digit >= '0' && digit <= '9') {
            // std::cout << "\tDigit found via direct match! " << digit << std::endl;
            std::string dig{digit};
            return dig;
        }

        for (auto re : replaces) {
            std::string after = std::regex_replace(subs, std::regex(re.first), std::to_string(re.second));
            digit = after[0];
            if (digit >= '0' && digit <= '9') {
                // std::cout << "\tDigit found via replace! " << digit << std::endl;
                std::string dig{digit};
                return dig;
            }
        }
    }
    return "";
}

int main(void) {
    std::ifstream text_input("../day01.txt");
    std::vector<std::string> v;
    std::string input;

    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            std::cout << "Line: '" << input << "'" << std::endl;
            v.push_back(input);
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    // Part 1
    std::string first_digit;
    std::string last_digit;
    int p1 = 0;

    for (auto s : v) {
        for (auto c : s) {
            if (c >= '0' && c <= '9') {
                first_digit = c;
                break;
            }
        }
        for (auto c = s.rbegin(); c != s.rend(); c++) {
            if (*c >= '0' && *c <= '9') {
                last_digit = *c;
                break;
            }
        }
        int num = std::stoi(first_digit + last_digit);
        // std::cout << "Input: " << s << ", first: " << first_digit << ", last: " << last_digit << ", num: " << num << std::endl;
        p1 += num;
    }
    std::cout << "Part 1\nAnswer: " << p1 << std::endl << std::endl;

    // v = {"two1nine",         // 29
    //      "eightwothree",     // 83
    //      "abcone2threexyz",  // 13
    //      "xtwone3four",      // 24
    //      "4nineeightseven2", // 42
    //      "zoneight234",      // 14
    //      "7pqrstsixteen"};   // 76

    // Part 2
    int p2 = 0;
    for (auto s : v) {

        first_digit = find_first_digit(s);
        last_digit = find_last_digit(s);

        int num = std::stoi(first_digit + last_digit);
        // std::cout << "Input: " << s << ", first: " << first_digit << ", last: " << last_digit << ", num: " << num << std::endl;
        p2 += num;
    }
    std::cout << "Part 2\nAnswer: " << p2 << std::endl << std::endl;
}
