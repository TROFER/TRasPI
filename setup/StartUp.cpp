#include <iostream>
#include <fstream>
#include <string>
#include <vector>

bool sys_call(const std::string filename) {
	std::vector<std::string> cmd;
	std::ifstream file(filename);
	if (file.is_open()) {
		std::string line;
		while (std::getline(file, line)) {
			cmd.push_back(line);
		}
	} else {
		std::cerr << "Unable to Open File: " << filename << std::endl;
		return false;
	}
	for (std::string c : cmd) {
		std::system(c.c_str());
	}
	return true;
}

int main(int argc, char const *argv[]) {
	if (argc < 2) { std::cerr << "Requires at least 1 argument" << std::endl; return -1; }
	sys_call(argv[1]);
	return 0;
}