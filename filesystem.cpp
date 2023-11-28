#include <iostream>
#include <algorithm>
#include <vector>
#include <string>
#include <filesystem>

namespace fs = std::filesystem;
class File {
    public:
        File(std::string path); // Constructor
        bool DeleteFile(std::string FileName); // Deletes a file
        bool CopyFile(std::string FileName); // Copies a file
        bool MoveFile(std::string FileName); // Moves a file
        bool RenameFile(std::string FileName); // Renames a file
        bool MassDelete(); // Deletes all files in a directory
        bool DeleteTypeInDirectory(std::string FileType); // Deletes all files in a directory with a certain type
        void DisplayFiles(); // Displays all files in a directory

    private:
        std::string path; // The path of the directory

}; 


int main() {
    return 0;
}