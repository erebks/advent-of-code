#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <map>
#include <memory>
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

std::set<int> recursive(std::string molecule, int depth, std::map<std::string, std::set<std::string>> const &recipies,
                        std::set<std::string> const &final_recipes) {
    std::set<int> replacements;
    // Do the replacement

    // std::cout << "At " << depth << " molecule: " << molecule << std::endl;

    // Check if e-> is the only possible replacement
    for (auto r : final_recipes) {
        if (molecule == r) {
            // End!
            // std::cout << "\t-> Is final!" << std::endl;
            replacements.insert(++depth);
            return replacements;
        }
    }

    for (auto prev : recipies) {
        for (auto m : prev.second) {

            std::regex re(m + "(?![^A-Z])");

            std::regex_iterator<std::string::iterator> rit(molecule.begin(), molecule.end(), re);
            std::regex_iterator<std::string::iterator> end;

            for (; rit != end; rit++) {
                // std::cout << "\t" << rit->str() << " Found at: " << rit->position() << std::endl;
                std::string m = molecule.substr(0, rit->position()) + prev.first + rit->suffix().str();

                std::set<int> ret = recursive(m, depth + 1, recipies, final_recipes);

                for (auto r : ret) {
                    // Hack to be faster... The puzzle is designed that most solutions are equally long
                    replacements.insert(r);
                    return replacements;
                }
            }
        }
    }

    return replacements;
}

int main(void) {
    std::ifstream text_input("../day19.txt");
    std::string input;

    std::map<std::string, std::set<std::string>> recipies;
    std::string molecule;

    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            // std::cout << "Line: '" << input << "'" << std::endl;
            if (input == "") {
                break;
            }
            std::vector<std::string> rec = resplit(input, std::regex(" => "));

            auto it = recipies.find(rec[0]);
            if (it == recipies.end()) {
                recipies.insert({rec[0], {rec[1]}});
            } else {
                it->second.insert(rec[1]);
            }
        }

        // Now read the last recipe
        if (std::getline(text_input, input)) {
            // std::cout << "Line: '" << input << "'" << std::endl;
            molecule = input;
        }

        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    // recipies.clear();
    // recipies.insert({"e", {"H", "O"}});
    // recipies.insert({"H", {"HO", "OH"}});
    // recipies.insert({"O", {"HH"}});
    // molecule = "HOH";

    for (auto r : recipies) {
        std::cout << "Recipe: " << r.first << " (";
        for (auto out : r.second) {
            std::cout << out << ", ";
        }
        std::cout << ")" << std::endl;
    }

    std::cout << "Molecule: " << molecule << std::endl;

    std::set<std::string> molecules;

    for (auto r : recipies) {

        std::regex re(r.first + "(?![^A-Z])");

        std::regex_iterator<std::string::iterator> rit(molecule.begin(), molecule.end(), re);
        std::regex_iterator<std::string::iterator> end;

        for (; rit != end; rit++) {
            // std::cout << rit->str() << " Found at: " << rit->position() << std::endl;
            // Now replace it

            for (auto out : r.second) {

                std::string replace;
                // Prefix will only give me the prefix until the last find...
                // Thuse use substr

                replace = molecule.substr(0, rit->position()) + out + rit->suffix().str();
                // std::cout << "\t" << r.first << " => " << out;
                // std::cout << " Gives: " << replace << "(" << rit->prefix().str() << " " << rit->suffix().str() << ")" << std::endl;

                molecules.insert(replace);
            }
        }
    }

    std::cout << "Part 1:\nAnswer: " << molecules.size() << std::endl << std::endl;

    // Start only with e and try to put together molecule
    // One at a time!

    std::set<std::string> final_recipes(recipies.at("e"));
    recipies.erase("e");

    // molecule = "HOH"; // Should give 3
    // molecule = "HOHOHO"; // Should give 6

    std::set<int> replacements = recursive(molecule, 0, recipies, final_recipes);

    // Iterate over recipes and try to fit
    std::cout << "Part 2:\nAnswer: " << *replacements.rbegin() << std::endl << std::endl;
}
