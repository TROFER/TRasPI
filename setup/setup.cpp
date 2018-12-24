#include <iostream>

#ifdef __linux__

#include <fstream>
#include <string>
#include <vector>

void hardware(bool& fail, const std::vector<std::string>& items) {
	if (!fail) {
		std::vector<std::string> not_found;
		for (std::string item : items) {
			// test each piece
		}

		if ((items.size() != 0) && (not_found.size() == 0)) {
			std::cerr << "Unable to Detect Hardware:\n";
			for (std::string s : not_found) {
				std::cerr << s << "\n";
			} std::cerr << std::endl;
			fail = true;
		}
	}
}

void package(bool& fail, const std::vector<std::string>& items) {
	if (!fail) {
		for (std::string item : items) {
			std::system(std::string("apt upgrade "+item+" -y"))
			} // if installing doesn't work, fail = true;
		}
	}
}

void install(bool& fail, const std::vector<std::string>& items) {
	if (!fail) {
		for (std::string item : items) {
			std::system(item.c_str());
		}
	}
}

bool setup(const std::string filename) {
	std::ifstream file(filename);
	std::vector<std::string> items[3];
	if (file.is_open()) {
		int type = -1;
		std::string line;
		while (std::getline(file, line)) {
			if (line[0] == '#') {
				++type;
				continue;
			}
			items[type].push_back(line);
		}

	} else {
		std::cerr << "Unable to Open File" << std::endl;
	}

	bool fail = false;
	hardware(fail, items[0]);
	package(fail, items[1]);
	install(fail, items[2]);

	if (!fail) { return true; }

	return false;
}

int main(int argc, char const *argv[]) {
	if (argc < 2) { std::cerr << "Please enter a filename" << std::endl; return -1; }
	if (setup(argv[1])) {
		std::vector<std::string> args;
		args.push_back(std::getenv("SSH_CLIENT") == nullptr ? "--ssh" : "");
		std::string cmd = "python3 main.py ";
		for (std::string arg : args) { cmd += arg+" "; }
		std::system(cmd.c_str());
	}
	return 0;
}

#elif _WIN32

int main() {
	std::cerr << "This program does not run on Windows" << std::endl;
	std::system("pause");
}

#endif // __linux__
