#include <cstddef>
#include <fstream>
#include <iostream>
#include <map>
#include <memory>
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

struct Rule {
    char a;
    char op;
    int b;
    std::string result;

    bool apply(std::map<char, int> m) {

        auto it = m.find(a);
        if (it == m.end()) {
            // Problem!
            std::cout << "Can't find '" << a << "' in map!" << std::endl;
            return false;
        }

        switch (op) {
        case '<':
            return it->second < b;
            break;
        case '>':
            return it->second > b;
            break;
        default:
            // Problem!
            std::cout << "Undefined operator '" << op << "'!" << std::endl;
            return false;
            break;
        };
    }
};

struct Workflow {
    std::vector<Rule> rules;
    std::string def;

    std::string work(std::map<char, int> m) {
        for (auto it = rules.begin(); it != rules.end(); it++) {
            if (it->apply(m)) {
                return it->result;
            }
        }
        return def;
    };
};

void parse_line(std::string in, std::map<std::string, Workflow> &workflows, std::vector<std::map<char, int>> &parts) {
    if (in[0] == '{') {
        std::map<char, int> part;

        in = in.substr(1, in.size() - 2);

        std::cout << "In: " << in << " -> ";

        // Part
        std::vector<std::string> v = resplit(in, std::regex(","));

        for (auto category : v) {
            std::cout << category << ", ";
            std::vector<std::string> c = resplit(category, std::regex("="));
            part.insert({c[0][0], std::stoi(c[1])});
        }
        std::cout << std::endl;

        parts.push_back(part);

    } else {
        std::vector<std::string> v = resplit(in, std::regex("\\{"));
        std::string name = v[0];

        std::cout << "New workflow, name: " << name << ", instructions: " << v[1].substr(0, v[1].size() - 1) << std::endl;
        std::vector<std::string> instructions = resplit(v[1].substr(0, v[1].size() - 1), std::regex(","));

        Workflow w;

        // Very ugly but gets the job done
        for (auto i : instructions) {
            // Find if > or <
            char op = 0;
            for (auto c : i) {
                if (c == '<' || c == '>') {
                    op = c;
                    break;
                }
            }

            std::vector<std::string> split = resplit(i, std::regex("(<|>|:)"));

            std::cout << "Split: ";
            for (auto s : split) {
                std::cout << s << ",";
            }
            std::cout << std::endl;

            if (split.size() == 1) {
                w.def = split[0];
            } else {
                Rule r;
                r.a = split[0][0];
                r.b = std::stoi(split[1]);
                r.op = op;
                r.result = split[2];
                w.rules.push_back(r);
            }
        }
        workflows.insert({name, w});
    }
}

bool is_part_accepted(std::map<std::string, Workflow> workflows, std::map<char, int> part) {

    // print part
    for (auto p : part) {
        std::cout << p.first << "=" << p.second << std::endl;
    }

    // Start at 'in'
    auto in = workflows.at("in");

    std::string next = in.work(part);

    while (next != "R" && next != "A") {
        auto it = workflows.at(next);
        next = it.work(part);
    }

    return next == "A";
}

int main(void) {
    std::ifstream text_input("../day19.txt");
    std::string input;
    std::map<std::string, Workflow> workflows;
    std::vector<std::map<char, int>> parts;

    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            std::cout << "Line: '" << input << "'" << std::endl;
            if (input != "")
                parse_line(input, workflows, parts);
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    // workflows.clear();
    // parts.clear();
    // std::vector<std::string> str = {"px{a<2006:qkq,m>2090:A,rfg}",
    //                                 "pv{a>1716:R,A}",
    //                                 "lnx{m>1548:A,A}",
    //                                 "rfg{s<537:gd,x>2440:R,A}",
    //                                 "qs{s>3448:A,lnx}",
    //                                 "qkq{x<1416:A,crn}",
    //                                 "crn{x>2662:A,R}",
    //                                 "in{s<1351:px,qqz}",
    //                                 "qqz{s>2770:qs,m<1801:hdj,R}",
    //                                 "gd{a>3333:R,R}",
    //                                 "hdj{m>838:A,pv}",
    //                                 "{x=787,m=2655,a=1222,s=2876}",
    //                                 "{x=1679,m=44,a=2067,s=496}",
    //                                 "{x=2036,m=264,a=79,s=2244}",
    //                                 "{x=2461,m=1339,a=466,s=291}",
    //                                 "{x=2127,m=1623,a=2188,s=1013}"};

    // for (auto s : str) {
    //     parse_line(s, workflows, parts);
    // }

    unsigned long p1 = 0;

    // Iterate over parts
    for (auto part : parts) {
        if (is_part_accepted(workflows, part)) {
            p1 += part.at('x');
            p1 += part.at('m');
            p1 += part.at('a');
            p1 += part.at('s');
        }
    }

    std::cout << "Part 1:\nAnswer: " << p1 << std::endl << std::endl;
}
