#include <cmath>
#include <fstream>
#include <iostream>
#include <string>

// Hat-tip to https://stackoverflow.com/a/28142357
#include <regex>
#include <vector>
std::vector<std::string> resplit(const std::string &s, const std::regex &sep_regex = std::regex{"\\s+"}) {
    std::sregex_token_iterator iter(s.begin(), s.end(), sep_regex, -1);
    std::sregex_token_iterator end;
    return {iter, end};
}

int main(void) {
    std::ifstream text_input("../day06.txt");
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

    // str = {"Time:      7  15   30", "Distance:  9  40  200"};

    std::vector<int> times;
    std::vector<int> distance_records;

    // Variables for part2
    std::string p2_time("");
    std::string p2_distance("");

    std::vector<std::string> str_time = resplit(str[0], std::regex(" +"));
    std::vector<std::string> str_dist = resplit(str[1], std::regex(" +"));

    for (int i = 1; i < str_time.size(); i++) {
        times.push_back(std::stoi(str_time[i]));
        p2_time += str_time[i];

        distance_records.push_back(std::stoi(str_dist[i]));
        p2_distance += str_dist[i];
    }

    int ways_to_beat = 1;

    for (int it = 0; it < times.size(); it++) {
        int time = times[it];
        double distance = distance_records[it] + 0.1;
        double hold_time_1 = 0.5 * (time + std::sqrt(time * time - 4 * distance));
        double hold_time_2 = 0.5 * (time - std::sqrt(time * time - 4 * distance));

        if (hold_time_1 > 0 && hold_time_2 > 0) {
            ways_to_beat = ways_to_beat * (std::ceil(hold_time_1) - std::ceil(hold_time_2));
        } else {
            std::cout << "Problem!!!" << std::endl;
        }
    }

    std::cout << "Part 1:\nAnswer: " << ways_to_beat << std::endl;

    // Part 2 join all the numbers
    unsigned long time = std::stoul(p2_time);
    double distance = std::stoul(p2_distance) + 0.1;

    double hold_time_1 = 0.5 * (time + std::sqrt(time * time - 4 * distance));
    double hold_time_2 = 0.5 * (time - std::sqrt(time * time - 4 * distance));

    std::cout << "Part 2:\nAnswer: " << (unsigned int)(std::ceil(hold_time_1) - std::ceil(hold_time_2));
}
