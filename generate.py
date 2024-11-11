import random
import string

class PasswordGenerator:
    def generate_password(self, length=8):
        characters = string.ascii_letters + string.digits
        password = []

        for i in range(length):
            random_char = random.choice(characters)
            password.append(random_char)

        password = ''.join(password)

        return password