#include <fstream>
#include <iostream>
#include <string>

// Hat-tip to https://stackoverflow.com/a/28142357
#include <regex>
#include <vector>
std::vector<std::string> resplit(const std::string &s, const std::regex &sep_regex = std::regex{"\\s+"}) {
    std::sregex_token_iterator iter(s.begin(), s.end(), sep_regex, -1);
    std::sregex_token_iterator end;
    return {iter, end};
}

struct Card {
    std::vector<int> winning_numbers;
    std::vector<int> card_numbers;
    int matching = 0;
    int points = 0;
    int copies = 0;

    Card(std::vector<int> winning_numbers, std::vector<int> card_numbers) : winning_numbers(winning_numbers), card_numbers(card_numbers) {

        int card_points = 1;
        for (auto n : card_numbers) {
            for (auto w : winning_numbers) {
                if (n == w) {
                    matching++;
                }
            }
        }

        points = (1 << matching) >> 1;
    };
};

Card *parse_card(std::string input) {

    std::vector<std::string> n = resplit(input, std::regex(": +"));

    std::vector<std::string> v = resplit(n[1], std::regex(" \\| +"));

    std::vector<std::string> winning_numbers_str = resplit(v[0], std::regex(" +"));
    std::vector<std::string> card_numbers_str = resplit(v[1], std::regex(" +"));

    std::vector<int> winning_numbers, card_numbers;

    for (auto w : winning_numbers_str) {
        winning_numbers.push_back(std::stoi(w));
    }

    for (auto w : card_numbers_str) {
        card_numbers.push_back(std::stoi(w));
    }

    Card *c = new Card(winning_numbers, card_numbers);

    return c;
}

int main(void) {
    std::ifstream text_input("../day04.txt");
    std::string input;

    std::vector<Card *> cards;

    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            // std::cout << "Line: '" << input << "'" << std::endl;

            cards.push_back(parse_card(input));
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    // for (auto c : cards) {
    //     free(c);
    // }
    // cards.clear();
    // cards.push_back(parse_card("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"));
    // cards.push_back(parse_card("Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19"));
    // cards.push_back(parse_card("Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1"));
    // cards.push_back(parse_card("Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83"));
    // cards.push_back(parse_card("Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36"));
    // cards.push_back(parse_card("Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"));

    // Part 1 - how many winning numbers?
    int p1 = 0;
    for (auto c : cards) {
        p1 += c->points;
    }

    std::cout << "Part 1:\nAnswer: " << p1 << std::endl << std::endl;

    // Part 2 - How many total cards

    // Iterate over cards and set copies accordingly
    for (int i = 0; i < cards.size(); i++) {
        int matching = cards[i]->matching;
        int copies = cards[i]->copies;

        // std::cout << "Card: " << i + 1 << " With matching: " << matching << ", copies: " << copies << std::endl;

        for (int i2 = 1; i2 <= matching; i2++) {
            cards[i + i2]->copies += copies + 1;
        }
    }

    // Now calculate the total amount
    int p2 = 0;
    for (auto c : cards) {
        p2 += c->copies + 1;
    }

    std::cout << "Part 2:\nAnswer: " << p2 << std::endl << std::endl;

    for (auto c : cards) {
        free(c);
    }
}
