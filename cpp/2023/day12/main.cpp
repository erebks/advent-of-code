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

bool is_arrangement_possible(std::string springs, std::string arrangement) {
    if (springs.size() != arrangement.size()) {
        std::cout << "Sizes don't match!" << std::endl;
        return false;
    }

    for (int i = 0; i < springs.size(); i++) {
        std::cout << springs[i] << " vs. " << arrangement[i] << std::endl;
        if ((springs[i] == '#' || springs[i] == '.') && arrangement[i] != springs[i]) {
            std::cout << "\tError in " << i << "th digit" << std::endl;
            return false;
        }
    }
    return true;
}

std::vector<std::string> generate_arrangement(std::string background, std::vector<std::string> groups, int index) {
    std::vector<std::string> arrangements;

    std::cout << "Background: " << background << " Index: " << index << std::endl;
    // Base case
    if (groups.size() == 0) {
        arrangements.push_back(background);
        return arrangements;
    }
    // Take next group
    std::string grp = groups.back();
    groups.pop_back();

    // Calculate how this group can be shifted
    std::string prefix;
    for (auto g : groups) {
        prefix += '.' + g;
    }

    for (int i = index; i < background.size() - prefix.size(); i++) {
        std::string arrangement = background.substr(0, i);
        arrangement += grp + '.';
        std::vector<std::string> a = generate_arrangement(arrangement, groups, arrangement.size() - 1);
        for (auto b : a) {
            arrangements.push_back(b);
        }
    }
    return arrangements;
}

int arrangements(std::string springs, std::vector<int> groups) {
    // Groups are seperated by '.' and consist only of '#'
    // '?' are either '.' or '#'

    std::string background;
    for (auto s : springs) {
        background += '.';
    }

    std::vector<std::string> spring_groups;

    for (int i1 = groups.size() - 1; i1 >= 0; i1++) {
        std::string grp;
        for (int i = 0; i < groups[i1]; i++) {
            grp += '#';
        }
        spring_groups.push_back(grp);
    }

    std::vector<std::string> arrangements = generate_arrangement(background, spring_groups, 0);

    for (auto a : arrangements) {
        std::cout << a << std::endl;
    }

    return arrangements.size();
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

    str = {
        "???.### 1,1,3", ".??..??...?##. 1,1,3", "?#?#?#?#?#?#?#? 1,3,1,6", "????.#...#... 4,1,1", "????.######..#####. 1,6,5", "?###???????? 3,2,1",
    };
    std::string springs;
    std::vector<int> groups;

    for (auto s : str) {
        parse(s, springs, groups);
        // arrangements(springs, groups);
    }

    arrangements(springs, groups);
}
