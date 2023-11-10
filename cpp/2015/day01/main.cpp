#include <fstream>
#include <iostream>
#include <string>

// Should result in floor 0
#define FLOOR0_1 ("(())")
#define FLOOR0_2 ("()()")

// Should result in floor 3
#define FLOOR3_1 ("(((")
#define FLOOR3_2 ("(()(()(")
#define FLOOR3_3 ("))(((((")

// Should result in floor -1
#define FLOORn1_1 ("())")
#define FLOORn1_2 ("))(")

// Should result in floor -3
#define FLOORn3_1 (")))")
#define FLOORn3_2 (")())())")

int part1(std::string input) {
    int floor = 0;

#if (1)
    // Range based loop, available since C++11
    for (char c : input) {
        switch (c) {
        case '(':
            floor++;
            break;
        case ')':
            floor--;
            break;
        default:
            std::cout << "Houston, we have a problem!" << std::endl;
            break;
        }
    }
    return floor;
#else
    // Or
    for (int i = 0; i < input.size(); i++) {
        switch (input[i]) {
        case '(':
            floor++;
            break;
        case ')':
            floor--;
            break;
        default:
            std::cout << "Houston, we have a problem!" << std::endl;
            break;
        }
    }
    return floor;
#endif
}

int part2(std::string input) {

    int floor = 0;
    size_t i = 0;

    for (i = 0; i < input.size(); i++) {
        switch (input[i]) {
        case '(':
            floor++;
            break;
        case ')':
            floor--;
            break;
        default:
            std::cout << "Houston, we have a problem!" << std::endl;
            break;
        }
        if (floor == -1)
            return i + 1;
    }

    std::cout << "Potential problem, should't come here!" << std::endl;

    return i + 1;
}

int main(void) {

    std::ifstream Day01_input("../day01.txt");
    std::string input;
    if (Day01_input.is_open()) {
        std::getline(Day01_input, input);
        Day01_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    std::cout << "Part 1: " << std::endl;
    std::cout << "Answer: " << part1(input) << std::endl;

    std::cout << "Part 2: " << std::endl;
    std::cout << "Answer: " << part2(input) << std::endl;
}
