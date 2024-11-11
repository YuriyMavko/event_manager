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

                    while num != 6:
                        print("Enter 1 to add an event")
                        print("Enter 2 to display events")
                        print("Enter 3 to edit events")
                        print("Enter 4 to delete events")
                        print("Enter 5 to log out of your account")
                        print("Enter 6 to close the program")
                        num = int(input())
                        path = "data/" + username

                        if num == 1:
                            event_interface.add_event_interface(path)
                        elif num == 2:
                            event_interface.display_event_interface(path)
                        elif num == 3:
                            event_interface.update_event_interface(path)
                        elif num == 4:
                            event_interface.delete_event_interface(path)
                        elif num == 5:
                            ui.logout()
                            num = 10
                            print(f"Logged out of {username}'s account.")
                            break
                        elif num == 6:
                            print("End of program execution. Thank you!")
                            exit()
        except KeyboardInterrupt:
            print("The program has been stopped!")
