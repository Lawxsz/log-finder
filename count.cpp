#include <iostream>
#include <filesystem>
#include <fstream>
#include <string>

namespace fs = std::filesystem;

int count_lines_in_file(const fs::path& file_path) {
    std::ifstream file(file_path);
    int line_count = 0;
    std::string line;

    while (std::getline(file, line)) {
        line_count++;
    }

    return line_count;
}

int main() {
    std::string folder_path = "cloud"; 
    int total_lines = 0;

    try {
        for (const auto& entry : fs::directory_iterator(folder_path)) {
            if (entry.path().extension() == ".txt") {
                total_lines += count_lines_in_file(entry.path());
            }
        }

        std::cout << total_lines << std::endl;

    } catch (const fs::filesystem_error& e) {
        std::cerr << "Error al acceder a la carpeta: " << e.what() << std::endl;
        return 1; 
    }

    return 0;  
}
