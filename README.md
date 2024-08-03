# Password Manager

## Overview

This Password Manager is a command-line tool that allows users to securely store and manage their passwords. It uses encryption to protect passwords and offers features like user registration, authentication, password management, and database backup/restore.

## Features

- **User Registration**: Allows users to sign up with a name, email, phone number, username, and password.
- **User Authentication**: Validates user credentials and provides access to the password manager.
- **Password Management**:
  - Add new passwords
  - View all stored passwords
  - Update existing passwords
  - Delete passwords
  - Search passwords by service or username
- **Password Generation**: Generate random passwords of specified length.
- **Database Management**:
  - Backup the database to a file
  - Restore the database from a backup file
- **Password Strength Checker**: Checks the strength of passwords based on length and complexity.

## Technologies Used

- **Python**: Programming language used to implement the application.
- **SQLite**: Database used to store user and password data.
- **Cryptography**: Used for password encryption and decryption.
- **ANSI Color Codes**: For adding color to console output.

## Getting Started

### Prerequisites

- Python 3.x
- `cryptography` library (Install via `pip install cryptography`)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/password-manager.git
    ```
2. Navigate to the project directory:
    ```bash
    cd password-manager
    ```

3. Install the required dependencies:
    ```bash
    pip install cryptography
    ```

### Usage

1. **Initialize the database and generate a key (if not already present):**
    ```bash
    python password_manager.py
    ```

2. **Run the application:**
    ```bash
    python password_manager.py
    ```

3. **Follow the on-screen prompts to use the application:**
    - **Sign Up**: Register a new user.
    - **Login**: Log in to the application.
    - **Main Menu**: Access password management features, backup/restore options, and more.

### Commands

- **Sign Up**: Register a new user with required details.
- **Login**: Authenticate with your username and password.
- **Add a New Password**: Store a new password for a specific service.
- **View All Passwords**: List all passwords stored for the logged-in user.
- **Update a Password**: Modify an existing password entry.
- **Delete a Password**: Remove a password entry.
- **Search for Passwords**: Search passwords by service name or username.
- **Generate a Random Password**: Create a random password of desired length.
- **Backup Database**: Create a backup of the current database.
- **Restore Database**: Restore the database from a backup file.

## Contributing

Feel free to contribute to this project by submitting issues, pull requests, or suggestions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Cryptography Library](https://cryptography.io/)
- Python and its community for providing a robust platform for development.

## Contact

For any questions or feedback, you can reach me at: [your-email@example.com]

