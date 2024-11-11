import os
from generate import PasswordGenerator
import re


class User(PasswordGenerator):
    def __init__(self):
        self.username = ""
        self.password = ""

    def authenticate(self, email):
        email_regex = re.compile(r"[A-Za-z]+[\. A-Za-z0-9 _-]*[A-Za-z0-9]+@[A-Za-z]+\.[A-Za-z]+")
        return email_regex.match(email)

    def register_user(self, email, password_choice, password=None, password_length=None):
        if self.authenticate(email):
            self.username = email
            if password_choice == 1:
                if len(password) < 8:
                    return "Password must be at least 8 characters long."
                self.password = password
            elif password_choice == 2:
                if password_length < 8:
                    return "Password length must be at least 8."
                self.password = self.generate_password(password_length)

            if not os.path.exists('logins'):
                os.makedirs('logins')

            path = 'logins/' + self.username + ".txt"
            if not os.path.exists(path):
                with open(path, 'w') as file:
                    file.write(self.password)
                return f"User {self.username} successfully registered with password: {self.password}"
            else:
                return f"The user {self.username} already exists."
        else:
            return "Invalid email format."

    def login_user(self, username, password):
        self.username = username
        self.password = password
        path = "logins/" + self.username + ".txt"

        if os.path.exists(path):
            with open(path, 'r') as file:
                stored_password = file.read().strip()
                if stored_password == self.password:
                    with open('temp.txt', 'w') as file:
                        file.write(f"{username}\n{password}")
                    return "Login successful."
                else:
                    return "Incorrect password."
        else:
            return "Username not found."

    def logout_user(self):
        with open('temp.txt', 'w') as file:
            file.truncate(0)
        return "User logged out successfully."

    def read_temp_file(self):
        try:
            with open("temp.txt", "r") as f:
                lines = f.readlines()
                if len(lines) >= 2:
                    username = lines[0].strip()
                    password = lines[1].strip()
                    return username, password
        except FileNotFoundError:
            pass
        return None, None

    def check_login(self, username, password):
        login_file_path = os.path.join("logins", f"{username}.txt")
        if os.path.exists(login_file_path):
            try:
                with open(login_file_path, "r") as f:
                    stored_password = f.readline().strip()
                    return password == stored_password
            except FileNotFoundError:
                pass
        return False
