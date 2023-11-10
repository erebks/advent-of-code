#include <array>
#include <fstream>
#include <iostream>
#include <set>
#include <string>

/*
 y

 ^
 |
 +--> x

*/

struct SantaRunner {
    std::set<std::array<unsigned int, 2>> pos = {{0, 0}};

    SantaRunner(){};

    SantaRunner(std::string path) {
        std::array<unsigned int, 2> cur_pos = {0, 0}; // x, y
        for (char step : path) {
            switch (step) {
            case '>':
                // increase x
                cur_pos[0]++;
                break;
            case '<':
                // decrease x
                cur_pos[0]--;
                break;
            case '^':
                // increase y
                cur_pos[1]++;
                break;
            case 'v':
                // decrease y
                cur_pos[1]--;
                break;
            default:
                std::cout << "Undefined char" << std::endl;
                throw 1;
                break;
            }

            // Insert position and let set handle doublicates
            pos.insert(cur_pos);
        }
    };

    std::set<std::array<unsigned int, 2>> get_pos(void) { return pos; }
};

int main(void) {
    std::ifstream text_input("../day03.txt");
    std::string input;
    if (text_input.is_open()) {
        std::getline(text_input, input);
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    std::cout << "Part 1:" << std::endl;

    SantaRunner s = SantaRunner(input);
    SantaRunner s0 = SantaRunner(">");
    SantaRunner s1 = SantaRunner("^>v<");
    SantaRunner s2 = SantaRunner("^v^v^v^v^v");

    std::cout << s.get_pos().size() << std::endl;

    std::cout << "Part 2:" << std::endl;

    std::string santa_path{};
    std::string robot_path{};

    for (size_t i = 0; i < input.size(); i++) {
        if (i % 2) {
            santa_path += input[i];
        } else {
            robot_path += input[i];
        }
    }

    SantaRunner santa = SantaRunner(santa_path);
    SantaRunner robot = SantaRunner(robot_path);

    // Does this do deep copy??
    std::set<std::array<unsigned int, 2>> santa_visited = santa.get_pos();
    std::set<std::array<unsigned int, 2>> robot_visited = robot.get_pos();

    // Wasn't able to get this running...
    // santa_visited.merge(robot_visited);

    for (std::array<unsigned int, 2> pos : santa_visited) {
        robot_visited.insert(pos);
    }

    std::cout << robot_visited.size() << std::endl;
}
