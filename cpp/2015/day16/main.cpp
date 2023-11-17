#include <fstream>
#include <iostream>
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

struct AuntieSue {
    int id{-1};
    int children{-1};
    int cats{-1};
    int samoyeds{-1};
    int pomeranians{-1};
    int akitas{-1};
    int vizslas{-1};
    int goldfish{-1};
    int trees{-1};
    int cars{-1};
    int perfumes{-1};

    friend std::ostream &operator<<(std::ostream &os, const AuntieSue &obj) {

        os << "ID: " << obj.id;

        if (obj.children >= 0) {
            os << ", children: " << obj.children;
        }
        if (obj.cats >= 0) {
            os << ", cats: " << obj.cats;
        }
        if (obj.samoyeds >= 0) {
            os << ", samoyeds: " << obj.samoyeds;
        }
        if (obj.pomeranians >= 0) {
            os << ", pomeranians: " << obj.pomeranians;
        }
        if (obj.akitas >= 0) {
            os << ", akitas: " << obj.akitas;
        }
        if (obj.vizslas >= 0) {
            os << ", vizslas: " << obj.vizslas;
        }
        if (obj.goldfish >= 0) {
            os << ", goldfish: " << obj.goldfish;
        }
        if (obj.trees >= 0) {
            os << ", trees: " << obj.trees;
        }
        if (obj.cars >= 0) {
            os << ", cars: " << obj.cars;
        }
        if (obj.perfumes >= 0) {
            os << ", perfumes: " << obj.perfumes;
        }

        return os;
    }
};

int main(void) {
    std::ifstream text_input("../day16.txt");
    std::string input;

    std::vector<AuntieSue *> sues;

    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            std::cout << "Line: '" << input << "'" << std::endl;
            std::vector<std::string> split = resplit(input, std::regex(" "));

            int id = std::stoi(split[1].substr(0, split[1].size() - 1));

            AuntieSue *sue = new AuntieSue;
            sue->id = id;

            auto it = split.begin() + 2;

            for (; it < split.end(); it += 2) {
                int value;

                if ((it + 1) == split.end() - 1) {
                    value = std::stoi(*(it + 1));
                } else {
                    value = std::stoi((it + 1)->substr(0, (it + 1)->size() - 1));
                }

                // Could be made prettier...
                if (*it == "children:") {
                    sue->children = value;
                } else if (*it == "cats:") {
                    sue->cats = value;
                } else if (*it == "samoyeds:") {
                    sue->samoyeds = value;
                } else if (*it == "pomeranians:") {
                    sue->pomeranians = value;
                } else if (*it == "akitas:") {
                    sue->akitas = value;
                } else if (*it == "vizslas:") {
                    sue->vizslas = value;
                } else if (*it == "goldfish:") {
                    sue->goldfish = value;
                } else if (*it == "trees:") {
                    sue->trees = value;
                } else if (*it == "cars:") {
                    sue->cars = value;
                } else if (*it == "perfumes:") {
                    sue->perfumes = value;
                } else {
                    std::cout << "Problem!" << std::endl;
                    return -1;
                }
            }

            sues.push_back(sue);
            std::cout << *sue << std::endl;
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    // search for Part 1
    for (auto sue : sues) {
        if (!(sue->children == 3 || sue->children == -1)) {
            continue;
        }
        if (!(sue->cats == 7 || sue->cats == -1)) {
            continue;
        }
        if (!(sue->samoyeds == 2 || sue->samoyeds == -1)) {
            continue;
        }
        if (!(sue->pomeranians == 3 || sue->pomeranians == -1)) {
            continue;
        }
        if (!(sue->akitas == 0 || sue->akitas == -1)) {
            continue;
        }
        if (!(sue->vizslas == 0 || sue->vizslas == -1)) {
            continue;
        }
        if (!(sue->goldfish == 5 || sue->goldfish == -1)) {
            continue;
        }
        if (!(sue->trees == 3 || sue->trees == -1)) {
            continue;
        }
        if (!(sue->cars == 2 || sue->cars == -1)) {
            continue;
        }
        if (!(sue->perfumes == 1 || sue->perfumes == -1)) {
            continue;
        }
        std::cout << "\nPart 1: " << *sue << std::endl;
        break;
    }

    // search for Part 2
    for (auto sue : sues) {
        if (!(sue->children == 3 || sue->children == -1)) {
            continue;
        }
        if (!(sue->cats > 7 || sue->cats == -1)) {
            continue;
        }
        if (!(sue->samoyeds == 2 || sue->samoyeds == -1)) {
            continue;
        }
        if (!(sue->pomeranians < 3 || sue->pomeranians == -1)) {
            continue;
        }
        if (!(sue->akitas == 0 || sue->akitas == -1)) {
            continue;
        }
        if (!(sue->vizslas == 0 || sue->vizslas == -1)) {
            continue;
        }
        if (!(sue->goldfish < 5 || sue->goldfish == -1)) {
            continue;
        }
        if (!(sue->trees > 3 || sue->trees == -1)) {
            continue;
        }
        if (!(sue->cars == 2 || sue->cars == -1)) {
            continue;
        }
        if (!(sue->perfumes == 1 || sue->perfumes == -1)) {
            continue;
        }
        std::cout << "\nPart 2: " << *sue << std::endl;
        break;
    }

    // Free all the aunties
    for (auto sue : sues) {
        free(sue);
    }
}
