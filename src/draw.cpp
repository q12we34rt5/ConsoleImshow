#include "PixelMatrix/PixelMatrix.h"
#include <iostream>
#include <cstdio>
#include <string>
#include <list>
#include <sstream>

struct Pixel {
    int row, col;
    RGB color;
};

enum class ENDBY {
    END_OF_FILE,
    EMPTY_LINE,
    ERROR
};

void printUsage(const std::string& program) {
    std::cerr << "Usage: " << program << " <options>\n"
              << "Draws a pixel matrix from input.\n"
              << "\n"
              << "Input format: <row> <col> <R> <G> <B>\n"
              << "  row:     row index\n"
              << "  col:     column index\n"
              << "  R, G, B: color components (0-255)\n"
              << "\n"
              << "If the input is an empty line, the current matrix will be printed and the program will wait for the next set of input.\n"
              << "The cursor position will be reset to the position when the program started.\n"
              << "\n"
              << "Options:\n"
              << "  -h, --help          Show this help message and exit\n";
}

ENDBY readPixels(std::istream& input, std::list<Pixel>& pixels) {
    std::string line;
    Pixel pixel;
    while (true) {
        if (!std::getline(input, line)) {
            return ENDBY::END_OF_FILE;
        }
        if (line.empty()) {
            return ENDBY::EMPTY_LINE;
        }
        std::istringstream iss(line);
        int err = std::sscanf(line.c_str(), "%d %d %hhu %hhu %hhu", &pixel.row, &pixel.col, &pixel.color.R, &pixel.color.G, &pixel.color.B);
        if (err != 5) {
            std::cerr << "Invalid input: " << line << std::endl;
            return ENDBY::ERROR;
        }
        pixels.push_back(pixel);
    }
}

void findMaxDimensions(const std::list<Pixel>& pixels, int& max_row, int& max_col) {
    max_row = 0;
    max_col = 0;
    for (const auto& pixel : pixels) {
        if (pixel.row > max_row) max_row = pixel.row;
        if (pixel.col > max_col) max_col = pixel.col;
    }
}

void populatePixelMatrix(PixelMatrix& pm, const std::list<Pixel>& pixels) {
    for (const auto& pixel : pixels) {
        pm[pixel.row][pixel.col].color = pixel.color;
        pm.enable(pixel.row, pixel.col);
    }
}

void displayPixelMatrix(PixelMatrix& pm) {
    std::ostringstream oss;
    oss << pm;
    std::fputs(oss.str().c_str(), stdout);
}

int main(int argc, char* argv[]) {
    if (argc > 1) {
        std::string arg = argv[1];
        if (arg == "-h" || arg == "--help") {
            printUsage(argv[0]);
            return 0;
        } else {
            std::cerr << "Unknown option: " << arg << "\n";
            printUsage(argv[0]);
            return 1;
        }
    }

    std::list<Pixel> pixels;
    while (true) {
        pixels.clear();
        ENDBY endby = readPixels(std::cin, pixels);
        if (endby == ENDBY::ERROR) {
            return 1;
        }

        int max_row = 0, max_col = 0;
        findMaxDimensions(pixels, max_row, max_col);

        PixelMatrix pm(max_row + 1, max_col + 1);
        std::fputs("\033[s", stdout);
        populatePixelMatrix(pm, pixels);

        displayPixelMatrix(pm);

        if (endby == ENDBY::END_OF_FILE) {
            break;
        } else if (endby == ENDBY::EMPTY_LINE) {
            std::fputs("\033[u", stdout);
        }
    }
    return 0;
}