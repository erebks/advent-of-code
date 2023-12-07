#include <array>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <string>

// Hat-tip to https://stackoverflow.com/a/28142357
#include <regex>
#include <vector>
std::vector<std::string> resplit(const std::string &s, const std::regex &sep_regex = std::regex{"\\s+"}) {
    std::sregex_token_iterator iter(s.begin(), s.end(), sep_regex, -1);
    std::sregex_token_iterator end;
    return {iter, end};
}

enum Type {
    HIGH_CARD = 0,
    ONE_PAIR,
    TWO_PAIR,
    THREE_OF_KIND,
    FULL_HOUSE,
    FOUR_OF_KIND,
    FIVE_OF_KIND,
};

auto add_or_inc(std::map<char, int> &m, char key) {
    auto it = m.find(key);
    if (it == m.end()) {
        m.insert({key, 1});
    } else {
        it->second++;
    }
    return it;
}

Type get_type(std::string cards) {

    std::cout << "Cards: '" << cards << "' -> ";

    std::map<char, int> map_cards;

    for (auto c : cards) {
        add_or_inc(map_cards, c);
    }

    switch (map_cards.size()) {
    case 5:
        std::cout << "HIGH_CARD" << std::endl;
        return Type::HIGH_CARD;
        break;
    case 4:
        std::cout << "ONE_PAIR" << std::endl;
        return Type::ONE_PAIR;
        break;
    case 3:
        for (auto it : map_cards) {
            if (it.second == 3) {
                std::cout << "THREE_OF_KIND" << std::endl;
                return Type::THREE_OF_KIND;
            }
        }

        std::cout << "TWO_PAIR" << std::endl;
        return Type::TWO_PAIR;
        break;
    case 2:
        if (map_cards.begin()->second == 1 || map_cards.begin()->second == 4) {
            std::cout << "FOUR_OF_KIND" << std::endl;
            return Type::FOUR_OF_KIND;
        }

        std::cout << "FULL_HOUSE" << std::endl;
        return Type::FULL_HOUSE;
        break;
    case 1:
        std::cout << "FIVE_OF_KIND" << std::endl;
        return Type::FIVE_OF_KIND;
        break;
    default:
        std::cout << "Problem!" << std::endl;
        return Type::HIGH_CARD;
        break;
    }
}

struct Hand {
    std::string cards;
    int bid;
    Type type;

    Hand(std::string cards, int bid) : cards(cards), bid(bid) {
        // Determine type
        type = get_type(cards);
    };

    bool operator<(const Hand &other) const {
        std::map<char, int> conv{
            {'2', 2}, {'3', 3}, {'4', 4}, {'5', 5}, {'6', 6}, {'7', 7}, {'8', 8}, {'9', 9}, {'T', 10}, {'J', 11}, {'Q', 12}, {'K', 13}, {'A', 14},
        };
        if (this->type == other.type) {
            std::cout << "\tTypes match!" << std::endl;
            // Iterate over cards
            for (int i = 0; i < this->cards.size(); i++) {
                std::cout << "\tCompare: " << this->cards[i] << " vs. " << other.cards[i] << " ";
                if (conv.at(this->cards[i]) == conv.at(other.cards[i])) {
                    std::cout << "Equal" << std::endl;
                    continue;
                }
                if (conv.at(this->cards[i]) < conv.at(other.cards[i])) {
                    std::cout << " < " << std::endl;
                    return true;
                } else {
                    std::cout << " > " << std::endl;
                    return false;
                }
            }
            std::cout << "All equal" << std::endl;
            return false;
        } else {
            return (this->type < other.type);
        }
    };

    bool operator>(const Hand &other) const { return !((*this) < other); };
};

Type get_type_p2(std::string cards) {

    std::cout << "Cards: '" << cards << "' -> ";

    std::map<char, int> map_cards;

    int j = 0;
    for (auto c : cards) {
        add_or_inc(map_cards, c);
        if (c == 'J') {
            j++;
        }
    }

    map_cards.erase('J');

    auto max = map_cards.begin();

    // Just add J's to the highest number?
    for (auto it = map_cards.begin(); it != map_cards.end(); it++) {
        if (it->second > max->second) {
            max = it;
        }
    }
    max->second = max->second + j;

    switch (map_cards.size()) {
    case 5:
        std::cout << "HIGH_CARD" << std::endl;
        return Type::HIGH_CARD;
        break;
    case 4:
        std::cout << "ONE_PAIR" << std::endl;
        return Type::ONE_PAIR;
        break;
    case 3:
        for (auto it : map_cards) {
            if (it.second == 3) {
                std::cout << "THREE_OF_KIND" << std::endl;
                return Type::THREE_OF_KIND;
            }
        }
        std::cout << std::endl;

        std::cout << "TWO_PAIR" << std::endl;
        return Type::TWO_PAIR;
        break;
    case 2:
        for (auto it : map_cards) {
            if (it.second == 4) {
                std::cout << "FOUR_OF_KIND" << std::endl;
                return Type::FOUR_OF_KIND;
            }
        }

        std::cout << "FULL_HOUSE" << std::endl;
        return Type::FULL_HOUSE;
        break;

    default:
    case 1:
    case 0:
        std::cout << "FIVE_OF_KIND" << std::endl;
        return Type::FIVE_OF_KIND;
        break;
    }
}

struct Hand_p2 {
    std::string cards;
    int bid;
    Type type;

    Hand_p2(std::string cards, int bid) : cards(cards), bid(bid) {
        // Determine type
        type = get_type_p2(cards);
    };

    bool operator<(const Hand_p2 &other) const {
        std::map<char, int> conv{
            {'J', 1}, {'2', 2}, {'3', 3}, {'4', 4}, {'5', 5}, {'6', 6}, {'7', 7}, {'8', 8}, {'9', 9}, {'T', 10}, {'Q', 12}, {'K', 13}, {'A', 14},
        };
        if (this->type == other.type) {
            std::cout << "\tTypes match!" << std::endl;
            // Iterate over cards
            for (int i = 0; i < this->cards.size(); i++) {
                std::cout << "\tCompare: " << this->cards[i] << " vs. " << other.cards[i] << " ";
                if (conv.at(this->cards[i]) == conv.at(other.cards[i])) {
                    std::cout << "Equal" << std::endl;
                    continue;
                }
                if (conv.at(this->cards[i]) < conv.at(other.cards[i])) {
                    std::cout << " < " << std::endl;
                    return true;
                } else {
                    std::cout << " > " << std::endl;
                    return false;
                }
            }
            std::cout << "All equal" << std::endl;
            return false;
        } else {
            return (this->type < other.type);
        }
    };
    bool operator>(const Hand_p2 &other) const { return !((*this) < other); };
};

Hand parse_input(std::string str) {

    std::vector<std::string> v = resplit(str, std::regex(" +"));

    Hand h(v[0], std::stoi(v[1]));

    return h;
}

Hand_p2 parse_input_p2(std::string str) {

    std::vector<std::string> v = resplit(str, std::regex(" +"));

    Hand_p2 h(v[0], std::stoi(v[1]));

    return h;
}

int main(void) {
    std::ifstream text_input("../day07.txt");
    std::string input;

    std::set<Hand> hands;
    std::set<Hand_p2> hands_p2;

    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            hands.insert(parse_input(input));
            hands_p2.insert(parse_input_p2(input));
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    // std::cout << "Test input: " << std::endl;
    // std::vector<std::string> str = {
    //     "32T3K 765", "T55J5 684", "KK677 28", "KTJJT 220", "QQQJA 483",
    // };

    // hands.clear();
    // hands_p2.clear();

    // for (auto s : str) {
    //     hands.insert(parse_input(s));
    //     hands_p2.insert(parse_input_p2(s));
    // }

    int winnings = 0;
    int i = 1;
    for (auto h : hands) {
        std::cout << h.cards << std::endl;
        winnings += (i++) * h.bid;
    }
    std::cout << "Part 1:\nAnswer: " << winnings << std::endl << std::endl;

    // Part 2 -> J are Joker...
    winnings = 0;
    i = 1;
    for (auto h : hands_p2) {
        std::cout << "Hand: " << h.cards << " -> " << h.type << std::endl;
        winnings += (i++) * h.bid;
    }

    std::cout << "Part 2:\nAnswer: " << winnings << std::endl << std::endl;
}
