#include <array>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

bool is_number(char c) {
    if ((c >= '0' && c <= '9')) {
        return true;
    }

    return false;
}

bool is_symbol(char c) {
    if (c == '.') {
        return false;
    }
    if (is_number(c)) {
        return false;
    }
    return true;
}

int get_number(std::string &line, int pos) {

    std::cout << "Getting number. Line: '" << line << "' pos: " << pos << std::endl;

    std::string number;
    if (is_number(line[pos])) {

        // Extract number
        // Go left
        int num_start = pos;
        int num_end = pos;

        while (1) {
            if (is_number(line[num_start])) {
                if (num_start > 0) {
                    num_start--;
                } else {
                    break;
                }
            } else {
                num_start++;
                break;
            }
        }

        while (1) {
            if (is_number(line[num_end])) {
                if (num_end < line.size()) {
                    num_end++;
                } else {
                    break;
                }
            } else {
                num_end--;
                break;
            }
        }

        number = line.substr(num_start, (num_end - num_start) + 1);

        std::cout << "\tFound! Line: '" << line << "' , start: " << num_start << ", end: " << num_end << ", number: " << number << std::endl;

        // Set digits of number in line to '.'
        while (num_start <= num_end) {
            line.replace(num_start++, 1, ".");
        }

        std::cout << "Line: " << line << std::endl;
        return std::stoi(number);

    } else {
        return 0;
    }
}

int sum_of_adjacent(std::vector<std::string> &schematic, int pos_line, int pos_char) {

    int sum = 0;

    if (!is_symbol(schematic[pos_line][pos_char])) {
        return sum;
    }

    // Top
    if (pos_line > 0) {
        sum += get_number(schematic[pos_line - 1], pos_char - 1);
        sum += get_number(schematic[pos_line - 1], pos_char);
        sum += get_number(schematic[pos_line - 1], pos_char + 1);
    }

    // Left
    if (pos_char > 0) {
        sum += get_number(schematic[pos_line], pos_char - 1);
    }

    // Right
    if (pos_char < schematic[0].size()) {
        sum += get_number(schematic[pos_line], pos_char + 1);
    }

    // Bottom
    if (pos_line < schematic.size()) {
        sum += get_number(schematic[pos_line + 1], pos_char - 1);
        sum += get_number(schematic[pos_line + 1], pos_char);
        sum += get_number(schematic[pos_line + 1], pos_char + 1);
    }

    return sum;
}

int sum_of_gear_ratios(std::vector<std::string> &schematic, int pos_line, int pos_char) {

    int ratio = 1;
    int cnt_numbers = 0;

    // Is a gear if the symbol is '*' and it has exactly two part numbers

    if (schematic[pos_line][pos_char] != '*') {
        return 0;
    }

    // Search for exactly two numbers

    // Top
    int num = 0;
    if (pos_line > 0) {
        num = get_number(schematic[pos_line - 1], pos_char - 1);
        if (num != 0) {
            ratio *= num;
            cnt_numbers++;
        }
        num = get_number(schematic[pos_line - 1], pos_char);
        if (num != 0) {
            ratio *= num;
            cnt_numbers++;
        }

        num = get_number(schematic[pos_line - 1], pos_char + 1);
        if (num != 0) {
            ratio *= num;
            cnt_numbers++;
        }
    }

    // Left
    if (pos_char > 0) {
        num = get_number(schematic[pos_line], pos_char - 1);
        if (num != 0) {
            ratio *= num;
            cnt_numbers++;
        }
    }

    // Right
    if (pos_char < schematic[0].size()) {
        num = get_number(schematic[pos_line], pos_char + 1);
        if (num != 0) {
            ratio *= num;
            cnt_numbers++;
        }
    }

    // Bottom
    if (pos_line < schematic.size()) {
        num = get_number(schematic[pos_line + 1], pos_char - 1);
        if (num != 0) {
            ratio *= num;
            cnt_numbers++;
        }
        num = get_number(schematic[pos_line + 1], pos_char);
        if (num != 0) {
            ratio *= num;
            cnt_numbers++;
        }
        num = get_number(schematic[pos_line + 1], pos_char + 1);
        if (num != 0) {
            ratio *= num;
            cnt_numbers++;
        }
    }

    if (cnt_numbers == 2) {
        return ratio;
    } else {
        return 0;
    }
}

int main(void) {
    std::ifstream text_input("../day03.txt");
    std::string input;

    std::vector<std::string> schematic;

    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            schematic.push_back(input);
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    // Iterate over schematic
    // Find "symbols" (anything that isn't . or 0-9)
    // If symbol found -> look at adjacent 8 tiles, add number and set to '.'

    // schematic.clear();
    // schematic.push_back("467..114..");
    // schematic.push_back("...*......");
    // schematic.push_back("..35..633.");
    // schematic.push_back("......#...");
    // schematic.push_back("617*......");
    // schematic.push_back(".....+.58.");
    // schematic.push_back("..592.....");
    // schematic.push_back("......755.");
    // schematic.push_back("...$.*....");
    // schematic.push_back(".664.598..");

    std::vector<std::string> schematic_p2(schematic);

    int sum = 0;
    for (int line = 0; line < schematic.size(); line++) {
        for (int cha = 0; cha < schematic[0].size(); cha++) {
            sum += sum_of_adjacent(schematic, line, cha);
        }
    }

    std::cout << "Part 1: \nAnswer: " << sum << std::endl << std::endl;

    sum = 0;
    for (int line = 0; line < schematic_p2.size(); line++) {
        for (int cha = 0; cha < schematic_p2[0].size(); cha++) {
            sum += sum_of_gear_ratios(schematic_p2, line, cha);
        }
    }

    std::cout << "Part 2: \nAnswer: " << sum << std::endl;

    std::cout << "Hello World" << std::endl;
}
