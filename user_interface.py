from user import User
class UserInterface:
    def __init__(self, user):
        self.user = user

    def register(self):
        email = input("Enter your email: ")
        password_choice = int(input("Enter 1 to write your password or 2 to generate it automatically: "))

        if password_choice == 1:
            password = ""
            while len(password) < 8:
                password = input("Enter your password to register (minimum 8 characters): ")
            result = self.user.register_user(email, password_choice, password=password)
        elif password_choice == 2:
            length = 0
            while length < 8:
                length = int(input("Enter the password length (minimum 8): "))
            result = self.user.register_user(email, password_choice, password_length=length)

        print(result)

    def login(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        result = self.user.login_user(username, password)
        print(result)

    def logout(self):
        result = self.user.logout_user()
        print(result)

    def check_temp_login(self):
        username, password = self.user.read_temp_file()
        if username and password:
            if self.user.check_login(username, password):
                print(f"User {username} is already logged in.")
                return True
        return False
