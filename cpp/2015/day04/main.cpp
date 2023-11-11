#include <cstdio>
#include <cstring>
#include <fstream>
#include <ios>
#include <iostream>
#include <openssl/md5.h>
#include <string>

unsigned int find_sequence(std::string key, std::string starts_with) {
    // Find sequence that produces md5 hash with 5 leading zeros
    unsigned int sequence{0};
    std::string hash{};

    do {
        std::string phrase = key + std::to_string(sequence);
        hash = std::string();

        unsigned char res[MD5_DIGEST_LENGTH]{};

        MD5((const unsigned char *)phrase.c_str(), phrase.size(), res);

        for (unsigned char &c : res) {
            // Performs copy... Isn't very good...
            char c_in_hex[3]{};
            std::snprintf(c_in_hex, 3, "%02x", c);

            hash = hash + c_in_hex[0] + c_in_hex[1];
        }

        // std::cout << "Phrase: " << phrase << " Hash: " << hash << std::endl;
        sequence++;
    } while (hash.compare(0, starts_with.size(), starts_with) != 0);

    return sequence - 1;
}

int main(void) {
    std::ifstream text_input("../day04.txt");
    std::string input;

    if (text_input.is_open()) {
        std::getline(text_input, input);
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    std::cout << "Part 1" << std::endl;
    unsigned int sequence = find_sequence(input, std::string("00000"));

    std::cout << "Answer: " << sequence << std::endl;

    std::cout << "Part 2" << std::endl;
    sequence = find_sequence(input, std::string("000000"));

    std::cout << "Answer: " << sequence << std::endl;
}
