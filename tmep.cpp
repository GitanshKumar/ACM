#include <iostream>
#include <string>
#include <cctype>

bool isPasswordValid(const std::string& password) {
    if (password.length() < 4 || std::isdigit(password[0])) {
        return false;
    }

    bool hasUpperCase = false;
    bool hasDigit = false;

    for (char ch : password) {
        if (std::isupper(ch)) {
            hasUpperCase = true;
        } else if (std::isdigit(ch)) {
            hasDigit = true;
        }
        else if (ch == ' ' || ch == ' ') {
            return false;
        }
    }

    return hasUpperCase && hasDigit;
}

int main() {
    std::string password;

    std::cout << "Enter your password: ";
    std::cin >> password;

    if (isPasswordValid(password)) {
        std::cout << "Password is valid." << std::endl;
    } else {
        std::cout << "Password is invalid. It should have at least 4 characters, "
                  << "at least one uppercase letters, and at least one digit, without spaces or '/' and first character should not be number"
                  << std::endl;
    }

    return 0;
}
