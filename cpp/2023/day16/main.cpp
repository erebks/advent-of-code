#include <array>
#include <fstream>
#include <iostream>
#include <set>
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

struct Beam {
    unsigned int posx = 0;
    unsigned int posy = 0;
    char direction = 'X';
    bool done = false;

    void print() { std::cout << this->str(); };
    std::string str() { return "(" + std::to_string(posx) + ", " + std::to_string(posy) + ", dir:" + direction + ")"; };
};

Beam adjust_direction(char tile, Beam &beam) {
    Beam split_beam(beam);
    split_beam.direction = 'X';

    std::map<char, char> conv;

    switch (tile) {
    case '\\':
        conv = {
            {'N', 'W'},
            {'E', 'S'},
            {'S', 'E'},
            {'W', 'N'},
        };
        beam.direction = conv[beam.direction];
        break;
    case '/':
        conv = {
            {'N', 'E'},
            {'E', 'N'},
            {'S', 'W'},
            {'W', 'S'},
        };
        beam.direction = conv[beam.direction];
        break;
    case '|':
        if (beam.direction == 'W' || beam.direction == 'E') {
            beam.direction = 'N';
            split_beam = beam;
            split_beam.direction = 'S';
        }
        break;
    case '-':
        if (beam.direction == 'N' || beam.direction == 'S') {
            beam.direction = 'E';
            split_beam = beam;
            split_beam.direction = 'W';
        }
        break;
    case '.':
    default:
        break;
    };

    return split_beam;
}

Beam step(std::vector<std::string> floor, Beam &beam) {

    Beam new_beam;

    // std::cout << "At:" << beam.str() << " -> ";

    // Get next move
    switch (beam.direction) {
    case 'N':
        if (beam.posx == 0) {
            // std::cout << "At end" << std::endl;
            beam.done = true;
            return new_beam;
        }
        beam.posx--;
        break;
    case 'E':
        if (beam.posy >= floor[0].size() - 1) {
            // std::cout << "At end" << std::endl;
            beam.done = true;
            return new_beam;
        }
        beam.posy++;
        break;
    case 'S':
        if (beam.posx >= floor.size() - 1) {
            // std::cout << "At end" << std::endl;
            beam.done = true;
            return new_beam;
        }
        beam.posx++;
        break;
    case 'W':
        if (beam.posy == 0) {
            // std::cout << "At end" << std::endl;
            beam.done = true;
            return new_beam;
        }
        beam.posy--;
        break;
    default:
        break;
    };

    char tile = floor[beam.posx][beam.posy];

    // std::cout << "Stepping to " << beam.str() << " -> " << tile;

    new_beam = adjust_direction(tile, beam);

    // std::cout << " -> New direction: " << beam.direction;

    if (new_beam.direction != 'X') {
        // std::cout << " Beam was split";
    }

    // std::cout << std::endl;
    return new_beam;
}

bool visited(Beam beam, std::vector<Beam> visited_beams) {
    for (auto visited : visited_beams) {
        if (visited.direction == beam.direction && visited.posx == beam.posx && visited.posy == beam.posy) {
            return true;
        }
    }
    return false;
}

void print_field(std::vector<std::string> field, std::vector<Beam> visited_beams) {
    for (auto b : visited_beams) {
        switch (b.direction) {
        case 'N':
            field[b.posx][b.posy] = '^';
            break;
        case 'E':
            field[b.posx][b.posy] = '>';
            break;
        case 'S':
            field[b.posx][b.posy] = 'v';
            break;
        case 'W':
            field[b.posx][b.posy] = '<';
            break;
        };
    }

    for (auto l : field) {
        std::cout << l << std::endl;
    }
}

unsigned int shine_beam(std::vector<std::string> const floor, Beam start) {
    std::vector<Beam> beams;

    Beam v = adjust_direction(floor[start.posx][start.posy], start);
    beams.push_back(start);

    if (v.direction != 'X') {
        beams.push_back(v);
    }

    std::set<std::array<unsigned int, 2>> energized_tiles;

    std::vector<Beam> visited_beams;

    int idx = 0;
    while (idx < beams.size()) {
        Beam b = beams[idx++];

        if (visited(b, visited_beams)) {
            continue;
        }

        energized_tiles.insert({b.posx, b.posy});
        visited_beams.push_back(b);

        while (!b.done) {
            Beam v = step(floor, b);

            if (v.direction != 'X') {
                beams.push_back(v);
            }

            if (visited(b, visited_beams)) {
                // std::cout << "Beam already visited" << std::endl;
                break;
            }

            energized_tiles.insert({b.posx, b.posy});
            visited_beams.push_back(b);

            // std::cout << std::endl;
        }
    }

    // print_field(floor, visited_beams);

    return energized_tiles.size();
}

int main(void) {
    std::ifstream text_input("../day16.txt");
    std::string input;

    std::vector<std::string> floor;

    if (text_input.is_open()) {
        while (std::getline(text_input, input)) {
            floor.push_back(input);
        }
        text_input.close();
    } else {
        std::cout << "Can't open file!" << std::endl;
        return -1;
    }

    // floor = {
    //     ".|...\\....", "|.-.\\.....", ".....|-...", "........|.", "..........", ".........\\", "..../.\\\\..", ".-.-/..|..", ".|....-|.\\", "..//.|....",
    // };

    Beam beam;
    beam.direction = 'E';

    unsigned int energized = shine_beam(floor, beam);

    std::cout << "Part 1:\nAnswer: " << energized << std::endl << std::endl;

    // For part 2 the entry is on any of the edges
    // This is quite unefficient but works.
    // To improve one could save a beam with a starting point
    // and an end point and (a beam would be equal if the starting
    // point and the direction match!)

    std::set<unsigned int> configuration;
    for (auto i = 0; i < floor.size(); i++) {
        beam.direction = 'E';
        beam.posx = i;
        beam.posy = 0;
        energized = shine_beam(floor, beam);
        configuration.insert(energized);

        beam.direction = 'S';
        beam.posx = 0;
        beam.posy = i;
        energized = shine_beam(floor, beam);
        configuration.insert(energized);

        beam.direction = 'W';
        beam.posx = floor.size() - 1;
        beam.posy = i;
        energized = shine_beam(floor, beam);
        configuration.insert(energized);

        beam.direction = 'S';
        beam.posx = i;
        beam.posy = floor[0].size() - 1;
        energized = shine_beam(floor, beam);
        configuration.insert(energized);

        std::cout << "Iteration: " << i << std::endl;
    }

    std::cout << "Part 2:\nAnswer: " << *configuration.rbegin();
}
