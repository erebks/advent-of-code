#include <fstream>
#include <iostream>
#include <string>

int main(void) {
    std::ifstream text_input("../dayXX.txt");
    std::string input;

    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            std::cout << "Line: '" << input << "'" << std::endl;
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    std::cout << "Hello World" << std::endl;
}
