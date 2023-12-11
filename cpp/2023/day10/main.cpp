#include <array>
#include <cstddef>
#include <fstream>
#include <iostream>
#include <ostream>
#include <stdexcept>
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

std::array<int, 2> find_start(std::vector<std::string> map) {
    // Find 'S'

    std::array<int, 2> start({0, 0});

    for (auto line : map) {
        for (auto pipe : line) {
            if (pipe == 'S') {
                return start;
            }
            start[1]++;
        }
        start[1] = 0;
        start[0]++;
    }

    return {-1, -1};
}

std::array<int, 2> step(std::vector<std::string> map, std::array<int, 2> prev, std::array<int, 2> pos) {
    char pipe = map[pos[0]][pos[1]];

    std::cout << "@pos " << pos[0] << ", " << pos[1] << " -> " << pipe << " prev: " << prev[0] << ", " << prev[1] << std::endl;

    std::array<int, 2> delta;
    std::array<int, 2> alt_delta;

    switch (pipe) {
    case '|':
        delta = {1, 0};
        alt_delta = {-1, 0};
        break;
    case '-':
        delta = {0, 1};
        alt_delta = {0, -1};
        break;
    case 'L':
        delta = {0, 1};
        alt_delta = {-1, 0};
        break;
    case 'J':
        delta = {0, -1};
        alt_delta = {-1, 0};
        break;
    case '7':
        delta = {0, -1};
        alt_delta = {1, 0};
        break;
    case 'F':
        delta = {0, 1};
        alt_delta = {1, 0};
        break;
    case '.':
        std::cout << "PROBLEM!!!!";
        return {-1, -1};
    };

    if (prev[0] < 0 || prev[1] < 0) {
        pos[0] += delta[0];
        pos[1] += delta[1];
        return pos;
    }

    // Try delta
    if (pos[0] + delta[0] == prev[0] && pos[1] + delta[1] == prev[1]) {
        std::cout << "Delta is prev!" << std::endl;
        if (pos[0] + alt_delta[0] == prev[0] && pos[1] + alt_delta[1] == prev[1]) {
            std::cout << "Altdelta is also prev!" << std::endl;
            return {-1, -1};
        } else {
            pos[0] += alt_delta[0];
            pos[1] += alt_delta[1];
            return pos;
        }

    } else {
        pos[0] += delta[0];
        pos[1] += delta[1];
        return pos;
    }
}

std::vector<std::array<int, 2>> find_loop(std::vector<std::string> map, char &start_char) {
    // This is really ugly...

    std::cout << "Map:" << std::endl;
    for (auto line : map) {
        std::cout << line << std::endl;
    }
    std::cout << std::endl;
    std::array<int, 2> start = find_start(map);

    std::cout << "Start: " << start[0] << ", " << start[1] << std::endl;

    // Assume start is either '|', '-', 'L', 'J', '7', 'F' and try to find loop

    std::string start_pipes = "|-LJ7F";

    std::vector<std::array<int, 2>> loop;

    for (char c : start_pipes) {
        loop.clear();

        std::array<int, 2> pos(start);
        std::array<int, 2> prev({-1, -1});
        map[start[0]][start[1]] = c;
        int i;

        for (i = 0; i < 1000000; i++) {
            std::array<int, 2> p = step(map, prev, pos);

            if (p[0] < 0 || p[1] < 0) {
                std::cout << "Invalid!" << std::endl;
                break;
            }

            if (p == start) {
                std::cout << "Start found!" << std::endl;
                std::cout << "Using: '" << c << "' Length: " << i;
                // Check if start pipe makes sense

                std::array<int, 2> x = step(map, loop[1], start);

                if (x == pos) {
                    std::cout << "Start fits!" << std::endl;
                    start_char = c;
                    loop.push_back(pos);
                    return loop;
                    break;

                } else {
                    std::cout << "Start doesn't fit!" << std::endl;
                    break;
                }
            }

            loop.push_back(pos);
            prev = pos;
            pos = p;
        }
    }
    return {};
}

int main(void) {
    std::ifstream text_input("../day10.txt");
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

    // map.clear();
    // map = {
    //     ".....", ".S-7.", ".|.|.", ".L-J.", ".....",
    // };
    // map = {
    //     "-L|F7", "7S-7|", "L|7||", "-L-J|", "L|-JF",
    // };
    // map = {
    //     "7-F7-", ".FJ|7", "SJLL7", "|F--J", "LJ.LJ",
    // };

    char start_char;
    std::vector<std::array<int, 2>> loop = find_loop(map, start_char);

    std::cout << "Length: " << loop.size() << std::endl;
    std::cout << "Part 1\nAnswer: " << (loop.size() + 1) / 2 << std::endl << std::endl;

    // map.clear();

    // map = {
    //     "...........", ".S-------7.", ".|F-----7|.", ".||.....||.", ".||.....||.", ".|L-7.F-J|.", ".|..|.|..|.", ".L--J.L--J.", "...........",
    // };

    // map = {
    //     ".F----7F7F7F7F-7....", ".|F--7||||||||FJ....", ".||.FJ||||||||L7....", "FJL7L7LJLJ||LJ.L-7..", "L--J.L7...LJS7F-7L7.",
    //     "....F-J..F7FJ|L7L7L7", "....L7.F7||L7|.L7L7|", ".....|FJLJ|FJ|F7|.LJ", "....FJL-7.||.||||...", "....L---J.LJ.LJLJ...",
    // };

    // map = {
    //     "FF7FSF7F7F7F7F7F---7", "L|LJ||||||||||||F--J", "FL-7LJLJ||||||LJL-77", "F--JF--7||LJLJ7F7FJ-", "L---JF-JLJ.||-FJLJJ7",
    //     "|F|F-JF---7F7-L7L|7|", "|FFJF7L7F-JF7|JL---7", "7-L-JL7||F7|L7F-7F7|", "L.L7LFJ|||||FJL7||LJ", "L7JLJL-JLJLJL--JLJ.L",
    // };

    // loop = find_loop(map, start_char);

    std::array<int, 2> start = find_start(map);

    map[start[0]][start[1]] = start_char;

    // Delete all pipes that aren't on loop

    std::vector<std::string> cleared_map;

    for (int i = 0; i < map.size(); i++) {
        std::string line{};

        for (auto c : map[0]) {
            line += ".";
        }
        cleared_map.push_back(line);
    }

    for (auto pos : loop) {
        cleared_map[pos[0]][pos[1]] = map[pos[0]][pos[1]];
    }

    // For every '.' -> check N, E, S, W to see if there's an odd amout of pipes

    bool inside = false;
    bool on_pipe = false;
    char last_edge;
    int tiles = 0;
    for (int line = 0; line < cleared_map.size(); line++) {
        inside = false;
        on_pipe = false;
        for (int c = 0; c < cleared_map[0].size(); c++) {
            char p = cleared_map[line][c];

            if (p == '|') {
                inside = !inside;
                // std::cout << p;
                continue;
            }

            if (p == 'J') {
                if (last_edge == 'F') {
                    inside = !inside;
                }
                last_edge = ' ';
                // std::cout << p;
                continue;
            }

            if (p == '7') {
                if (last_edge == 'L') {
                    inside = !inside;
                }
                last_edge = ' ';
                // std::cout << p;
                continue;
            }

            if (p == '-') {
                // std::cout << p;
                continue;
            }

            if (p == 'F' || p == 'L') {
                last_edge = p;
                // std::cout << p;
                continue;
            }

            if (p == '.' && inside) {
                // std::cout << "I";
                tiles++;
                continue;
            }

            if (p == '.' && !inside) {
                // std::cout << "O";
                continue;
            }
        }
        // std::cout << std::endl;
    }

    std::cout << "Part 2\nAnswer: " << tiles << std::endl << std::endl;
}
