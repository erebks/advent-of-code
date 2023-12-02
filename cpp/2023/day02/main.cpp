#include <array>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <vector>

// Hat-tip to https://stackoverflow.com/a/28142357
#include <regex>
#include <vector>
std::vector<std::string> resplit(const std::string &s, const std::regex &sep_regex = std::regex{"\\s+"}) {
    std::sregex_token_iterator iter(s.begin(), s.end(), sep_regex, -1);
    std::sregex_token_iterator end;
    return {iter, end};
}

struct Game {
    int id;
    // red, green, blue
    std::vector<std::array<int, 3>> rounds;

    Game(){};
};

Game *parse_input(std::string input) {
    std::vector<std::string> split_colon = resplit(input, std::regex(":"));

    std::vector<std::string> split_semi = resplit(split_colon[1], std::regex(";"));

    Game *g = new Game;

    g->id = std::stoi(split_colon[0].substr(4, split_colon[0].size() - 2));

    for (auto s : split_semi) {
        s = std::regex_replace(s, std::regex(","), "");
        std::vector<std::string> split_whitespace = resplit(s.substr(1), std::regex(" "));

        std::array<int, 3> round = {0, 0, 0};

        for (auto it = split_whitespace.begin(); it != split_whitespace.end(); it += 2) {
            if (*(it + 1) == "red") {
                round[0] = std::stoi(*it);
            }
            if (*(it + 1) == "green") {
                round[1] = std::stoi(*it);
            }
            if (*(it + 1) == "blue") {
                round[2] = std::stoi(*it);
            }
        }
        g->rounds.push_back(round);
    }
    return g;
}

bool game_valid(Game *game) {

    const int max_red = 12;
    const int max_green = 13;
    const int max_blue = 14;

    // std::cout << "\tGame: " << game->id << std::endl;

    for (auto r : game->rounds) {
        // std::cout << "\tRound: Red: " << r[0] << ", Green: " << r[1] << ", Blue: " << r[2] << std::endl;

        int red = r[0];
        int green = r[1];
        int blue = r[2];

        if (red > max_red) {
            return false;
        }

        if (green > max_green) {
            return false;
        }

        if (blue > max_blue) {
            return false;
        }
    }
    return true;
}

int main(void) {
    std::ifstream text_input("../day02.txt");
    std::string input;

    std::vector<Game *> games;

    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            std::cout << "Line: '" << input << "'" << std::endl;

            Game *g = parse_input(input);
            games.push_back(g);
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    // // Free the games
    // for (auto g : games) {
    //     free(g);
    // }
    // games.clear();
    // games.push_back(parse_input("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"));
    // games.push_back(parse_input("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue"));
    // games.push_back(parse_input("Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red"));
    // games.push_back(parse_input("Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red"));
    // games.push_back(parse_input("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"));

    // Part 1, check if possible

    int num = 0;
    for (auto g : games) {
        if (!game_valid(g)) {
            // std::cout << "Game: " << g->id << " NOT VAILD" << std::endl;
        } else {
            // std::cout << "Game: " << g->id << " VAILD" << std::endl;
            num += g->id;
        }
    }

    std::cout << "Part 1:\nAnswer: " << num << std::endl << std::endl;

    // Part 2, find miniums
    num = 0;
    for (auto g : games) {
        int max_red = 0;
        int max_green = 0;
        int max_blue = 0;

        int power = 0;

        // std::cout << "Game: " << g->id << std::endl;

        for (auto r : g->rounds) {
            // std::cout << "\tRound: Red: " << r[0] << ", Green: " << r[1] << ", Blue: " << r[2] << std::endl;

            int red = r[0];
            int green = r[1];
            int blue = r[2];

            if (red > max_red) {
                max_red = red;
            }

            if (green > max_green) {
                max_green = green;
            }

            if (blue > max_blue) {
                max_blue = blue;
            }
        }
        power = max_red * max_blue * max_green;

        // std::cout << "Max Red: " << max_red << ", Max Blue: " << max_blue << ", Max Green: " << max_green << ", Power: " << power << std::endl;
        num += power;
    }

    std::cout << "Part 2:\nAnswer: " << num << std::endl << std::endl;

    // Free the games
    for (auto g : games) {
        free(g);
    }
}
