#include <array>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
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

int main(void) {
    std::ifstream text_input("../day14.txt");
    std::string input;

    std::map<std::string, std::array<int, 3>> reindeers;

    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            std::cout << "Line: '" << input << "'" << std::endl;

            std::vector<std::string> line = resplit(input, std::regex(" "));

            std::string name = line[0];
            int speed = std::stoi(line[3]);
            int speed_duration = std::stoi(line[6]);
            int rest_duration = std::stoi(line[13]);

            std::cout << "Name: " << name << ", speed: " << speed << ", speed_duration: " << speed_duration << ", rest_duration: " << rest_duration
                      << std::endl;

            reindeers.insert({name, {speed, speed_duration, rest_duration}});
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    // reindeers = {{"Comet", {14, 10, 127}}, {"Dancer", {16, 11, 162}}};

    std::set<int> distances;

    int race_time = 2503;

    for (auto &reindeer : reindeers) {
        int cycle_time = reindeer.second[1] + reindeer.second[2];

        int tot_cycles = (int)race_time / cycle_time;
        int remainder = (int)race_time % cycle_time;
        int distance = 0;

        if (remainder < reindeer.second[2]) {
            distance = (tot_cycles + 1) * reindeer.second[1] * reindeer.second[0];
        } else {
            distance = tot_cycles * reindeer.second[1] * reindeer.second[0];
        }

        distances.insert(distance);
        std::cout << "After: " << race_time << "s, " << reindeer.first << " traveled: " << distance << std::endl;
    }

    std::cout << "Part 1:\nAnswer: " << *distances.rbegin() << std::endl << std::endl;

    // 2720 too high
}
