#include <array>
#include <fstream>
#include <iostream>
#include <ostream>
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

std::vector<std::vector<std::string>> parse(std::vector<std::string> str) {

    std::vector<std::vector<std::string>> fields;

    fields.push_back({});
    auto f = fields.rbegin();

    for (auto l : str) {
        if (l == "") {
            fields.push_back({});
            f = fields.rbegin();
        } else {
            f->push_back(l);
        }
    }

    return fields;
}

std::vector<std::string> transponse(std::vector<std::string> field) {

    std::vector<std::string> t_field{};

    for (int col = 0; col < field[0].size(); col++) {
        std::string l{};
        for (int row = 0; row < field.size(); row++) {
            l += field[row][col];
        }
        t_field.push_back(l);
    }

    return t_field;
}

std::vector<std::vector<std::string>> transponse(std::vector<std::vector<std::string>> fields) {
    std::vector<std::vector<std::string>> t_fields{};

    for (auto field : fields) {
        std::vector<std::string> t_field = transponse(field);
        t_fields.push_back(t_field);
    }

    return t_fields;
}

int get_smudges(std::vector<std::string> field, int plane) {

    // Get smaller side

    int dec = plane;
    int inc = plane + 1;

    int smudges = 0;

    while (dec >= 0 && inc < field.size()) {

        // std::cout << field[dec] << " vs. " << field[inc];

        for (int i = 0; i < field[0].size(); i++) {
            if (field[dec][i] != field[inc][i]) {
                smudges++;
            }
        }

        dec--;
        inc++;
        // std::cout << std::endl;
    }

    return smudges;
}

std::array<std::vector<int>, 2> find_mirror(std::vector<std::string> field) {

    std::vector<int> mirrors;
    std::vector<int> mirrors_with_smudges;

    for (auto i = 0; i < field.size() - 1; i++) {
        int smudges = get_smudges(field, i);

        if (smudges == 0) {
            mirrors.push_back(i);
        } else if (smudges == 1) {
            // std::cout << "At: " << i << ", smudges: " << smudges << std::endl;
            mirrors_with_smudges.push_back(i);
        }
    }

    return {mirrors, mirrors_with_smudges};
}

int main(void) {
    std::ifstream text_input("../day13.txt");
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
    //     "#.##..##.", "..#.##.#.", "##......#", "##......#", "..#.##.#.", "..##..##.", "#.#.##.#.", "",
    //     "#...##..#", "#....#..#", "..##..###", "#####.##.", "#####.##.", "..##..###", "#....#..#",
    // };

    std::vector<std::vector<std::string>> fields = parse(str);

    std::vector<std::vector<std::string>> t_fields = transponse(fields);

    int p1 = 0;
    int p2 = 0;

    for (auto f : fields) {
        // std::cout << "\nField: " << std::endl;
        // for (auto l : f) {
        //     std::cout << l << std::endl;
        // }

        std::array<std::vector<int>, 2> mirrors_and_smudges = find_mirror(f);

        std::vector<int> mirrors = mirrors_and_smudges[0];
        std::vector<int> smudges = mirrors_and_smudges[1];

        if (!mirrors.empty()) {
            for (auto m : mirrors) {
                // std::cout << "Mirror at: " << m << std::endl;
                p1 += (m + 1) * 100;
            }
        } else {
            // std::cout << "No mirror" << std::endl;
        }

        if (!smudges.empty()) {
            for (auto m : smudges) {
                // std::cout << "Smudges at: " << m << std::endl;
                p2 += (m + 1) * 100;
            }
        } else {
            // std::cout << "No mirror" << std::endl;
        }
    }

    // std::cout << "Transponse:" << std::endl;

    for (auto f : t_fields) {
        // std::cout << "\nField: " << std::endl;
        // for (auto l : f) {
        //     std::cout << l << std::endl;
        // }

        std::array<std::vector<int>, 2> mirrors_and_smudges = find_mirror(f);

        std::vector<int> mirrors = mirrors_and_smudges[0];
        std::vector<int> smudges = mirrors_and_smudges[1];

        if (!mirrors.empty()) {
            for (auto m : mirrors) {
                // std::cout << "Mirror at: " << m << std::endl;
                p1 += (m + 1);
            }
        } else {
            // std::cout << "No mirror" << std::endl;
        }

        if (!smudges.empty()) {
            for (auto m : smudges) {
                // std::cout << "Smudges at: " << m << std::endl;
                p2 += (m + 1);
            }
        } else {
            // std::cout << "No mirror" << std::endl;
        }
    }

    std::cout << "Part 1:\nAnswer: " << p1 << std::endl << std::endl;
    std::cout << "Part 2:\nAnswer: " << p2 << std::endl << std::endl;
}
