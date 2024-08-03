import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import sqlite3
import string
import random

DATABASE = "password_manager.db"
LOGGED_IN_USER = None

def create_login_screen():
    def login():
        global LOGGED_IN_USER
        username = username_entry.get()
        password = password_entry.get()
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            LOGGED_IN_USER = username
            login_window.destroy()
            main_menu()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def signup():
        def signup_submit():
            name = name_entry.get()
            email = email_entry.get()
            phone = phone_entry.get()
            username = signup_username_entry.get()
            password = signup_password_entry.get()

            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, email, phone, username, password) VALUES (?, ?, ?, ?, ?)", (name, email, phone, username, password))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Sign up successful!")
            signup_window.destroy()

        signup_window = tk.Toplevel()
        signup_window.title("Sign Up")

        # Styling
        signup_window.configure(bg="black")
        signup_window.geometry("400x400")

        window_width = signup_window.winfo_reqwidth()
        window_height = signup_window.winfo_reqheight()
        position_right = int(signup_window.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(signup_window.winfo_screenheight() / 2 - window_height / 2)
        signup_window.geometry(f"+{position_right}+{position_down}")

        tk.Label(signup_window, text="Name:", bg="black", fg="white", font=("Helvetica", 12)).pack(pady=10)
        name_entry = tk.Entry(signup_window, font=("Helvetica", 12))
        name_entry.pack(pady=5)

        tk.Label(signup_window, text="Email:", bg="black", fg="white", font=("Helvetica", 12)).pack(pady=10)
        email_entry = tk.Entry(signup_window, font=("Helvetica", 12))
        email_entry.pack(pady=5)

        tk.Label(signup_window, text="Phone:", bg="black", fg="white", font=("Helvetica", 12)).pack(pady=10)
        phone_entry = tk.Entry(signup_window, font=("Helvetica", 12))
        phone_entry.pack(pady=5)

        tk.Label(signup_window, text="Username:", bg="black", fg="white", font=("Helvetica", 12)).pack(pady=10)
        signup_username_entry = tk.Entry(signup_window, font=("Helvetica", 12))
        signup_username_entry.pack(pady=5)

        tk.Label(signup_window, text="Password:", bg="black", fg="white", font=("Helvetica", 12)).pack(pady=10)
        signup_password_entry = tk.Entry(signup_window, show="*", font=("Helvetica", 12))
        signup_password_entry.pack(pady=5)

        tk.Button(signup_window, text="Sign Up", command=signup_submit, font=("Helvetica", 12), bg="#fdcb6e", fg="black", width=20).pack(pady=20)

    login_window = tk.Tk()
    login_window.title("Login")

    # Styling
    login_window.configure(bg="black")
    login_window.geometry("400x300")

    window_width = login_window.winfo_reqwidth()
    window_height = login_window.winfo_reqheight()
    position_right = int(login_window.winfo_screenwidth() / 2 - window_width / 2)
    position_down = int(login_window.winfo_screenheight() / 2 - window_height / 2)
    login_window.geometry(f"+{position_right}+{position_down}")

    tk.Label(login_window, text="Username:", bg="black", fg="white", font=("Helvetica", 12)).pack(pady=10)
    username_entry = tk.Entry(login_window, font=("Helvetica", 12))
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password:", bg="black", fg="white", font=("Helvetica", 12)).pack(pady=10)
    password_entry = tk.Entry(login_window, show="*", font=("Helvetica", 12))
    password_entry.pack(pady=5)

    tk.Button(login_window, text="Login", command=login, font=("Helvetica", 12), bg="#fdcb6e", fg="black", width=20).pack(pady=20)
    tk.Button(login_window, text="Sign Up", command=signup, font=("Helvetica", 12), bg="#fdcb6e", fg="black", width=20).pack(pady=10)

    login_window.mainloop()

def main_menu():
    def logout():
        global LOGGED_IN_USER
        LOGGED_IN_USER = None
        main_menu_window.destroy()
        create_login_screen()

    def handle_add_password():
        def add_password_submit():
            service = service_entry.get()
            username = username_entry.get()
            password = password_entry.get()
            add_password(service, username, password)
            messagebox.showinfo("Success", "Password added successfully!")
            add_password_window.destroy()

        add_password_window = tk.Toplevel()
        add_password_window.title("Add Password")

        # Styling
        add_password_window.configure(bg="black")
        add_password_window.geometry("400x300")

        window_width = add_password_window.winfo_reqwidth()
        window_height = add_password_window.winfo_reqheight()
        position_right = int(add_password_window.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(add_password_window.winfo_screenheight() / 2 - window_height / 2)
        add_password_window.geometry(f"+{position_right}+{position_down}")

        tk.Label(add_password_window, text="Service:", bg="black", fg="white", font=("Helvetica", 12)).pack(pady=10)
        service_entry = tk.Entry(add_password_window, font=("Helvetica", 12))
        service_entry.pack(pady=5)

        tk.Label(add_password_window, text="Username:", bg="black", fg="white", font=("Helvetica", 12)).pack(pady=10)
        username_entry = tk.Entry(add_password_window, font=("Helvetica", 12))
        username_entry.pack(pady=5)

        tk.Label(add_password_window, text="Password:", bg="black", fg="white", font=("Helvetica", 12)).pack(pady=10)
        password_entry = tk.Entry(add_password_window, show="*", font=("Helvetica", 12))
        password_entry.pack(pady=5)

        tk.Button(add_password_window, text="Add Password", command=add_password_submit, font=("Helvetica", 12), bg="#fdcb6e", fg="black", width=20).pack(pady=20)

    def handle_view_passwords():
        passwords = view_passwords()
        if passwords:
            view_passwords_window = tk.Toplevel()
            view_passwords_window.title("Your Passwords")

            # Styling
            view_passwords_window.configure(bg="black")
            view_passwords_window.geometry("600x400")

            window_width = view_passwords_window.winfo_reqwidth()
            window_height = view_passwords_window.winfo_reqheight()
            position_right = int(view_passwords_window.winfo_screenwidth() / 2 - window_width / 2)
            position_down = int(view_passwords_window.winfo_screenheight() / 2 - window_height / 2)
            view_passwords_window.geometry(f"+{position_right}+{position_down}")

            for idx, (service, username, password) in enumerate(passwords):
                tk.Label(view_passwords_window, text=f"{service} ({username}): {password}", bg="black", fg="white", font=("Helvetica", 12)).pack(pady=5)
        else:
            messagebox.showinfo("No Passwords", "No passwords saved yet.")

    def handle_update_password():
        def update_password_submit():
            service = service_entry.get()
            new_password = new_password_entry.get()
            update_password(service, LOGGED_IN_USER, new_password)
            messagebox.showinfo("Success", "Password updated successfully!")
            update_password_window.destroy()

        update_password_window = tk.Toplevel()
        update_password_window.title("Update Password")

        # Styling
        update_password_window.configure(bg="black")
        update_password_window.geometry("400x300")

        window_width = update_password_window.winfo_reqwidth()
        window_height = update_password_window.winfo_reqheight()
        position_right = int(update_password_window.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(update_password_window.winfo_screenheight() / 2 - window_height / 2)
        update_password_window.geometry(f"+{position_right}+{position_down}")

        tk.Label(update_password_window, text="Service:", bg="black", fg="white", font=("Helvetica", 12)).pack(pady=10)
        service_entry = tk.Entry(update_password_window, font=("Helvetica", 12))
        service_entry.pack(pady=5)

        tk.Label(update_password_window, text="New Password:", bg="black", fg="white", font=("Helvetica", 12)).pack(pady=10)
        new_password_entry = tk.Entry(update_password_window, show="*", font=("Helvetica", 12))
        new_password_entry.pack(pady=5)

        tk.Button(update_password_window, text="Update Password", command=update_password_submit, font=("Helvetica", 12), bg="#fdcb6e", fg="black", width=20).pack(pady=20)

    def handle_delete_password():
        def delete_password_submit():
            service = service_entry.get()
            delete_password(service, LOGGED_IN_USER)
            messagebox.showinfo("Success", "Password deleted successfully!")
            delete_password_window.destroy()

        delete_password_window = tk.Toplevel()
        delete_password_window.title("Delete Password")

        # Styling
        delete_password_window.configure(bg="black")
        delete_password_window.geometry("400x300")

        window_width = delete_password_window.winfo_reqwidth()
        window_height = delete_password_window.winfo_reqheight()
        position_right = int(delete_password_window.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(delete_password_window.winfo_screenheight() / 2 - window_height / 2)
        delete_password_window.geometry(f"+{position_right}+{position_down}")

        tk.Label(delete_password_window, text="Service:", bg="black", fg="white", font=("Helvetica", 12)).pack(pady=10)
        service_entry = tk.Entry(delete_password_window, font=("Helvetica", 12))
        service_entry.pack(pady=5)

        tk.Button(delete_password_window, text="Delete Password", command=delete_password_submit, font=("Helvetica", 12), bg="#fdcb6e", fg="black", width=20).pack(pady=20)

    def handle_search_password():
        def search_password_submit():
            service = service_entry.get()
            password = search_password(service, LOGGED_IN_USER)
            if password:
                messagebox.showinfo("Password Found", f"Password for {service}: {password}")
            else:
                messagebox.showinfo("Password Not Found", f"No password saved for {service}.")
            search_password_window.destroy()

        search_password_window = tk.Toplevel()
        search_password_window.title("Search Password")

        # Styling
        search_password_window.configure(bg="black")
        search_password_window.geometry("400x300")

        window_width = search_password_window.winfo_reqwidth()
        window_height = search_password_window.winfo_reqheight()
        position_right = int(search_password_window.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(search_password_window.winfo_screenheight() / 2 - window_height / 2)
        search_password_window.geometry(f"+{position_right}+{position_down}")

        tk.Label(search_password_window, text="Service:", bg="black", fg="white", font=("Helvetica", 12)).pack(pady=10)
        service_entry = tk.Entry(search_password_window, font=("Helvetica", 12))
        service_entry.pack(pady=5)

        tk.Button(search_password_window, text="Search Password", command=search_password_submit, font=("Helvetica", 12), bg="#fdcb6e", fg="black", width=20).pack(pady=20)

    main_menu_window = tk.Tk()
    main_menu_window.title("Password Manager")

    # Styling
    main_menu_window.configure(bg="black")
    main_menu_window.geometry("600x400")

    window_width = main_menu_window.winfo_reqwidth()
    window_height = main_menu_window.winfo_reqheight()
    position_right = int(main_menu_window.winfo_screenwidth() / 2 - window_width / 2)
    position_down = int(main_menu_window.winfo_screenheight() / 2 - window_height / 2)
    main_menu_window.geometry(f"+{position_right}+{position_down}")

    tk.Button(main_menu_window, text="Add Password", command=handle_add_password, font=("Helvetica", 12), bg="#fdcb6e", fg="black", width=20).pack(pady=20)
    tk.Button(main_menu_window, text="View Passwords", command=handle_view_passwords, font=("Helvetica", 12), bg="#fdcb6e", fg="black", width=20).pack(pady=20)
    tk.Button(main_menu_window, text="Update Password", command=handle_update_password, font=("Helvetica", 12), bg="#fdcb6e", fg="black", width=20).pack(pady=20)
    tk.Button(main_menu_window, text="Delete Password", command=handle_delete_password, font=("Helvetica", 12), bg="#fdcb6e", fg="black", width=20).pack(pady=20)
    tk.Button(main_menu_window, text="Search Password", command=handle_search_password, font=("Helvetica", 12), bg="#fdcb6e", fg="black", width=20).pack(pady=20)
    tk.Button(main_menu_window, text="Logout", command=logout, font=("Helvetica", 12), bg="#fdcb6e", fg="black", width=20).pack(pady=20)

    main_menu_window.mainloop()

def add_password(service, username, password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passwords (service, username, password) VALUES (?, ?, ?)", (service, username, password))
    conn.commit()
    conn.close()

def view_passwords():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT service, username, password FROM passwords WHERE username = ?", (LOGGED_IN_USER,))
    passwords = cursor.fetchall()
    conn.close()
    return passwords

def update_password(service, username, new_password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE passwords SET password = ? WHERE service = ? AND username = ?", (new_password, service, username))
    conn.commit()
    conn.close()

def delete_password(service, username):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM passwords WHERE service = ? AND username = ?", (service, username))
    conn.commit()
    conn.close()

def search_password(service, username):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM passwords WHERE service = ? AND username = ?", (service, username))
    password = cursor.fetchone()
    conn.close()
    return password[0] if password else None

def initialize_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL,
                       email TEXT NOT NULL,
                       phone TEXT NOT NULL,
                       username TEXT UNIQUE NOT NULL,
                       password TEXT NOT NULL)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS passwords
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       service TEXT NOT NULL,
                       username TEXT NOT NULL,
                       password TEXT NOT NULL,
                       FOREIGN KEY (username) REFERENCES users(username))''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
    create_login_screen()
