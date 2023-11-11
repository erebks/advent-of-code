#include <cstdint>
#include <cstdio>
#include <fstream>
#include <iostream>
#include <string>

#include <regex>
#include <set>
#include <string>
#include <vector>

// Hat-tip to https://stackoverflow.com/a/28142357
std::vector<std::string> resplit(const std::string &s, const std::regex &sep_regex = std::regex{"\\s+"}) {
    std::sregex_token_iterator iter(s.begin(), s.end(), sep_regex, -1);
    std::sregex_token_iterator end;
    return {iter, end};
}

// y
// ^
// |       (x,MAX)
// x---------------------x (MAX,MAX)
// | (0,MAX)             |
// |                     |
// | (0,y)               | (MAX,y)
// |                     |
// |                     |
// x---------------------x---> x
// (0,0)    (x,0)        (MAX,0)
//
// turn on 0,0 through 999,999
// Turns on EVERY light
//
// toggle 0,0 through 999,0
// Toggles first LINE (ROW) to off
//
// turn off 499,499 through 500,500
// Turns off middle four lights

struct Rectangle {
    unsigned int x_start{};
    unsigned int x_end{};
    unsigned int y_start{};
    unsigned int y_end{};

    Rectangle(){};
    Rectangle(std::string s1, std::string s2) {
        // x,y through x,y
        // Get rid of ' through ' and get those precious x and y values
        // Order both x values and assign x_start and x_end accordingly

        unsigned int x_vals[2], y_vals[2];

        std::sscanf(s1.c_str(), "%d,%d", &x_vals[0], &y_vals[0]);
        std::sscanf(s2.c_str(), "%d,%d", &x_vals[1], &y_vals[1]);

        if (x_vals[1] > x_vals[0]) {
            x_start = x_vals[0];
            x_end = x_vals[1];
        } else {
            x_start = x_vals[1];
            x_end = x_vals[0];
        }

        if (y_vals[1] > y_vals[0]) {
            y_start = y_vals[0];
            y_end = y_vals[1];
        } else {
            y_start = y_vals[1];
            y_end = y_vals[0];
        }
    };

    Rectangle(unsigned int x_start, unsigned int x_end, unsigned int y_start, unsigned int y_end)
        : x_start(x_start), x_end(x_end), y_start(y_start), y_end(y_end){};

    bool is_point_inside(unsigned int x, unsigned int y) {
        if (x >= x_start && x <= x_end && y >= y_start && y <= y_end) {
            return true;
        }
        return false;
    };

    unsigned int area() { return ((x_end - x_start) + 1) * ((y_end - y_start) + 1); };
};

enum Instructions { ON, OFF, TOGGLE };

struct Instruction {
    Rectangle r{};
    Instructions inst{};

    Instruction(){};

    Instruction(std::string str) {

        if (str.find("turn on") != -1) {
            inst = ON;
        } else if (str.find("turn off") != -1) {
            inst = OFF;
        } else if (str.find("toggle") != -1) {
            inst = TOGGLE;
        } else {
            std::cout << "Problem!!!" << std::endl;
        }

        // turn off 446,432 through 458,648
        std::vector<std::string> v = resplit(str, std::regex{" "});

        r = Rectangle(*(v.rbegin()), *(v.rbegin() + 2));

        // INSTRUCTION -> Rectangle
    }
};

bool is_finally_lit(unsigned int x, unsigned int y, std::vector<Instruction> *inst) {
    bool pixel = false;
    // Traverse until instruction found
    for (auto it = inst->rbegin(); it != inst->rend(); ++it) {
        if (it->r.is_point_inside(x, y)) {
            switch (it->inst) {
            case ON:
                // Nice
                if (pixel == true) {
                    return false;
                } else {
                    return true;
                }
                break;
            case OFF:
                // Nice
                if (pixel == false) {
                    return false;
                } else {
                    return true;
                }
                break;
            case TOGGLE:
                pixel = pixel ^ true;
                break;
            default:
                break;
            }
        } else {
            // Keep looking
        }
    }
    std::cout << "No absolute instruction encountered" << std::endl;
    return pixel;
}

unsigned int get_final_brightness(unsigned int x, unsigned int y, std::vector<Instruction> *inst) {
    unsigned int pixel{0};
    for (auto &i : *inst) {
        if (i.r.is_point_inside(x, y)) {
            switch (i.inst) {
            case ON:
                pixel += 1;
                break;
            case OFF:
                if (pixel > 0) {
                    pixel -= 1;
                }
                break;
            case TOGGLE:
                pixel += 2;
                break;
            }
        }
    }
    return pixel;
}

// Start from end (assume dark) and do as said -> if absolute found see if matches (otherwise toogle one last time)

int main(void) {
    std::ifstream text_input("../day06.txt");
    std::string input;
    std::vector<Instruction> inst;

    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            inst.push_back(Instruction(input));
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    // inst.clear();
    // inst.push_back(Instruction(std::string("turn on 0,0 through 999,999")));
    // inst.push_back(Instruction(std::string("toggle 0,0 through 999,0")));
    // inst.push_back(Instruction(std::string("turn off 499,499 through 500,500")));

    std::cout << "Part 1:" << std::endl;
    // Ok now every pixel:
    unsigned int num_lit_pixel{0};
    for (int x = 0; x < 1000; x++) {
        for (int y = 0; y < 1000; y++) {
            if (is_finally_lit(x, y, &inst)) {
                num_lit_pixel++;
            }
        }
    }
    std::cout << "Answer: " << num_lit_pixel << std::endl;

    std::cout << "Part 2:" << std::endl;

    // inst.clear();
    // inst.push_back(Instruction(std::string("turn on 0,0 through 999,999")));
    // inst.push_back(Instruction(std::string("toggle 0,0 through 999,0")));
    // inst.push_back(Instruction(std::string("turn off 499,499 through 500,500")));

    // Ok now every pixel:
    unsigned int tot_pixel_brightness{0};
    for (int x = 0; x < 1000; x++) {
        for (int y = 0; y < 1000; y++) {
            tot_pixel_brightness += get_final_brightness(x, y, &inst);
        }
    }
    std::cout << "Answer: " << tot_pixel_brightness << std::endl;
}
