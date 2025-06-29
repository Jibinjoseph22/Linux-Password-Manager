## Password Manager

### Overview
This Password Manager application helps you securely manage and store your passwords. It features both a Command-Line Interface (CLI) and a Graphical User Interface (GUI) for ease of use. The application uses encryption to secure your passwords and includes functionalities such as user registration, password storage, password retrieval, and more.

---

### Command-Line Interface (CLI)

#### Features
- **User Registration:** Register a new user with name, email, phone number, username, and password.
- **User Authentication:** Log in with a username and password.
- **Password Management:** Add, view, update, delete, and search for passwords.
- **Password Generation:** Generate random passwords with customizable length.
- **Database Backup and Restore:** Backup the database to a file and restore from a backup.
- **Password Strength Checker:** Evaluate the strength of passwords to ensure they meet security requirements

#### CLI Usage
1. **Run the Application:**
    ```bash
    python3 password_manager.py
    ```
2. **Choose an Option:**
    - Sign Up: Register a new user.
    - Login: Authenticate and access the main menu.
    - Exit: Close the application.

3. **Main Menu Options:**
    - Add a new password
    - View all passwords
    - Update a password
    - Delete a password
    - Search for passwords
    - Generate a random password
    - Backup database
    - Restore database
    - Exit

#### CLI Commands
- **Generate Encryption Key:**
    ```bash
    python3 -c "from password_manager import generate_key; generate_key()"
    ```
- **Backup Database:**
    ```bash
    python3 -c "from password_manager import backup_database; backup_database()"
    ```
- **Restore Database:**
    ```bash
    python3 -c "from password_manager import restore_database; restore_database('backup_filename.db')"
    ```

---

### Graphical User Interface (GUI)

#### Features
- **User-Friendly Interface:** Easy-to-navigate interface with graphical elements.
- **Password Management:** Add, view, update, and delete passwords.
- **Password Generation:** Generate strong passwords directly from the interface.
- **Database Operations:** Backup and restore the database through graphical options.

#### GUI Usage
1. **Run the Application:**
    ```bash
    python3 gui_password_manager.py
    ```
2. **Interface Navigation:**
    - **Sign Up / Log In:** Access registration or login forms.
    - **Main Menu:** Navigate to various password management features.
    - **Password Management:** Use graphical forms to manage passwords.

3. **Options Available:**
    - Add, View, Update, Delete passwords
    - Generate passwords
    - Backup and Restore database

---

### Getting Started

1. **Install Dependencies:**
    Make sure you have the required libraries installed. You can use `pip` to install them:
    ```bash
    pip install cryptography
    ```

2. **Initialize Database:**
    The database will be initialized automatically when running the application for the first time.

3. **Generate Key:**
    A secret key will be generated for encryption if it does not already exist:
    ```bash
    python3 -c "from password_manager import generate_key; generate_key()"
    ```

4. **Run the Application:**
    - For CLI:
        ```bash
        python3 password_manager.py
        ```
    - For GUI:
        ```bash
        python3 gui_password_manager.py
        ```

---

### Contributing

Feel free to contribute to the project by submitting issues, feature requests, or pull requests. Please follow the project's code style and guidelines.

---

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
