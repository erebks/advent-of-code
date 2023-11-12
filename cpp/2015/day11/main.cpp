#include <array>
#include <fstream>
#include <iostream>
#include <regex>
#include <string>
#include <vector>

std::vector<char> increment(std::vector<char> old) {
    bool carry{true};

    // From the last element
    for (auto o = old.rbegin(); o != old.rend(); o++) {
        if (carry) {
            // Increment
            (*o)++;
            carry = false;
            switch (*o) {
            case ('z' + 1):
                carry = true;
                *o = 'a';
                break;
            case 'i':
            case 'o':
            case 'l':
                (*o)++;
            }
        } else {
            break;
        }
    }

    return old;
}

bool is_valid(std::vector<char> pw) {

    std::string n{};

    for (int i = 0; i < pw.size(); i++) {
        n += pw[i];
    }

    // std::cout << "Checking PW: " << n << std::endl;

    bool first_condition{false};
    for (int i = 0; i < pw.size() - 2; i++) {
        if (pw[i + 1] == (pw[i] + 1) && pw[i + 2] == (pw[i] + 2)) {
            first_condition = true;
            break;
        }
    }

    if (!first_condition) {
        // std::cout << "\tFirst condition not met" << std::endl;
        return false;
    }

    std::regex re("([a-z])\\1"); // Finds pairs of same charater e.g. 'aa', 'bb'
    std::smatch match{};

    int matches = 0;
    std::string inner(n);
    while (std::regex_search(inner, match, re)) {
        inner = match.suffix().str();
        matches++;
    }

    // std::cout << "\tmatches: " << matches << std::endl;

    return (matches >= 2);
}

std::string find_next(std::string old) {

    std::vector<char> pw;

    for (int i = 0; i < old.size(); i++) {
        pw.push_back((char)old[i]);
    }

    do {
        pw = increment(pw);
    } while (!is_valid(pw));

    std::string n{};

    for (int i = 0; i < pw.size(); i++) {
        n += pw[i];
    }

    return n;
};

int main(void) {
    std::ifstream text_input("../day11.txt");
    std::string input;
    std::string old_pw;

    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            std::cout << "Line: '" << input << "'" << std::endl;
            old_pw = input;
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    //    old_pw = "abcdefgh";

    std::string pw = find_next(old_pw);

    std::cout << "Part 1:\nAnswer: " << pw << std::endl;

    pw = find_next(pw);

    std::cout << "Part 2:\nAnswer: " << pw << std::endl;
}
