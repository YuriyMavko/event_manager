from file_manager import FileManager
import os
from generate import PasswordGenerator
import re


class User(PasswordGenerator):
    def __init__(self, file_manager):
        self.username = ""
        self.password = ""
        self.file_manager = file_manager

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

            path = os.path.join('logins', f"{self.username}.txt")
            if FileManager.read_file(path) is None:
                FileManager.write_file(path, self.password)
                return f"User {self.username} successfully registered with password: {self.password}"
            else:
                return f"The user {self.username} already exists."
        else:
            return "Invalid email format."

    def login_user(self, username, password):
        self.username = username
        self.password = password
        path = os.path.join("logins", f"{self.username}.txt")

        stored_password = FileManager.read_file(path)
        if stored_password is not None:
            if stored_password.strip() == self.password:
                FileManager.write_file("temp.txt", f"{username}\n{password}")
                return "Login successful."
            else:
                return "Incorrect password."
        else:
            return "Username not found."

    def logout_user(self):
        self.file_manager.write_file("temp.txt","" , mode='w')
        return "User logged out successfully."

    def read_temp_file(self):
        lines = FileManager.read_lines("temp.txt")
        if len(lines) >= 2:
            username = lines[0].strip()
            password = lines[1].strip()
            return username, password
        return None, None

    def check_login(self, username, password):
        path = os.path.join("logins", f"{username}.txt")
        stored_password = FileManager.read_file(path)
        return stored_password is not None and stored_password.strip() == password
