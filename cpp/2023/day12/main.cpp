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

void parse(std::string str, std::string &springs, std::vector<int> &groups) {
    std::vector<std::string> v = resplit(str, std::regex(" "));

    springs = v[0];
    v = resplit(v[1], std::regex(","));

    for (auto g : v) {
        groups.push_back(std::stoi(g));
    }
}

bool is_arrangement_valid(std::string arrangement, std::regex re) { return std::regex_match(arrangement, re); }

std::vector<std::string> recursive(std::string fixed, std::vector<int> unknowns) {
    std::vector<std::string> arrangements;

    if (unknowns.size() == 0) {
        arrangements.push_back(fixed);
        return arrangements;
    }

    // Next unknown
    int idx = unknowns.back();
    unknowns.pop_back();

    std::vector<std::string> a;

    fixed[idx] = '.';
    a = recursive(fixed, unknowns);

    for (auto b : a) {
        arrangements.push_back(b);
    }

    fixed[idx] = '#';
    a = recursive(fixed, unknowns);

    for (auto b : a) {
        arrangements.push_back(b);
    }

    return arrangements;
}

int arrangements(std::string springs, std::vector<int> groups) {
    // Groups are seperated by '.' and consist only of '#'
    // '?' are either '.' or '#'

    std::vector<int> unknowns;

    for (int i = 0; i < springs.size(); i++) {
        if (springs[i] == '?') {
            unknowns.push_back(i);
        }
    }

    std::vector<std::string> arrangements = recursive(springs, unknowns);
    int cnt = 0;

    std::string re = "\\.*";

    for (auto g : groups) {
        re += "#{" + std::to_string(g) + "}\\.+";
    }

    // Delete .+ at the back
    re = re.substr(0, re.size() - 3);
    re += "\\.*";

    for (auto a : arrangements) {
        // std::cout << "Arrangement: '" << a << "' ";
        if (is_arrangement_valid(a, std::regex(re))) {
            // std::cout << "VALID" << std::endl;
            cnt++;
        } else {
            // std::cout << "NOT VALID" << std::endl;
        }
    }

    return cnt;
}

int main(void) {
    std::ifstream text_input("../day12.txt");
    std::string input;

    std::vector<std::string> str;

    if (text_input.is_open()) {

        while (std::getline(text_input, input)) {
            std::cout << "Line: '" << input << "'" << std::endl;
            str.push_back(input);
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    // str = {
    //     "???.### 1,1,3", ".??..??...?##. 1,1,3", "?#?#?#?#?#?#?#? 1,3,1,6", "????.#...#... 4,1,1", "????.######..#####. 1,6,5", "?###???????? 3,2,1",
    // };

    int p1 = 0;
    for (auto s : str) {
        std::string springs;
        std::vector<int> groups;

        parse(s, springs, groups);
        p1 += arrangements(springs, groups);
    }

    std::cout << "Part 1:\nAnswer: " << p1 << std::endl << std::endl;
}
