#include <fstream>
#include <iostream>
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

std::string roll_left(std::string line) {
    // Roll all the 'O' up as far as possible

    std::string l;

    int free_spot = 0;
    for (int i = 0; i < line.size(); i++) {
        switch (line[i]) {
        case '.':
            l += '.';
            break;

        case '#':
            l += '#';
            free_spot = i + 1;
            break;

        case 'O':
            l += '.';
            l[free_spot++] = 'O';
            break;

        default:
            break;
        };
        // std::cout << l << std::endl;
    }

    return l;
}

std::vector<std::string> transponse(std::vector<std::string> platform) {
    std::vector<std::string> t_platform{};

    for (int col = 0; col < platform[0].size(); col++) {
        std::string l{};
        for (int row = 0; row < platform.size(); row++) {
            l += platform[row][col];
        }
        t_platform.push_back(l);
    }

    return t_platform;
}

std::vector<std::string> tilt(std::vector<std::string> platform, char axis = 'N') {
    std::vector<std::string> transonded;
    std::vector<std::string> p;

    switch (axis) {
    case 'N':
        transonded = transponse(platform);
        transonded = transponse(transonded);
        transonded = transponse(transonded);

        for (auto s : transonded) {
            std::cout << s << " -> ";
            p.push_back(roll_left(s));
            std::cout << p.back() << std::endl;
        }

        p = transponse(p);

        break;
    case 'E':
        break;
    case 'S':
        break;
    case 'W':
        break;
    default:
        break;
    };

    return p;
}

int load(std::vector<std::string> platform) {
    int l = 0;
    for (int row = 0; row < platform.size(); row++) {
        int stones = 0;
        for (auto c : platform[row]) {
            if (c == 'O')
                stones++;
        }
        l += stones * (platform.size() - row);
    }
    return l;
}

int main(void) {
    std::ifstream text_input("../day14.txt");
    std::string input;

    std::vector<std::string> platform;

    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            std::cout << "Line: '" << input << "'" << std::endl;
            platform.push_back(input);
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    // platform = {
    //     "O....#....", "O.OO#....#", ".....##...", "OO.#O....O", ".O.....O#.", "O.#..O.#.#", "..O..#O..O", ".......O..", "#....###..", "#OO..#....",
    // };

    std::vector<std::string> tilted = tilt(platform);
    int l = load(tilted);

    std::cout << "Part 1\nAnswer: " << l << std::endl << std::endl;
}
