#include <algorithm>
#include <array>
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

unsigned char hash(unsigned char val, char c) {
    unsigned int current = val + c;
    current *= 17;
    return current % 256;
}

struct Lense {
    std::string name;
    int focal_length = -1;

    void print() { std::cout << "[" << name << " " << focal_length << "]"; };

    unsigned char get_box() {
        unsigned char box = 0;
        for (auto c : name) {
            box = hash(box, c);
        }
        return box;
    };
};

struct Box {
    std::array<Lense, 9> slots;
    unsigned int end = 0;

    std::map<std::string, unsigned int> lenses;

    void addLense(Lense l) {
        auto it = lenses.find(l.name);
        if (it == lenses.end()) {
            // add
            slots[end] = l;
            lenses.insert({l.name, end});
            end++;
        } else {
            // update
            slots[it->second] = l;
        }
    }

    void delLense(Lense l) {
        auto it = lenses.find(l.name);
        if (it != lenses.end()) {
            unsigned int idx = it->second;
            // Now move every slot forward
            for (int i = idx + 1; i < end; i++) {
                auto x = lenses.find(slots[i].name);
                slots[i - 1] = slots[i];
                x->second = i - 1;
            }
            end--;
            lenses.erase(it);
        }
    }

    void print() {
        for (int i = 0; i < 9; i++) {
            std::cout << i << ": ";
            if (slots[i].name != "") {
                slots[i].print();
                std::cout << " ";
            }
            std::cout << ", ";
        }
    }
};

void print_boxes(std::array<Box, 256> boxes) {
    for (int i = 0; i < boxes.size(); i++) {
        if (boxes[i].end == 0)
            continue;
        std::cout << "Box " << i << ": ";
        boxes[i].print();
        std::cout << std::endl;
    }
}

int main(void) {
    std::ifstream text_input("../day15.txt");
    std::string input;

    std::vector<std::string> instructions;

    if (text_input.is_open()) {
        if (std::getline(text_input, input)) {
            instructions = resplit(input, std::regex(","));
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    // instructions = resplit("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7", std::regex(","));

    unsigned int p1 = 0;
    for (auto i : instructions) {
        unsigned char h = 0;
        for (auto c : i) {
            h = hash(h, c);
        }
        // std::cout << "Instuction '" << i << "' -> " << std::to_string(h) << "\n";
        p1 += h;
    }
    std::cout << "Part 1\nAnswer: " << std::to_string(p1) << "\n\n";

    // std::array<std::map<int, std::string>, 256> boxes;
    std::array<Box, 256> boxes;

    print_boxes(boxes);

    for (auto i : instructions) {
        // Determine if '-' or '='
        if (i.back() == '-') {
            Lense l;
            l.name = i.substr(0, i.size() - 1);

            // Get box
            unsigned char box = l.get_box();

            // remove lense if possible
            boxes[box].delLense(l);

        } else {
            std::vector<std::string> v = resplit(i, std::regex("="));
            Lense l;

            l.name = v[0];
            l.focal_length = std::stoi(v[1]);

            // Get box
            unsigned char box = l.get_box();

            boxes[box].addLense(l);
        }

        // std::cout << "After: " << i << std::endl;
        // print_boxes(boxes);
    }

    unsigned int p2 = 0;

    for (int i = 0; i < boxes.size(); i++) {
        for (int i1 = 0; i1 < boxes[i].end; i1++) {
            p2 += (i + 1) * (i1 + 1) * (boxes[i].slots[i1].focal_length);
        }
    }

    std::cout << "Part 2\nAnswer: " << std::to_string(p2) << "\n\n";
}
