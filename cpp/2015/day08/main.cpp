#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>

unsigned int strlen_in_memory(std::string str) {

    size_t pos{};
    std::cout << "String: '" << str << "'";
    pos = str.find('\\', pos);

    while (pos != -1) {
        std::cout << "pos: " << pos << std::endl;
        std::string subs{};
        // Found! Now we see whats behind it
        switch (str[pos + 1]) {
        case '\\':
        case '"':
            // We just delete pos
            str.erase(pos, 1);
            pos++;
            break;
        case 'x':
            subs = str.substr(pos + 2, pos + 4);
            str.erase(pos, 4);
            str.insert(pos, 1, (char)std::stoi(subs, nullptr, 16));
            break;
        default:
            break;
        }
        pos = str.find('\\', pos);
    }

    str.erase(0, 1);
    str.erase(str.size() - 1, 1);

    std::cout << " -> '" << str << "' size: " << str.size() << std::endl;

    return str.size();
}

std::string str_to_literal(std::string str) {

    size_t pos{};
    std::cout << "String: '" << str << "'";

    // Search all \ and prepend with \

    pos = str.find('\\', pos);
    while (pos != str.npos) {
        std::cout << "pos: " << pos << std::endl;
        str.insert(pos, 1, '\\');
        pos++;
        pos++;

        pos = str.find('\\', pos);
    }

    std::cout << " -> '" << str << "' size: " << str.size();

    pos = 0;
    pos = str.find('\"', pos);
    while (pos != str.npos) {
        str.insert(pos, 1, '\\');
        pos++;
        pos++;

        pos = str.find('\"', pos);
    }

    std::cout << " -> '" << str << "' size: " << str.size();

    str.insert(0, 1, '\"');
    str.insert(str.size() - 1, 1, '\"');
    std::cout << " -> '" << str << "' size: " << str.size() << std::endl;

    return str;
}

int main(void) {
    std::ifstream text_input("../day08.txt");
    std::string input;

    int answer_p1{};
    int answer_p2{};

    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            std::cout << "Line: '" << input << "'" << std::endl;
            answer_p1 += input.size();
            answer_p1 -= strlen_in_memory(input);

            answer_p2 -= input.size();
            answer_p2 += str_to_literal(input).size();
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    std::cout << "Part 1:" << std::endl;

    std::cout << "Answer: " << answer_p1 << std::endl << std::endl;

    std::cout << "Part 2:" << std::endl;
    std::cout << "Answer: " << answer_p2 << std::endl;
}
