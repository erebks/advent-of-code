#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <fstream>
#include <iostream>
#include <map>
#include <regex>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>

struct Signal {
    std::string name{};
    bool stable = false;
    uint16_t value = 0;

    Signal(){};
    Signal(std::string str) {
        name = str;
        // Check if it can be converted to a number
        try {
            size_t pos;
            value = std::stoi(str, &pos);
            stable = true;
        } catch (std::invalid_argument const &ex) {
            value = 0;
            stable = false;
        }
    };

    bool is_stable() { return stable; };

    void set(uint16_t value) {
        this->value = value;
        stable = true;
    };
};

enum Operation { SOURCE, AND, OR, LSHIFT, RSHIFT, NOT };

// Hat-tip to https://stackoverflow.com/a/28142357
std::vector<std::string> resplit(const std::string &s, const std::regex &sep_regex = std::regex{"\\s+"}) {
    std::sregex_token_iterator iter(s.begin(), s.end(), sep_regex, -1);
    std::sregex_token_iterator end;
    return {iter, end};
}

struct Gate {
    Signal *in1{};
    Signal *in2{};

    Operation op{};
    Signal *out{};

    bool processed = false;

    Gate(){};

    Gate(Signal *in1, Signal *in2, Operation op, Signal *out) : in1(in1), in2(in2), op(op), out(out){};

    bool inputs_stable(void) {
        switch (op) {
        case Operation::OR:
        case Operation::AND:
        case Operation::LSHIFT:
        case Operation::RSHIFT:
            return in1->is_stable() && in2->is_stable();
            break;
        case Operation::NOT:
        case Operation::SOURCE:
            return in1->is_stable();
            break;
        }
    };

    uint16_t process(void) {
        switch (op) {
        case Operation::OR:
            out->set(in1->value | in2->value);
            break;
        case Operation::AND:
            out->set(in1->value & in2->value);
            break;
        case Operation::LSHIFT:
            out->set(in1->value << in2->value);
            break;
        case Operation::RSHIFT:
            out->set(in1->value >> in2->value);
            break;
        case Operation::NOT:
            out->set(~in1->value);
            break;
        case Operation::SOURCE:
            out->set(in1->value);
            break;
        }
        processed = true;
        return out->value;
    };
};

int main(void) {
    std::ifstream text_input("../day07.txt");
    std::string input;

    std::map<std::string, Signal> signals{};
    std::map<std::string, Gate> gates{};
    std::map<std::string, Gate> gates_stable{};

    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            // Parse signals and driver
            std::cout << "Line: '" << input << "'" << std::endl;

            // Add 3 signals

            Operation op{};
            Gate g{};

            std::smatch re_match{};

            if (std::regex_search(input, re_match, std::regex("AND"))) {
                std::vector<std::string> v = resplit(input, std::regex{" "});

                op = Operation::AND;

                signals.insert({v[0], Signal(v[0])});
                Signal *in1 = &(signals.find(v[0])->second);

                signals.insert({v[2], Signal(v[2])});
                Signal *in2 = &(signals.find(v[2])->second);

                signals.insert({v[4], Signal(v[4])});
                Signal *out = &(signals.find(v[4])->second);

                g = Gate(in1, in2, op, out);
                gates.insert({out->name, g});

            } else if (std::regex_search(input, re_match, std::regex("OR"))) {
                std::vector<std::string> v = resplit(input, std::regex{" "});

                op = Operation::OR;

                signals.insert({v[0], Signal(v[0])});
                Signal *in1 = &(signals.find(v[0])->second);

                signals.insert({v[2], Signal(v[2])});
                Signal *in2 = &(signals.find(v[2])->second);

                signals.insert({v[4], Signal(v[4])});
                Signal *out = &(signals.find(v[4])->second);

                g = Gate(in1, in2, op, out);
                gates.insert({out->name, g});

            } else if (std::regex_search(input, re_match, std::regex("LSHIFT"))) {
                std::vector<std::string> v = resplit(input, std::regex{" "});

                op = Operation::LSHIFT;

                signals.insert({v[0], Signal(v[0])});
                Signal *in1 = &(signals.find(v[0])->second);

                signals.insert({v[2], Signal(v[2])});
                Signal *in2 = &(signals.find(v[2])->second);

                if (!in2->is_stable()) {
                    std::cout << "Invalid LSHIFT " << input << std::endl;
                }

                signals.insert({v[4], Signal(v[4])});
                Signal *out = &(signals.find(v[4])->second);

                g = Gate(in1, in2, op, out);
                gates.insert({out->name, g});

            } else if (std::regex_search(input, re_match, std::regex("RSHIFT"))) {
                std::vector<std::string> v = resplit(input, std::regex{" "});

                op = Operation::RSHIFT;

                signals.insert({v[0], Signal(v[0])});
                Signal *in1 = &(signals.find(v[0])->second);

                signals.insert({v[2], Signal(v[2])});
                Signal *in2 = &(signals.find(v[2])->second);

                if (!in2->is_stable()) {
                    std::cout << "Invalid RSHIFT " << input << std::endl;
                }

                signals.insert({v[4], Signal(v[4])});
                Signal *out = &(signals.find(v[4])->second);

                g = Gate(in1, in2, op, out);
                gates.insert({out->name, g});

            } else if (std::regex_search(input, re_match, std::regex("NOT"))) {
                std::vector<std::string> v = resplit(input, std::regex{" "});
                op = Operation::NOT;

                signals.insert({v[1], Signal(v[1])});
                Signal *in1 = &(signals.find(v[1])->second);

                signals.insert({std::string("0"), Signal(std::string("0"))});
                Signal *in2 = &(signals.find(std::string("0"))->second);

                signals.insert({v[3], Signal(v[3])});
                Signal *out = &(signals.find(v[3])->second);

                g = Gate(in1, in2, op, out);
                gates.insert({out->name, g});

            } else {
                std::vector<std::string> v = resplit(input, std::regex{" "});
                op = Operation::SOURCE;

                signals.insert({v[0], Signal(v[0])});
                Signal *in1 = &(signals.find(v[0])->second);

                signals.insert({std::string("0"), Signal(std::string("0"))});
                Signal *in2 = &(signals.find(std::string("0"))->second);

                signals.insert({v[2], Signal(v[2])});
                Signal *out = &(signals.find(v[2])->second);

                g = Gate(in1, in2, op, out);
                gates.insert({out->name, g});
            }

            std::cout << "\tlen gates: " << gates.size() << " len signals: " << signals.size() << std::endl;

            std::cout << "\tin1: " << g.in1->name << " (" << g.in1->value << ")"
                      << " in2: " << g.in2->name << " (" << g.in2->value << ")"
                      << " op: " << g.op << " out: " << g.out->name << " (" << g.out->value << ")" << std::endl;
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    std::cout << "Part 1:" << std::endl;

    while (gates.size() > 0) {
        // Iterate over gates to find processable gate
        for (auto &g : gates) {
            if (g.second.inputs_stable()) {
                g.second.process();
                // Set processed gate to done
                gates_stable.insert(g);
                gates.erase(g.first);
                break;
            }
        }
    }
    uint16_t signal_a_part1 = signals.find(std::string("a"))->second.value;

    std::cout << "Answer: " << signal_a_part1 << std::endl;

    std::ifstream text_input_2("../day07.txt");

    signals.clear();
    gates.clear();
    gates_stable.clear();

    if (text_input_2.is_open()) {
        while (std::getline(text_input_2, input)) {
            // Parse signals and driver
            std::cout << "Line: '" << input << "'" << std::endl;

            // Add 3 signals

            Operation op{};
            Gate g{};

            std::smatch re_match{};

            if (std::regex_search(input, re_match, std::regex("AND"))) {
                std::vector<std::string> v = resplit(input, std::regex{" "});

                op = Operation::AND;

                signals.insert({v[0], Signal(v[0])});
                Signal *in1 = &(signals.find(v[0])->second);

                signals.insert({v[2], Signal(v[2])});
                Signal *in2 = &(signals.find(v[2])->second);

                signals.insert({v[4], Signal(v[4])});
                Signal *out = &(signals.find(v[4])->second);

                g = Gate(in1, in2, op, out);
                gates.insert({out->name, g});

            } else if (std::regex_search(input, re_match, std::regex("OR"))) {
                std::vector<std::string> v = resplit(input, std::regex{" "});

                op = Operation::OR;

                signals.insert({v[0], Signal(v[0])});
                Signal *in1 = &(signals.find(v[0])->second);

                signals.insert({v[2], Signal(v[2])});
                Signal *in2 = &(signals.find(v[2])->second);

                signals.insert({v[4], Signal(v[4])});
                Signal *out = &(signals.find(v[4])->second);

                g = Gate(in1, in2, op, out);
                gates.insert({out->name, g});

            } else if (std::regex_search(input, re_match, std::regex("LSHIFT"))) {
                std::vector<std::string> v = resplit(input, std::regex{" "});

                op = Operation::LSHIFT;

                signals.insert({v[0], Signal(v[0])});
                Signal *in1 = &(signals.find(v[0])->second);

                signals.insert({v[2], Signal(v[2])});
                Signal *in2 = &(signals.find(v[2])->second);

                if (!in2->is_stable()) {
                    std::cout << "Invalid LSHIFT " << input << std::endl;
                }

                signals.insert({v[4], Signal(v[4])});
                Signal *out = &(signals.find(v[4])->second);

                g = Gate(in1, in2, op, out);
                gates.insert({out->name, g});

            } else if (std::regex_search(input, re_match, std::regex("RSHIFT"))) {
                std::vector<std::string> v = resplit(input, std::regex{" "});

                op = Operation::RSHIFT;

                signals.insert({v[0], Signal(v[0])});
                Signal *in1 = &(signals.find(v[0])->second);

                signals.insert({v[2], Signal(v[2])});
                Signal *in2 = &(signals.find(v[2])->second);

                if (!in2->is_stable()) {
                    std::cout << "Invalid RSHIFT " << input << std::endl;
                }

                signals.insert({v[4], Signal(v[4])});
                Signal *out = &(signals.find(v[4])->second);

                g = Gate(in1, in2, op, out);
                gates.insert({out->name, g});

            } else if (std::regex_search(input, re_match, std::regex("NOT"))) {
                std::vector<std::string> v = resplit(input, std::regex{" "});
                op = Operation::NOT;

                signals.insert({v[1], Signal(v[1])});
                Signal *in1 = &(signals.find(v[1])->second);

                signals.insert({std::string("0"), Signal(std::string("0"))});
                Signal *in2 = &(signals.find(std::string("0"))->second);

                signals.insert({v[3], Signal(v[3])});
                Signal *out = &(signals.find(v[3])->second);

                g = Gate(in1, in2, op, out);
                gates.insert({out->name, g});

            } else {
                std::vector<std::string> v = resplit(input, std::regex{" "});
                op = Operation::SOURCE;

                signals.insert({v[0], Signal(v[0])});
                Signal *in1 = &(signals.find(v[0])->second);

                signals.insert({std::string("0"), Signal(std::string("0"))});
                Signal *in2 = &(signals.find(std::string("0"))->second);

                signals.insert({v[2], Signal(v[2])});
                Signal *out = &(signals.find(v[2])->second);

                g = Gate(in1, in2, op, out);
                gates.insert({out->name, g});
            }

            std::cout << "\tlen gates: " << gates.size() << " len signals: " << signals.size() << std::endl;

            std::cout << "\tin1: " << g.in1->name << " (" << g.in1->value << ")"
                      << " in2: " << g.in2->name << " (" << g.in2->value << ")"
                      << " op: " << g.op << " out: " << g.out->name << " (" << g.out->value << ")" << std::endl;
        }
        text_input_2.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    // Set signal b to what signal a was in part 1

    gates.find(std::string("b"))->second.in1->set(signal_a_part1);

    std::cout << "Part 2:" << std::endl;

    while (gates.size() > 0) {
        // Iterate over gates to find processable gate
        for (auto &g : gates) {
            if (g.second.inputs_stable()) {
                g.second.process();
                // Set processed gate to done
                gates_stable.insert(g);
                gates.erase(g.first);
                break;
            }
        }
    }

    std::cout << "Answer: " << signals.find(std::string("a"))->second.value << std::endl;
}
