#include <fstream>
#include <iostream>
#include <map>
#include <ostream>
#include <set>
#include <sstream>
#include <string>
#include <type_traits>
#include <vector>

struct City {
    // Connetions to other cities
    std::string name{};
    std::map<City *, unsigned int> connections{};

    City(){};
    City(std::string name) { this->name = name; };

    void add_connection(City *city, unsigned int distance) { connections.insert({city, distance}); }

    bool operator<(const City &other) const { return this->name < other.name; };
    bool operator==(const City &other) const { return other.name == this->name; };
    bool operator!=(const City &other) const { return !operator==(other); };

    std::string serialize_connections() const {
        std::string out("(");
        for (auto &c : connections) {
            out += " -> " + c.first->name + ": " + std::to_string(c.second);
        }
        out += ")";
        return out;
    };

    friend std::ostream &operator<<(std::ostream &os, const City &obj) {

        os << "'" << obj.name << "' Connections: " << obj.serialize_connections();
        return os;
    }
};

// Hat tip to https://stackoverflow.com/a/46931770
std::vector<std::string> split(const std::string &s, char delim) {
    std::vector<std::string> result;
    std::stringstream ss(s);
    std::string item;

    while (getline(ss, item, delim)) {
        result.push_back(item);
    }

    return result;
}

void parse_input(std::string input, std::map<std::string, City *> *cities) {
    std::vector<std::string> input_split = split(input, ' ');
    std::string start_city = input_split[0];
    std::string dest_city = input_split[2];
    unsigned int distance = std::stoi(input_split[4]);

    std::cout << "start: " << start_city << ", Distance: " << distance << ", End: " << dest_city << std::endl;

    City *start = new City(start_city);
    City *end = new City(dest_city);

    auto it = cities->find(start_city);
    if (it != cities->end()) {
        std::cout << *(it->second) << " found\n";
        start = it->second;
    } else {
        start = new City(start_city);
    }

    it = cities->find(dest_city);
    if (it != cities->end()) {
        std::cout << *(it->second) << " found\n";
        end = it->second;
    } else {
        end = new City(dest_city);
    }

    cities->insert({start_city, start});
    cities->insert({dest_city, end});

    start->add_connection(end, distance);
    end->add_connection(start, distance);

    // std::cout << "Start: " << *start << std::endl;
}

std::vector<unsigned int> visit_next(City *current, std::map<std::string, City *> visited, unsigned int cost) {

    std::vector<unsigned int> costs{};

    City *n{nullptr};

    std::cout << "New instance -> visited: " << std::endl;
    for (auto v : visited) {
        std::cout << v.first << ", ";
    }
    std::cout << std::endl;

    // visit next city which is NOT in visited
    for (auto &next : current->connections) {
        unsigned int n_cost = cost;
        auto it = visited.find(next.first->name);
        if (it == visited.end()) {
            // Not visited -> let's visit

            // Copy visited list
            std::map<std::string, City *> n_visited(visited);

            n_cost += next.second;
            n = next.first;

            std::cout << "Visiting: " << *n << std::endl;

            n_visited.insert({n->name, n});

            for (auto &c : visit_next(n, n_visited, n_cost)) {
                costs.push_back(c);
            }

            if (visited.size() == n->connections.size()) {
                costs.push_back(n_cost);
            }
        }
    }

    return costs;

    // if (n == nullptr) {
    //     std::cout << "No more neighbors to visit, total cost: " << cost << std::endl;
    //     return cost;
    // }

    //    return visit_next(n, visited, cost);
}

int main(void) {
    std::ifstream text_input("../day09.txt");
    std::string input;

    std::map<std::string, City *> cities;

    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            std::cout << "Line: '" << input << "'" << std::endl;

            parse_input(input, &cities);

            std::cout << "Cities:\n";
            for (auto &c : cities) {
                std::cout << "\t" << *(c.second) << std::endl;
            }
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    std::cout << "Part 1:\n";

    // cities.clear();
    // parse_input("London to Dublin = 464", &cities);
    // parse_input("London to Belfast = 518", &cities);
    // parse_input("Dublin to Belfast = 141", &cities);

    std::cout << "Cities:\n";
    for (auto &c : cities) {
        std::cout << "\t" << *(c.second) << std::endl;
    }
    std::cout << std::endl;

    std::set<unsigned int> costs;

    for (auto &c : cities) {
        std::map<std::string, City *> visited{{c.first, c.second}};
        std::cout << c.first << std::endl;

        for (auto &c : visit_next(c.second, visited, 0)) {
            costs.insert(c);
        }
    }

    std::cout << "Answer: " << *costs.begin() << std::endl;

    std::cout << "Part 2\nAnswer: " << *costs.rbegin();

    // Free all cities!

    for (auto &c : cities) {
        free(c.second);
    }
}
