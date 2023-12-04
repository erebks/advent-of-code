#include <cmath>
#include <fstream>
#include <iostream>
#include <map>
#include <regex>
#include <set>
#include <string>
#include <vector>

auto map_insert_or_inc(std::map<int, int> &m, int key) {
    auto it = m.find(key);

    if (it == m.end()) {
        m.insert({key, 1});
    } else {
        it->second++;
    }
    return it;
}

// number, times
std::map<int, int> prime_factorize(int number) {
    std::map<int, int> factors;

    while (number % 2 == 0) {
        auto it = factors.find(2);

        map_insert_or_inc(factors, 2);

        number /= 2;
    }

    for (int i = 3; i * i <= number; i += 2) {
        while ((number % i) == 0) {
            number = number / i;

            map_insert_or_inc(factors, i);
        }
    }

    if (number > 2) {
        map_insert_or_inc(factors, number);
    }

    return factors;
}

std::vector<int> recursive(std::map<int, int> factors) {

    int presents = 0;

    std::vector<int> good_name;

    // Take an element
    auto it = factors.begin();

    int factor = it->first;
    int power = it->second;

    // If last element
    if (factors.size() == 1) {
        for (int i = 0; i <= power; i++) {
            good_name.push_back(std::pow(factor, i));
        }
        return good_name;
    }

    // Delete element
    factors.erase(it);

    // Go deeper until only one is left
    good_name = recursive(factors);

    int size = good_name.size();

    for (int i = 0; i < size; i++) {

        for (int i2 = 1; i2 <= power; i2++) {
            good_name.push_back(good_name[i] * std::pow(factor, i2));
        }
    }
    return good_name;
}

int calculate_presents_p1(int house) {
    int presents = 0;

    std::map<int, int> factors = prime_factorize(house);

    // std::cout << "Factors of " << house << " ";
    // for (auto f : factors) {
    //     std::cout << f.first << "^" << f.second << ", ";
    // }

    std::vector<int> permut = recursive(factors);

    for (auto l : permut) {
        presents += l * 10;
    }

    // std::cout << "Presents: " << presents << std::endl;

    return presents;
}

int calculate_presents_p2(int house, std::map<int, int> &elfs_active, std::set<int> &elfs_done) {
    int presents = 0;

    std::map<int, int> factors = prime_factorize(house);

    // std::cout << "Factors of " << house << " ";
    // for (auto f : factors) {
    //     std::cout << f.first << "^" << f.second << ", ";
    // }

    std::vector<int> elfs = recursive(factors);

    // std::cout << "House: " << house << std::endl;
    for (auto elf : elfs) {
        // std::cout << "\tElf: " << elf << std::endl;

        if (elfs_done.find(elf) != elfs_done.end()) {
            // std::cout << "\t\tSkipping elf: " << elf << std::endl;
            continue;
        }

        auto it = map_insert_or_inc(elfs_active, elf);

        if (it->second >= 50) {
            // std::cout << "\t\tElf " << it->first << " is done" << std::endl;
            elfs_done.insert(it->first);
        }

        presents += elf * 11;
    }
    // std::cout << std::endl;

    // std::cout << "Presents: " << presents << std::endl;

    return presents;
}

int main(void) {
    std::ifstream text_input("../day20.txt");
    std::string input;
    int goal_presents;

    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            std::cout << "Line: '" << input << "'" << std::endl;
            goal_presents = std::stoi(input);
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    // You might need to adjust the upper value
    for (int i = 2; i <= 1000000; i++) {
        int presents = calculate_presents_p1(i);

        if (presents > goal_presents) {
            std::cout << "Part 1:\nAnswer: " << i << std::endl;
            break;
        }
    }

    // Elf # and how many visits
    std::map<int, int> elfs_active;
    std::set<int> elfs_done;

    elfs_active.insert({1, 1});

    // Needs to start at 2, you might need to adjust the upper value
    for (int i = 2; i <= 100000 * 10; i++) {
        int presents = calculate_presents_p2(i, elfs_active, elfs_done);

        if (presents > goal_presents) {
            std::cout << "Part 2:\nAnswer: " << i << std::endl;
            break;
        }
    }
}
