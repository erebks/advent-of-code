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

int get_distance(std::string name, std::array<int, 4> dat, int time) {
    int cycle_time = dat[1] + dat[2];

    int tot_cycles = (int)time / cycle_time;
    int remainder = (int)time % cycle_time;
    int distance = 0;

    distance = tot_cycles * dat[1] * dat[0];

    if (remainder <= dat[1]) {
        distance += remainder * dat[0];
    } else {
        distance += dat[1] * dat[0];
    }

    return distance;
}

int main(void) {
    std::ifstream text_input("../day14.txt");
    std::string input;

    std::map<std::string, std::array<int, 4>> reindeers;

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
        int distance = get_distance(reindeer.first, reindeer.second, race_time);

        distances.insert(distance);
        // std::cout << "After: " << race_time << "s, " << reindeer.first << " traveled: " << distance << std::endl;
    }

    std::cout << "Part 1:\nAnswer: " << *distances.rbegin() << std::endl << std::endl;

    int winning_distance = 0;

    for (int time = 1; time <= race_time; time++) {
        std::map<std::string, int> distances;
        int max_distance = 0;
        for (auto &reindeer : reindeers) {
            int distance = get_distance(reindeer.first, reindeer.second, time);

            distances.insert({reindeer.first, distance});
            // std::cout << "After: " << time << "s, " << reindeer.first << " traveled: " << distance << std::endl;
            if (distance > max_distance) {
                max_distance = distance;
            }
        }

        // Iterate over all reindeers and assign points
        for (auto &dist : distances) {
            if (dist.second == max_distance) {
                // std::cout << "At: " << time << "s " << dist.first << " wins and gets a point" << std::endl;
                auto r = reindeers.find(dist.first);
                r->second[3]++;
                if (r->second[3] > winning_distance) {
                    winning_distance = r->second[3];
                }
            }
        }
    }

    std::cout << "Part 2:\nAnswer: " << winning_distance << std::endl << std::endl;
}
