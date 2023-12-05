#include <array>
#include <fstream>
#include <iostream>
#include <ostream>
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

struct Map {
    unsigned long long destination;
    unsigned long long source;
    unsigned long long range;

    void print() { std::cout << "Destination: " << destination << ", Source: " << source << ", Range: " << range; };

    bool in_source_range(unsigned long long number) { return (number >= source && number < (source + range)); };

    unsigned long long convert(unsigned long long number) {
        // std::cout << "Converting: " << number;
        if (in_source_range(number)) {
            number += (destination - source);
            // std::cout << " is between: " << source << " and " << (source + range) << " -> " << number << std::endl;
            return number;
        }

        // std::cout << " No conversion" << std::endl;
        return number;
    };
};

struct Almanac {
    std::vector<unsigned long long> seeds;

    std::vector<Map> seed_to_soil;
    std::vector<Map> soil_to_fert;
    std::vector<Map> fert_to_water;
    std::vector<Map> water_to_light;
    std::vector<Map> light_to_temp;
    std::vector<Map> temp_to_hum;
    std::vector<Map> hum_to_location;

    unsigned long long convert_seed_to_soil(unsigned long long number) { return convert_map(number, seed_to_soil); };
    unsigned long long convert_soil_to_fert(unsigned long long number) { return convert_map(number, soil_to_fert); };
    unsigned long long convert_fert_to_water(unsigned long long number) { return convert_map(number, fert_to_water); };
    unsigned long long convert_water_to_light(unsigned long long number) { return convert_map(number, water_to_light); };
    unsigned long long convert_light_to_temp(unsigned long long number) { return convert_map(number, light_to_temp); };
    unsigned long long convert_temp_to_hum(unsigned long long number) { return convert_map(number, temp_to_hum); };
    unsigned long long convert_hum_to_location(unsigned long long number) { return convert_map(number, hum_to_location); };

    unsigned long long convert(unsigned long long number) {
        // std::cout << "Converting: " << number;
        // number = convert_seed_to_soil(number);
        // std::cout << " Soil: " << number;
        // number = convert_soil_to_fert(number);
        // std::cout << " Fertilizer: " << number;
        // number = convert_fert_to_water(number);
        // std::cout << " Water: " << number;
        // number = convert_water_to_light(number);
        // std::cout << " Light: " << number;
        // number = convert_light_to_temp(number);
        // std::cout << " Temperature: " << number;
        // number = convert_temp_to_hum(number);
        // std::cout << " Humidity: " << number;
        // number = convert_hum_to_location(number);
        // std::cout << " Location: " << number << std::endl;

        number = convert_seed_to_soil(number);
        number = convert_soil_to_fert(number);
        number = convert_fert_to_water(number);
        number = convert_water_to_light(number);
        number = convert_light_to_temp(number);
        number = convert_temp_to_hum(number);
        number = convert_hum_to_location(number);

        return number;
    };

  private:
    unsigned long long convert_map(unsigned long long number, std::vector<Map> m) {
        for (auto e : m) {
            if (e.in_source_range(number)) {
                return e.convert(number);
            }
        }

        return number;
    };
};

void parse_input(std::vector<std::string> str, Almanac &a);

int main(void) {
    std::ifstream text_input("../day05.txt");
    std::string input;
    std::vector<std::string> str;

    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            str.push_back(input);
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    // str = {
    //     "seeds: 79 14 55 13",
    //     "",
    //     "seed-to-soil map:",
    //     "50 98 2",
    //     "52 50 48",
    //     "",
    //     "soil-to-fertilizer map:",
    //     "0 15 37",
    //     "37 52 2",
    //     "39 0 15",
    //     "",
    //     "fertilizer-to-water map:",
    //     "49 53 8",
    //     "0 11 42",
    //     "42 0 7",
    //     "57 7 4",
    //     "",
    //     "water-to-light map:",
    //     "88 18 7",
    //     "18 25 70",
    //     "",
    //     "light-to-temperature map:",
    //     "45 77 23",
    //     "81 45 19",
    //     "68 64 13",
    //     "",
    //     "temperature-to-humidity map:",
    //     "0 69 1",
    //     "1 0 69",
    //     "",
    //     "humidity-to-location map:",
    //     "60 56 37",
    //     "56 93 4",
    // };

    Almanac a;
    parse_input(str, a);

    std::set<unsigned long long> locs;

    for (auto s : a.seeds) {
        locs.insert(a.convert(s));
    }

    std::cout << "Part 1\nAnswer: " << *locs.begin() << std::endl;

    // Use first seed start to init minimum loc
    unsigned long long minimum_loc = a.convert(a.seeds[0]);

    // Takes some 50 minutes to complete on my PC, should be a little refactored :D
    for (int i = 0; i < a.seeds.size(); i += 2) {
        std::cout << "First seed range" << std::endl;
        unsigned long long start = a.seeds[i];
        unsigned long long end = start + a.seeds[i + 1];

        for (unsigned long long seed = start; seed < end; seed++) {
            unsigned long long loc = a.convert(seed);
            if (loc < minimum_loc) {
                minimum_loc = loc;
            }
        }
    }

    std::cout << "Part 2\nAnswer: " << minimum_loc << std::endl;
}

void parse_input(std::vector<std::string> str, Almanac &a) {

    int idx = 0;
    // Read Seeds
    std::vector<std::string> seeds = resplit(str[idx].substr(7), std::regex(" +"));

    std::cout << "Seeds: ";
    for (auto s : seeds) {
        std::cout << s << ", ";
        a.seeds.push_back(std::stoull(s));
    }
    std::cout << std::endl;

    idx += 3;
    // Read seed-to-soil map
    std::cout << "Seed to Soil:" << std::endl;
    while (str[idx] != "") {
        std::vector<std::string> m = resplit(str[idx], std::regex(" +"));

        Map map;
        map.destination = std::stoull(m[0]);
        map.source = std::stoull(m[1]);
        map.range = std::stoull(m[2]);
        a.seed_to_soil.push_back(map);

        map.print();
        std::cout << std::endl;

        idx++;
    }
    idx += 2;

    // Read soil-to-fertilizer map
    std::cout << "Soil to Fertilizer:" << std::endl;
    while (str[idx] != "") {
        std::vector<std::string> m = resplit(str[idx], std::regex(" +"));

        Map map;
        map.destination = std::stoull(m[0]);
        map.source = std::stoull(m[1]);
        map.range = std::stoull(m[2]);
        a.soil_to_fert.push_back(map);

        map.print();
        std::cout << std::endl;

        idx++;
    }
    idx += 2;

    // Read fertilizer-to-water map
    std::cout << "Fertilizer to Water:" << std::endl;
    while (str[idx] != "") {
        std::vector<std::string> m = resplit(str[idx], std::regex(" +"));

        Map map;
        map.destination = std::stoull(m[0]);
        map.source = std::stoull(m[1]);
        map.range = std::stoull(m[2]);
        a.fert_to_water.push_back(map);

        map.print();
        std::cout << std::endl;

        idx++;
    }
    idx += 2;

    // Read water-to-light map
    std::cout << "Water to Light:" << std::endl;
    while (str[idx] != "") {
        std::vector<std::string> m = resplit(str[idx], std::regex(" +"));

        Map map;
        map.destination = std::stoull(m[0]);
        map.source = std::stoull(m[1]);
        map.range = std::stoull(m[2]);
        a.water_to_light.push_back(map);

        map.print();
        std::cout << std::endl;

        idx++;
    }
    idx += 2;

    // Read light_to_temp map
    std::cout << "Light to Temperature:" << std::endl;
    while (str[idx] != "") {
        std::vector<std::string> m = resplit(str[idx], std::regex(" +"));

        Map map;
        map.destination = std::stoull(m[0]);
        map.source = std::stoull(m[1]);
        map.range = std::stoull(m[2]);
        a.light_to_temp.push_back(map);

        map.print();
        std::cout << std::endl;

        idx++;
    }
    idx += 2;

    // Read temp_to_hum map
    std::cout << "Temperature to Humidity:" << std::endl;
    while (str[idx] != "") {
        std::vector<std::string> m = resplit(str[idx], std::regex(" +"));

        Map map;
        map.destination = std::stoull(m[0]);
        map.source = std::stoull(m[1]);
        map.range = std::stoull(m[2]);
        a.temp_to_hum.push_back(map);

        map.print();
        std::cout << std::endl;

        idx++;
    }
    idx += 2;

    // Read hum-to-loc map
    std::cout << "Humidity-to-location:" << std::endl;
    while (idx < str.size()) {
        std::vector<std::string> m = resplit(str[idx], std::regex(" +"));

        Map map;
        map.destination = std::stoull(m[0]);
        map.source = std::stoull(m[1]);
        map.range = std::stoull(m[2]);
        a.hum_to_location.push_back(map);

        map.print();
        std::cout << std::endl;

        idx++;
    }
}
