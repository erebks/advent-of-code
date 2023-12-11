#include <array>
#include <cmath>
#include <fstream>
#include <iostream>
#include <set>
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

bool is_galaxy_in_line(std::string line) {
    for (auto c : line) {
        if (c != '.') {
            return true;
        }
    }
    return false;
}

std::vector<std::string> expand(std::vector<std::string> universe) {
    std::vector<std::string> u;

    std::set<int> rows;
    std::set<int> cols;

    // std::cout << "Rows to insert: ";

    for (int row = 0; row < universe.size(); row++) {
        if (!is_galaxy_in_line(universe[row])) {
            rows.insert(row);
            // std::cout << row << ", ";
        }
    }

    // std::cout << std::endl;

    // std::cout << "Cols to insert: ";
    for (int col = 0; col < universe[0].size(); col++) {
        std::string line{};
        for (int row = 0; row < universe.size(); row++) {
            line += universe[row][col];
        }

        if (!is_galaxy_in_line(line)) {
            // std::cout << col << ", ";
            cols.insert(col);
        }
    }
    // std::cout << std::endl;

    int u_row = 0;
    int u_col = 0;

    for (int row = 0; row < universe.size(); row++) {
        std::string line{};

        for (int col = 0; col < universe[0].size(); col++) {
            line += universe[row][col];
            if (cols.find(col) != cols.end()) {
                line += universe[row][col];
            }
        }

        u.push_back(line);

        if (rows.find(row) != rows.end()) {
            u.push_back(line);
        }
    }

    return u;
}

std::vector<std::array<int, 2>> find_galaxies(std::vector<std::string> universe) {
    std::vector<std::array<int, 2>> galaxies;

    for (int row = 0; row < universe.size(); row++) {
        for (int col = 0; col < universe[0].size(); col++) {
            if (universe[row][col] == '#') {
                galaxies.push_back({row, col});
            }
        }
    }
    return galaxies;
}

std::vector<std::array<int, 2>> expand_and_find_galaxies(std::vector<std::string> universe, unsigned int expansion) {

    std::set<int> rows;
    std::set<int> cols;

    // std::cout << "Rows to insert: ";

    for (int row = 0; row < universe.size(); row++) {
        if (!is_galaxy_in_line(universe[row])) {
            rows.insert(row);
            // std::cout << row << ", ";
        }
    }

    // std::cout << std::endl;

    // std::cout << "Cols to insert: ";
    for (int col = 0; col < universe[0].size(); col++) {
        std::string line{};
        for (int row = 0; row < universe.size(); row++) {
            line += universe[row][col];
        }

        if (!is_galaxy_in_line(line)) {
            // std::cout << col << ", ";
            cols.insert(col);
        }
    }
    // std::cout << std::endl;

    std::vector<std::array<int, 2>> galaxies;

    int expanded_row = 0;
    int expanded_col = 0;

    for (int row = 0; row < universe.size(); row++) {
        for (int col = 0; col < universe[0].size(); col++) {
            if (universe[row][col] == '#') {
                galaxies.push_back({expanded_row, expanded_col});
            }
            if (cols.find(col) != cols.end()) {
                expanded_col += (expansion - 1);
            }
            expanded_col++;
        }
        if (rows.find(row) != rows.end()) {
            expanded_row += (expansion - 1);
        }
        expanded_col = 0;
        expanded_row++;
    }
    return galaxies;
}

std::array<int, 2> step(std::array<int, 2> pos, std::array<int, 2> end) {

    if (pos == end) {
        return pos;
    }

    // calculate trajectory
    int delta_row = (end[0] - pos[0]);
    int delta_col = (end[1] - pos[1]);

    int step_row = 1;
    int step_col = 1;

    if (delta_row < 0) {
        step_row = -1;
    }

    if (delta_col < 0) {
        step_col = -1;
    }

    // std::cout << "delta_row: " << delta_row << ", delta_col: " << delta_col << std::endl;

    if (std::abs(delta_row) == 0) {
        // use col
        // std::cout << "\tUsing col. pos: ";
        pos[1] += step_col;
    } else if (std::abs(delta_col) == 0) {
        // use row
        // std::cout << "\tUsing row. pos: ";
        pos[0] += step_row;
    } else if (std::abs(delta_row) < std::abs(delta_col)) {
        // use col
        // std::cout << "\tUsing col. pos: ";
        pos[1] += step_col;
    } else {
        // use row
        // std::cout << "\tUsing row. pos: ";
        pos[0] += step_row;
    }

    // std::cout << pos[0] << ", " << pos[1] << std::endl;
    return pos;
}

std::vector<std::array<int, 2>> find_path(std::array<int, 2> a, std::array<int, 2> b) {
    std::vector<std::array<int, 2>> path;

    std::array<int, 2> pos(a);

    while (pos != b) {
        pos = step(pos, b);
        path.push_back(pos);
    }

    return path;
}

unsigned long long find_path_length(std::array<int, 2> a, std::array<int, 2> b) {
    unsigned long long length = 0;

    unsigned long long delta_x = std::abs(b[0] - a[0]);
    unsigned long long delta_y = std::abs(b[1] - a[1]);

    return delta_x + delta_y;
}

int main(void) {
    std::ifstream text_input("../day11.txt");
    std::string input;

    std::vector<std::string> str;

    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            // std::cout << "Line: '" << input << "'" << std::endl;
            str.push_back(input);
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    // str = {
    //     "...#......", ".......#..", "#.........", "..........", "......#...", ".#........", ".........#", "..........", ".......#..", "#...#.....",
    // };

    std::vector<std::array<int, 2>> galaxies = expand_and_find_galaxies(str, 2);

    std::vector<std::vector<int>> path_lengths;

    for (auto g : galaxies) {

        std::vector<int> a;
        a.resize(galaxies.size());

        path_lengths.push_back(a);
    }

    unsigned long long p1 = 0;
    for (int i = 0; i < galaxies.size(); i++) {
        for (int other = i + 1; other < galaxies.size(); other++) {
            p1 += find_path_length(galaxies[i], galaxies[other]);
        }
    }

    std::cout << "Part 1\nAnswer: " << p1 << std::endl << std::endl;

    std::vector<std::array<int, 2>> galaxies_p2 = expand_and_find_galaxies(str, 1000000);

    unsigned long long p2 = 0;
    for (int i = 0; i < galaxies_p2.size(); i++) {
        for (int other = i + 1; other < galaxies_p2.size(); other++) {
            p2 += find_path_length(galaxies_p2[i], galaxies_p2[other]);
        }
    }

    std::cout << "Part 2\nAnswer: " << p2 << std::endl << std::endl;
}
