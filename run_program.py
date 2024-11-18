from user import User
from user_interface import UserInterface
from event import Event
from event_interface import EventInterface
from file_manager import FileManager


class RunProgram:
    def __init__(self):
        self.file_manager = FileManager()  # Ініціалізація FileManager
        self.user = User(file_manager=self.file_manager)  # Передаємо FileManager у User
        self.ui = UserInterface(self.user)  # Ініціалізація UserInterface
        self.event_logic = Event(file_manager=self.file_manager)  # Передаємо FileManager у Event
        self.event_interface = EventInterface(self.event_logic)  # EventInterface

    def run_program(self):
        try:
            while True:
                username, password = self.user.read_temp_file()
                if username and password and self.user.check_login(username, password):
                    print(f"Automatically logged in as {username}.")
                    is_authenticated = True
                else:
                    is_authenticated = False
                    while not is_authenticated:
                        choice = input("Enter 'reg' to register, 'log' to log in, or any other key to exit: ")
                        if choice.lower() == "reg":
                            self.ui.register()
                        elif choice.lower() == "log":
                            self.ui.login()
                            username, password = self.user.read_temp_file()
                            if self.user.check_login(username, password):
                                print(f"Successfully logged in as {username}.")
                                is_authenticated = True
                        else:
                            print("End of program execution.")
                            exit()

                path = f"data/{username}"
                while is_authenticated:
                    try:
                        print("\nOptions:")
                        options = {
                            1: ("Add an event", lambda: self.event_interface.add_event_interface(path)),
                            2: ("Display events", lambda: self.event_interface.display_events_interface(path)),
                            3: ("Edit events", lambda: self.event_interface.update_event_interface(path)),
                            4: ("Delete events", lambda: self.event_interface.delete_event_interface(path)),
                            5: ("Log out", lambda: self.ui.logout()),
                            6: ("Exit program", lambda: exit())
                        }

                        for key, (desc, _) in options.items():
                            print(f"{key}: {desc}")

                        choice = int(input("Select an option: "))
                        if choice in options:
                            action = options[choice][1]
                            if choice == 5:  # Log out
                                action()
                                is_authenticated = False
                            elif choice == 6:  # Exit
                                action()
                            else:
                                action()
                        else:
                            print("Invalid selection. Please try again.")
                    except ValueError:
                        print("Please enter a valid number.")
                    except Exception as e:
                        print(f"An error occurred: {e}")
        except KeyboardInterrupt:
            print("\nThe program has been stopped!")
