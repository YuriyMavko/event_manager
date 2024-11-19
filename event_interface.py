from event import Event
from validate import Date
from file_manager import FileManager

class EventInterface:
    def __init__(self, event_logic):
        self.event_logic = event_logic

    def add_event_interface(self, path_to_auth):
        title = input("Enter title\n")
        description = input("Enter description\n")
        date = ""
        obj_date = Date()
        while not obj_date.validate_date(date):
            date = input("Enter date (dd-mm-yyyy)\n")

        day, month, year = date.split("-")
        file_path = path_to_auth + f"/{day}-{month}-{year}/{date}.json"

        if self.event_logic.file_manager.file_exists(file_path):
            print(f"Error: An event on {date} already exists!")
            return

        num = int(input("Enter the number of participants\n"))
        participants = [input(f"Enter participant {i + 1}\n") for i in range(num)]

        try:
            self.event_logic.add_event(path_to_auth, title, description, date, participants)
            print("Event added successfully!")
        except ValueError as e:
            print(f"Error: {e}")

    def update_event_interface(self, path_to_auth):
        while True:
            old_date = input("Enter the current date (dd-mm-yyyy) of the event you want to change\n")

            day, month, year = old_date.split("-")
            file_path = path_to_auth + f"/{day}-{month}-{year}/{old_date}.json"

            if not self.event_logic.file_manager.file_exists(file_path):
                print(f"Error: No event exists on {old_date}")
                choice = input("Do you want to try another date? (y/n): ")
                if choice.lower() != 'y':
                    return
                continue

            updated_data = {}
            num = 0
            obj_date = Date()

            while num != 5:
                print("Enter a number if you want to change:")
                print("1 - title, 2 - description, 3 - date, 4 - participants, 5 - exit")
                num = int(input())
                if num == 1:
                    updated_data["title"] = input("Enter the new title\n")
                elif num == 2:
                    updated_data["description"] = input("Enter the new description\n")
                elif num == 3:
                    new_date = ""
                    while not obj_date.validate_date(new_date):
                        new_date = input("Enter the new date (dd-mm-yyyy)\n")
                    updated_data["date"] = new_date
                elif num == 4:
                    participant_count = int(input("Enter the number of new participants\n"))
                    updated_data["participants"] = [input(f"Enter participant {i + 1}\n") for i in
                                                    range(participant_count)]
                elif num == 5:
                    print("Exiting update process.")
                else:
                    print("Invalid option. Please enter a number between 1 and 5.")

            try:
                new_date = updated_data.get("date", old_date)
                self.event_logic.update_event(path_to_auth, old_date, {**updated_data, "date": new_date})
                print("Event updated successfully!")
                break
            except (ValueError, FileNotFoundError) as e:
                print(f"Error: {e}")
                break

    def display_events_interface(self, path_to_auth):
        options = {
            1: ("Enter 1 to display events by year", lambda: self._display_year(path_to_auth)),
            2: ("Enter 2 to display events by month", lambda: self._display_month(path_to_auth)),
            3: ("Enter 3 to display events by day", lambda: self._display_day(path_to_auth)),
            4: ("Enter 4 to display events by period", lambda: self._display_period(path_to_auth)),
        }

        for option in options.values():
            print(option[0])
        num = int(input("Select an option: "))

        if num in options:
            options[num][1]()
        else:
            print("Invalid selection. Please try again.")

    def _display_year(self, path_to_auth):
        year = input("Enter the year (yyyy): ")
        events = self.event_logic.display_events_by_year(path_to_auth, year)
        if isinstance(events, str):
            print(events)
        else:
            for event in events:
                print(event)
            self._display_specific_event(path_to_auth)

    def _display_month(self, path_to_auth):
        year = input("Enter the year (yyyy): ")
        month = input("Enter the month (mm): ")
        events = self.event_logic.display_events_by_month(path_to_auth, year, month)
        if isinstance(events, str):
            print(events)
        else:
            for event in events:
                print(event)
            self._display_specific_event(path_to_auth)
    def _display_day(self, path_to_auth):
        date = input("Enter the date (dd-mm-yyyy): ")
        events = self.event_logic.display_events_by_day(path_to_auth, date)
        if isinstance(events, str):
            print(events)
        else:
            print(f"Date: {events['date']} - Title: {events['title']}")

    def _display_period(self, path_to_auth):
        start_date = input("Enter the start date (dd-mm-yyyy): ")
        end_date = input("Enter the end date (dd-mm-yyyy): ")
        events = self.event_logic.display_events_by_period(path_to_auth, start_date, end_date)
        if isinstance(events, str):
            print(events)
        else:
            for event in events:
                print(event)
            self._display_specific_event(path_to_auth)

    def delete_event_interface(self, path_to_auth):
        date = input("Enter the date (dd-mm-yyyy) of the event to delete\n")
        try:
            self.event_logic.delete_event(path_to_auth, date)
            print("Event deleted successfully!")
        except FileNotFoundError:
            print("Event not found.")
        except ValueError as e:
            print(f"Error: {e}")

    def _display_specific_event(self, path_to_auth):
        choice = int(input("If you want to view a specific event, press 1, otherwise any other number\n"))
        if choice == 1:
            try:
                date = input("\nEnter the date of the event (dd-mm-yyyy): ")
                day, month, year = date.split("-")
                file_path = f"{path_to_auth}/{day}-{month}-{year}/{date}.json"
                event_data = self.event_logic.file_manager.read_json(file_path)
                if event_data:
                    print("\nEvent details:")
                    print(f"Title: {event_data['title']}")
                    print(f"Description: {event_data['description']}")
                    print(f"Date: {event_data['date']}")
                    print(f"Participants: {', '.join(event_data['participants'])}")
                else:
                    print("Event not found!")

            except ValueError as e:
                print(f"Date format error: {e}")
            except FileNotFoundError:
                print(f"Error: Event file not found")
            except Exception as e:
                print(f"An error occurred: {e}")