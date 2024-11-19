import unittest
from user import User
from file_manager import FileManager
import os
import shutil


class TestUser(unittest.TestCase):
    def setUp(self):
        self.file_manager = FileManager()
        self.user = User(self.file_manager)
        if not os.path.exists('logins'):
            os.makedirs('logins')

    def test_authenticate(self):
        valid_emails = [
            "test@example.com",
            "user.name@domain.com",
            "user_name@domain.com",
            "user-name@domain.com"
        ]
        for email in valid_emails:
            self.assertTrue(self.user.authenticate(email))
        invalid_emails = [
            "test@.com",
            "@domain.com",
            "test@domain",
            "test.domain.com",
            "test@domain."
        ]
        for email in invalid_emails:
            self.assertFalse(self.user.authenticate(email))

    def test_register_user(self):
        result = self.user.register_user("test@example.com", 1, password="password123")
        self.assertIn("successfully registered", result)

        result = self.user.register_user("test2@example.com", 2, password_length=10)
        self.assertIn("successfully registered", result)
        result = self.user.register_user("test3@example.com", 1, password="short")
        self.assertEqual(result, "Password must be at least 8 characters long.")
        result = self.user.register_user("test@example.com", 1, password="password123")
        self.assertIn("already exists", result)

    def test_login_user(self):
        self.user.register_user("test@example.com", 1, password="password123")

        result = self.user.login_user("test@example.com", "password123")
        self.assertEqual(result, "Login successful.")
        result = self.user.login_user("test@example.com", "wrongpassword")
        self.assertEqual(result, "Incorrect password.")
        result = self.user.login_user("nonexistent@example.com", "password123")
        self.assertEqual(result, "Username not found.")

    def test_logout_user(self):
        self.user.login_user("test@example.com", "password123")

        result = self.user.logout_user()
        self.assertEqual(result, "User logged out successfully.")
        with open("temp.txt", 'r') as f:
            content = f.read()
        self.assertEqual(content, "")

    def test_check_login(self):
        self.user.register_user("test@example.com", 1, password="password123")

        self.assertTrue(self.user.check_login("test@example.com", "password123"))
        self.assertFalse(self.user.check_login("test@example.com", "wrongpassword"))
        self.assertFalse(self.user.check_login("nonexistent@example.com", "password123"))

    def tearDown(self):
        if os.path.exists('logins'):
            shutil.rmtree('logins')
        if os.path.exists('temp.txt'):
            os.remove('temp.txt')


if __name__ == '__main__':
    unittest.main()