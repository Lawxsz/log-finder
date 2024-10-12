#include <iostream>
#include <fstream>
#include <string>
#include <ctime>
#include <vector>
#include <windows.h>

void setColor(int textColor) {
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), textColor);
}

std::string getCurrentTime() {
    time_t now = time(0);
    tm* ltm = localtime(&now);
    char buffer[9];
    strftime(buffer, sizeof(buffer), "%H-%M-%S", ltm);
    return std::string(buffer);
}

std::string generateFilename(const std::string& searchTerm) {
    std::string currentTime = getCurrentTime();
    std::string filename = searchTerm + "_" + currentTime + ".txt";
    return filename;
}

void printCredits() {
    setColor(11);
    std::cout << "Credits:\n";
    std::cout << "Telegram: t.me/lawxsz\n";
    std::cout << "GitHub: github.com/lawxsz\n\n";
    setColor(7);
}

void searchInFile(const std::string& filePath, const std::string& searchTerm, int& foundCount) {
    std::ifstream inputFile(filePath, std::ios::in | std::ios::binary);
    std::string outputFileName = generateFilename(searchTerm);
    std::ofstream outputFile(outputFileName);

    if (!inputFile.is_open()) {
        setColor(12);
        std::cout << "Error: Could not open the file " << filePath << ".\n";
        return;
    }

    if (!outputFile.is_open()) {
        setColor(12);
        std::cout << "Error: Could not create the output file " << outputFileName << ".\n";
        inputFile.close();
        return;
    }

    setColor(10);
    std::cout << "Searching for: " << searchTerm << " in " << filePath << "\n";

    std::string line;
    while (std::getline(inputFile, line)) {
        // Check if the line contains the search term
        if (line.find(searchTerm) != std::string::npos) {
            outputFile << line << "\n";
            std::cout << "Found: " << line << "\n";
            foundCount++;
        }
    }

    inputFile.close();
    outputFile.close();

    setColor(14);
    std::cout << "Total found: " << foundCount << "\n";
}

int main() {
    printCredits();
    
    std::string searchTerm;
    std::string filePath;

    std::cout << "Enter the search term (account, url, password): ";
    std::getline(std::cin, searchTerm);

    std::cout << "Enter the path of the file to search: ";
    std::getline(std::cin, filePath);

    char continueSearch = 'y';
    
    while (continueSearch == 'y') {
        int foundAccounts = 0;
        searchInFile(filePath, searchTerm, foundAccounts);

        std::cout << "Do you want to search again? (y/n): ";
        std::cin >> continueSearch;
        std::cin.ignore();

        if (continueSearch == 'y') {
            std::cout << "Enter the search term (account, url, password): ";
            std::getline(std::cin, searchTerm);
            std::cout << "Enter the path of the file to search: ";
            std::getline(std::cin, filePath);
        }
    }

    std::cout << "Exiting program. Press Enter to close..." << std::endl;
    std::cin.get();
    return 0;
}
