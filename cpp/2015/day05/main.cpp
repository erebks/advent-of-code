#include <algorithm>
#include <cstddef>
#include <fstream>
#include <iostream>
#include <iterator>
#include <ostream>
#include <regex>
#include <set>
#include <string>

bool part1_is_nice(std::string str) {

    // Does not contain ad, cd, pq, xy
    std::regex first_condition("(ab)|(cd)|(pq)|(xy)");
    std::smatch re_match{};

    if (std::regex_search(str, re_match, first_condition)) {
        std::cout << str << " failed first condition" << std::endl;
        return false;
    }

    // Contains at least 3 of aeiou

    std::regex second_condition("(a)|(e)|(i)|(o)|(u)");
    unsigned int occurances = std::distance(std::sregex_iterator(str.begin(), str.end(), second_condition), std::sregex_iterator());
    if (occurances < 3) {
        std::cout << str << " failed second condition" << std::endl;
        return false;
    }

    // Contains at least one double letter in a row (-> convert to a set and search for it)

    std::set<char> letters{};

    for (char const &c : str) {
        letters.insert(c);
    }

    for (char const &l : letters) {
        std::string re{std::string("(") + l + l + std::string(")")};
        std::regex third_condition(re);
        if (std::regex_search(str, re_match, third_condition)) {
            return true;
        }
    }

    std::cout << str << " failed third condition" << std::endl;
    return false;
};

bool part2_is_nice(std::string str) {

    std::smatch re_match{};
    // Contains a pair of letters twice (no overlap)

    bool first_condition_done = false;

    for (size_t i = 0; i + 1 < str.size(); i++) {
        std::string re{std::string("(") + str[i] + str[i + 1] + std::string(")")};
        std::regex first_condition(re);

        // Cut out
        std::string str_remainder = str.substr(i + 2);

        // std::cout << "Remainder: " << str_remainder << ", re: " << re << std::endl;

        unsigned int occurances = std::distance(std::sregex_iterator(str_remainder.begin(), str_remainder.end(), first_condition), std::sregex_iterator());

        if (occurances > 0) {
            // std::cout << str << " first condition ok" << std::endl;
            first_condition_done = true;
            break;
        }
    }

    if (!first_condition_done) {
        std::cout << str << " failed first condition" << std::endl;
        return false;
    }

    // Contains one letter twice with one letter in between

    std::set<char> letters{};

    for (char const &c : str) {
        letters.insert(c);
    }

    for (char const &l : letters) {
        std::string re{std::string("(") + l + std::string("[a-zA-Z]") + l + std::string(")")};
        std::regex second_condition(re);
        if (std::regex_search(str, re_match, second_condition)) {
            return true;
        }
    }

    std::cout << str << " failed second condition" << std::endl;
    return false;
};

int main(void) {
    std::ifstream text_input("../day04.txt");
    std::string input;
    unsigned int num_nice_strings_part1{0};
    unsigned int num_nice_strings_part2{0};

    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            if (part1_is_nice(input)) {
                num_nice_strings_part1++;
            }
            if (part2_is_nice(input)) {
                num_nice_strings_part2++;
            }
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    std::cout << "Part 1:" << std::endl;

    std::cout << "Answer: " << num_nice_strings_part1 << std::endl;

    std::string str{};
    bool res{};

    std::cout << "Part 2:" << std::endl;

    std::cout << "Answer: " << num_nice_strings_part2 << std::endl;
}
