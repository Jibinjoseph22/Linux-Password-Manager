import os
import shutil
import sqlite3
import random
import string
import time
from datetime import datetime
from cryptography.fernet import Fernet, InvalidToken
import re

# ANSI color codes
class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Logo for Password Manager with Boy Thinking (colored)
def print_logo():
    logo = f"""
    {colors.OKBLUE}         _.-^^---....,,--{colors.ENDC}
    {colors.OKBLUE}     _--                  --_{colors.ENDC}
    {colors.OKGREEN}    <          {colors.BOLD}Password Manager{colors.ENDC}          >
    {colors.OKBLUE}     \._                   _./{colors.ENDC}
    {colors.OKBLUE}        ```--. . , ; .--'''{colors.ENDC}
    {colors.WARNING}              | |   |{colors.ENDC}
    {colors.WARNING}           .-=||  | |=-.{colors.ENDC}
    {colors.WARNING}           `-=#$%&%$#=-'{colors.ENDC}
    {colors.WARNING}              | ;  :|{colors.ENDC}
    """
    print(logo)

# Initialize the database
def init_db():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS passwords
                      (id INTEGER PRIMARY KEY, user_id INTEGER, service TEXT, username TEXT, password TEXT,
                      FOREIGN KEY (user_id) REFERENCES users(id))''')
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY, name TEXT, email TEXT, phone TEXT, username TEXT UNIQUE, password TEXT)''')
    conn.commit()
    conn.close()

# Generate and save the encryption key
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Load the encryption key
def load_key():
    return open("secret.key", "rb").read()

# Encrypt the password
def encrypt_password(password, key):
    f = Fernet(key)
    return f.encrypt(password.encode())

# Decrypt the password
def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    try:
        return f.decrypt(encrypted_password).decode()
    except InvalidToken:
        return None

# Add a new user
def add_user(name, email, phone, username, password):
    key = load_key()
    encrypted_password = encrypt_password(password, key)
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f"INSERT INTO users (name, email, phone, username, password) VALUES (?, ?, ?, ?, ?)",
                       (name, email, phone, username, encrypted_password))
        conn.commit()
        print(f"{colors.OKGREEN}User registered successfully!{colors.ENDC}")
        main()
    except sqlite3.IntegrityError:
        print(f"{colors.FAIL}Username already exists. Please choose a different username.{colors.ENDC}")
        main()
    conn.close()

# Authenticate user
def authenticate_user(username, password):
    key = load_key()
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, password FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()
    
    if result is None:
        return False, None
    user_id, stored_encrypted_password = result
    stored_password = decrypt_password(stored_encrypted_password, key)
    
    if stored_password == password:
        return True, user_id
    else:
        return False, None

# Add a new password
def add_password(user_id, service, username, password):
    key = load_key()
    encrypted_password = encrypt_password(password, key)
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    
    # Check if the entry already exists
    cursor.execute(f"SELECT * FROM passwords WHERE user_id=? AND service=? AND username=?", (user_id, service, username))
    result = cursor.fetchone()
    
    if result:
        print(f"{colors.FAIL}Password for this service and username already exists.{colors.ENDC}")
    else:
        cursor.execute(f"INSERT INTO passwords (user_id, service, username, password) VALUES (?, ?, ?, ?)",
                       (user_id, service, username, encrypted_password))
        conn.commit()
        print(f"{colors.OKGREEN}Password added successfully!{colors.ENDC}")
    
    conn.close()

# View all passwords
def view_passwords(user_id):
    key = load_key()
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM passwords WHERE user_id=?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        print(f"{colors.WARNING}No passwords stored yet.{colors.ENDC}")
    else:
        print(f"{colors.OKBLUE}Listing all passwords:{colors.ENDC}")
        for row in rows:
            decrypted_password = decrypt_password(row[4], key)
            if decrypted_password:
                print(f"ID: {row[0]}, Service: {row[2]}, Username: {row[3]}, Password: {decrypted_password}")
            else:
                print(f"ID: {row[0]}, Service: {row[2]}, Username: {row[3]}, Password: {colors.FAIL}Error: Invalid encryption key or tampered data.{colors.ENDC}")

def update_password(user_id, service, username, new_password):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    
    # Check if the entry exists
    cursor.execute(f"SELECT * FROM passwords WHERE user_id=? AND service=? AND username=?", (user_id, service, username))
    result = cursor.fetchone()
    
    if not result:
        print(f"{colors.FAIL}No entry found for the specified service and username.{colors.ENDC}")
    else:
        key = load_key()
        encrypted_password = encrypt_password(new_password, key)
        cursor.execute(f"UPDATE passwords SET password=? WHERE user_id=? AND service=? AND username=?",
                       (encrypted_password, user_id, service, username))
        conn.commit()
        print(f"{colors.OKGREEN}Password updated successfully!{colors.ENDC}")
    
    conn.close()

# Delete a password
def delete_password(user_id, service, username):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM passwords WHERE user_id=? AND service=? AND username=?", (user_id, service, username))
    conn.commit()
    conn.close()
    print(f"{colors.OKGREEN}Password deleted successfully!{colors.ENDC}")

# Generate a random password
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

# Search for passwords
def search_passwords(user_id, keyword):
    key = load_key()
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM passwords WHERE user_id=? AND (service LIKE ? OR username LIKE ?)",
                   (user_id, f'%{keyword}%', f'%{keyword}%'))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print(f"{colors.WARNING}No passwords found matching the keyword.{colors.ENDC}")
    else:
        print(f"{colors.OKBLUE}Matching passwords:{colors.ENDC}")
        for row in rows:
            decrypted_password = decrypt_password(row[4], key)
            if decrypted_password:
                print(f"ID: {row[0]}, Service: {row[2]}, Username: {row[3]}, Password: {decrypted_password}")
            else:
                print(f"ID: {row[0]}, Service: {row[2]}, Username: {row[3]}, Password: {colors.FAIL}Error: Invalid encryption key or tampered data.{colors.ENDC}")

# Backup Database
def backup_database():
    try:
        backup_filename = f"backup_{datetime.now().strftime('%Y%m%d%H%M%S')}.db"
        shutil.copyfile("my_database.db", backup_filename)
        print(f"{colors.OKGREEN}Database backed up successfully to {backup_filename}{colors.ENDC}")
    except Exception as e:
        print(f"{colors.FAIL}Error backing up database: {e}{colors.ENDC}")

# Restore Database
def restore_database(backup_filename):
    try:
        shutil.copyfile(backup_filename, "my_database.db")
        print(f"{colors.OKGREEN}Database restored successfully from {backup_filename}{colors.ENDC}")
    except Exception as e:
        print(f"{colors.FAIL}Error restoring database: {e}{colors.ENDC}")

# Password strength checker
def check_password_strength(password):
    if len(password) < 8:
        return "Weak"
    if not any(char.isdigit() for char in password):
        return "Weak"
    if not any(char.isupper() for char in password):
        return "Weak"
    if not any(char.islower() for char in password):
        return "Weak"
    if not any(char in string.punctuation for char in password):
        return "Weak"
    return "Strong"

def signup():
    print_logo()
    print(f"{colors.OKBLUE}Sign Up{colors.ENDC}")

    while True:
        name = input("Enter your name: ")
        if all(char.isalpha() or char.isspace() for char in name):
            break
        else:
            print(f"{colors.FAIL}Invalid name. Please enter a valid name without numbers or special characters.{colors.ENDC}")

    while True:
        email = input("Enter your email: ")
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_regex, email):
            break
        else:
            print(f"{colors.FAIL}Invalid email format. Please enter a valid email address.{colors.ENDC}")

    while True:
        phone = input("Enter your phone number (10 digits): ")
        if len(phone) == 10 and phone.isdigit():
            break
        else:
            print(f"{colors.FAIL}Invalid phone number. Please enter a valid 10-digit phone number.{colors.ENDC}")

    while True:
        username = input("Enter your username: ")
        if any(char.isalpha() for char in username):
            break
        else:
            print(f"{colors.FAIL}Username must contain at least one alphabet.{colors.ENDC}")

    while True:
        password = input("Enter your password: ")
        confirm_password = input("Confirm your password: ")
        if password == confirm_password:
            strength = check_password_strength(password)
            print(f"Password strength: {strength}")
            if strength == "Weak":
                print(f"{colors.WARNING}Please choose a stronger password.{colors.ENDC}")
            else:
                break
        else:
            print(f"{colors.FAIL}Passwords do not match. Please try again.{colors.ENDC}")

    # Register the user
    add_user(name, email, phone, username, password)
    
    # After successful registration, log the user in
    #authenticated, user_id = authenticate_user(username, password)
    #if authenticated:
       # print(f"{colors.OKGREEN}Login successful!{colors.ENDC}")
        #main_menu(user_id)
    #else:
        #print(f"{colors.FAIL}Failed to log in after registration.{colors.ENDC}")


# Login menu
def login():
    print_logo()
    print(f"{colors.OKBLUE}Login{colors.ENDC}")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    authenticated, user_id = authenticate_user(username, password)
    if authenticated:
        print(f"{colors.OKGREEN}Login successful!{colors.ENDC}")
        main_menu(user_id)
    else:
        print(f"{colors.FAIL}Invalid username or password.{colors.ENDC}")
        main()
# Main menu
def main_menu(user_id):
    print_logo()
    print(f"{colors.OKBLUE}Main Menu{colors.ENDC}")
    print("1. Add a new password")
    print("2. View all passwords")
    print("3. Update a password")
    print("4. Delete a password")
    print("5. Search for passwords")
    print("6. Generate a random password")
    print("7. Backup database")
    print("8. Restore database")
    print("9. Exit")
    choice = input("Enter your choice (1-9): ")

    if choice == '1':
        service = input("Enter the service name: ")
        username = input("Enter the username: ")
        password = input("Enter the password: ")
        add_password(user_id, service, username, password)
    elif choice == '2':
        view_passwords(user_id)
    elif choice == '3':
        service = input("Enter the service name: ")
        username = input("Enter the username: ")
        new_password = input("Enter the new password: ")
        update_password(user_id, service, username, new_password)
    elif choice == '4':
        service = input("Enter the service name: ")
        username = input("Enter the username: ")
        delete_password(user_id, service, username)
    elif choice == '5':
        keyword = input("Enter the keyword to search: ")
        search_passwords(user_id, keyword)
    elif choice == '6':
        length = int(input("Enter the length of the password: "))
        print(f"Generated password: {generate_password(length)}")
    elif choice == '7':
        backup_database()
    elif choice == '8':
        backup_filename = input("Enter the backup filename: ")
        restore_database(backup_filename)
    elif choice == '9':
        print(f"{colors.OKGREEN}Goodbye!{colors.ENDC}")
        exit()
    else:
        print(f"{colors.FAIL}Invalid choice. Please enter a number between 1 and 9.{colors.ENDC}")
    
    # Return to main menu after each operation
    time.sleep(2)
    main_menu(user_id)

# Main function
def main():
    print_logo()
    print("1. Sign Up")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter your choice (1-3): ")

    if choice == '1':
        signup()
    elif choice == '2':
        login()
    elif choice == '3':
        print(f"{colors.OKGREEN}Goodbye!{colors.ENDC}")
        exit()
    else:
        print(f"{colors.FAIL}Invalid choice. Please enter a number between 1 and 3.{colors.ENDC}")
        main()

# Initialize the database and generate a key if not present
if __name__ == "__main__":
    init_db()
    if not os.path.exists("secret.key"):
        generate_key()
    main()
