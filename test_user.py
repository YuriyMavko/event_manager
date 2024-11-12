import unittest
import os
from user import User

class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists('logins'):
            for root, dirs, files in os.walk('logins', topdown=False):
                for file in files:
                    os.remove(os.path.join(root, file))
                for dir in dirs:
                    os.rmdir(os.path.join(root, dir))
            os.rmdir('logins')
        if os.path.exists('temp.txt'):
            os.remove('temp.txt')

    def test_authenticate_valid_email(self):
        self.assertTrue(self.user.authenticate("valid.email@example.com"))

    def test_authenticate_invalid_email(self):
        self.assertFalse(self.user.authenticate("invalid-email.com"))

    def test_register_user_with_custom_password(self):
        email = "test_user@example.com"
        password = "customPassword123"
        response = self.user.register_user(email, password_choice=1, password=password)
        self.assertEqual(response, f"User {email} successfully registered with password: {password}")
        self.assertTrue(os.path.exists(f'logins/{email}.txt'))

    def test_register_user_with_generated_password(self):
        email = "generated_user@example.com"
        password_length = 12
        response = self.user.register_user(email, password_choice=2, password_length=password_length)
        self.assertTrue(response.startswith(f"User {email} successfully registered with password: "))
        self.assertTrue(os.path.exists(f'logins/{email}.txt'))

    def test_register_user_existing_user(self):
        email = "existing_user@example.com"
        password = "existingPassword123"
        self.user.register_user(email, password_choice=1, password=password)
        response = self.user.register_user(email, password_choice=1, password=password)
        self.assertEqual(response, f"The user {email} already exists.")

    def test_register_user_invalid_email(self):
        response = self.user.register_user("invalid_email.com", password_choice=1, password="test12345")
        self.assertEqual(response, "Invalid email format.")

    def test_login_user_successful(self):
        email = "login_user@example.com"
        password = "correctPassword123"
        self.user.register_user(email, password_choice=1, password=password)
        response = self.user.login_user(email, password)
        self.assertEqual(response, "Login successful.")

    def test_login_user_incorrect_password(self):
        email = "login_user_fail@example.com"
        password = "correctPassword123"
        self.user.register_user(email, password_choice=1, password=password)
        response = self.user.login_user(email, "wrongPassword")
        self.assertEqual(response, "Incorrect password.")

    def test_login_user_not_found(self):
        response = self.user.login_user("nonexistent_user@example.com", "anyPassword")
        self.assertEqual(response, "Username not found.")

    def test_logout_user(self):
        self.user.login_user("test_logout@example.com", "logoutPassword")
        response = self.user.logout_user()
        self.assertEqual(response, "User logged out successfully.")
        with open('temp.txt', 'r') as file:
            content = file.read().strip()
        self.assertEqual(content, "")

    def test_read_temp_file_with_data(self):
        email = "temp_user@example.com"
        password = "tempPassword123"
        self.user.register_user(email, password_choice=1, password=password)
        self.user.login_user(email, password)
        username, read_password = self.user.read_temp_file()
        self.assertEqual(username, email)
        self.assertEqual(read_password, password)

    def test_read_temp_file_no_data(self):
        if os.path.exists("temp.txt"):
            os.remove("temp.txt")
        username, password = self.user.read_temp_file()
        self.assertIsNone(username)
        self.assertIsNone(password)

    def test_check_login_success(self):
        email = "check_user@example.com"
        password = "checkPassword123"
        self.user.register_user(email, password_choice=1, password=password)
        self.assertTrue(self.user.check_login(email, password))

    def test_check_login_failure(self):
        email = "check_fail_user@example.com"
        password = "failPassword123"
        self.user.register_user(email, password_choice=1, password=password)
        self.assertFalse(self.user.check_login(email, "wrongPassword"))


if __name__ == '__main__':
    unittest.main()
