from user import User
from user_interface import UserInterface
from event import Event
from event_interface import EventInterface

class RunProgram:
    def __init__(self):
        pass

    def run_program(self):
        user = User()
        ui = UserInterface(user)

        try:
            while True:
                username, password = user.read_temp_file()
                if username and password and user.check_login(username, password):
                    print(f"Automatically logged in as {username}.")
                    auth = 1
                else:
                    while True:
                        choice = input("Enter 'reg' to register, 'log' to log in, or any other key to exit\n")
                        if choice.lower() == "reg":
                            ui.register()
                        elif choice.lower() == "log":
                            ui.login()
                            username, password = user.read_temp_file()
                            auth = user.check_login(username, password)
                            if auth:
                                print(f"Successfully logged in as {username}.")
                                break
                        else:
                            print("End of program execution.")
                            exit()

                if auth == 1:
                    num = 0
                    event_logic = Event()
                    event_interface = EventInterface(event_logic)
                    path = "data/" + username
                    while num != 6:

                        options = {
                            1: ("Enter 1 to add an event", lambda path: event_interface.add_event_interface(path)),
                            2: ("Enter 2 to display events", lambda path: event_interface.display_event_interface(path)),
                            3: ("Enter 3 to edit events", lambda path: event_interface.update_event_interface(path)),
                            4: ("Enter 4 to delete events", lambda path: event_interface.delete_event_interface(path)),
                            5: ("Enter 5 to log out of your account", lambda _: ui.logout()),
                            6: ("Enter 6 to close the program", lambda _: exit())
                        }

                        for option in options.values():
                            print(option[0])
                        num = int(input("Select an option: "))

                        if num in options:
                            result = options[num][1](path)
                            if result:
                                break
                            if num == 5:
                                break
                        else:
                            print("Invalid selection. Please try again.")

        except KeyboardInterrupt:
            print("The program has been stopped!")
