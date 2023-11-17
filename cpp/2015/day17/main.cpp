#include <algorithm>
#include <fstream>
#include <functional>
#include <iostream>
#include <map>
#include <string>
#include <vector>

std::map<int, int> recursive(int liters, int depth, std::vector<int>::iterator begin, std::vector<int>::iterator end) {
    std::cout << "Iteration, liters: " << liters << std::endl;

    std::map<int, int> hits;
    // find the entry which might fit the liters

    for (auto it = begin; it != end; it++) {
        int b = *it;

        int liters_left = liters - b;

        std::cout << "Using bucket with: " << b << " -> now we have " << liters_left << " liters left";

        if (liters_left > 0) {
            // Need to go deeper
            std::cout << " -> Going deeper" << std::endl;
            std::map<int, int> ret = recursive(liters_left, depth + 1, it + 1, end);

            for (auto r : ret) {
                auto h = hits.find(r.first);
                if (h == hits.end()) {
                    hits.insert(r);
                } else {
                    h->second += r.second;
                }
            }

        } else if (liters_left == 0) {
            // Perfect fit
            std::cout << " -> Perfect fit" << std::endl;
            auto h = hits.find(depth);
            if (h == hits.end()) {
                hits.insert({depth, 1});
            } else {
                h->second++;
            }
        } else {
            // Unperfect fit
            std::cout << " -> Unperfect fit" << std::endl;
        }
    }

    return hits;
}

int main(void) {
    std::ifstream text_input("../day17.txt");
    std::string input;

    std::vector<int> buckets;

    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            buckets.push_back(std::stoi(input));
        }

        std::sort(buckets.begin(), buckets.end(), std::greater<int>());

        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    int liters_eggnog = 150;

    // buckets.clear();
    // buckets = {20, 15, 10, 5, 5};
    // liters_eggnog = 25;

    std::map<int, int> possibilities = recursive(liters_eggnog, 0, buckets.begin(), buckets.end());

    int p1 = 0;
    for (auto p : possibilities) {
        std::cout << "#Buckets: " << p.first << " #Cnt: " << p.second << std::endl;
        p1 += p.second;
    }

    std::cout << "\nPart 1:\nAnswer: " << p1 << std::endl << std::endl;

    std::cout << "\nPart 2:\nAnswer: " << possibilities.begin()->second << std::endl << std::endl;
}
