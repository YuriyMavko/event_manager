from event import Event
from validate import Date
import os
import json


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
        num = int(input("Enter the number of participants\n"))
        participant = [input(f"Enter participant {i + 1}\n") for i in range(num)]
        try:
            self.event_logic.add_event(path_to_auth, title, description, date, participant)
            print("Event added successfully!")
        except ValueError as e:
            print(f"Error: {e}")

    def update_event_interface(self, path_to_auth):
        date = input("Enter the date (dd-mm-yyyy) of the event you want to change\n")
        updated_data = {}
        num = 0
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
                while not Date().validate_date(new_date):
                    new_date = input("Enter the new date (dd-mm-yyyy)\n")
                updated_data["date"] = new_date
            elif num == 4:
                participants_count = int(input("Enter the number of participants\n"))
                updated_data["participants"] = [input(f"Enter participant {i + 1}\n") for i in
                                                range(participants_count)]

        try:
            self.event_logic.update_event(path_to_auth, date, updated_data)
            print("Event updated successfully!")
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Error: {e}")

    def delete_event_interface(self, path_to_auth):
        date = input("Enter date (dd-mm-yyyy) of the event you want to delete\n")
        try:
            self.event_logic.delete_event(path_to_auth, date)
            print("Event deleted successfully!")
        except FileNotFoundError as e:
            print(f"Error: {e}")

    def display_event_interface(self, path_to_auth):
        print("Choose an option to display events:")
        print("1 - Display events for a specific year")
        print("2 - Display events for a specific month")
        print("3 - Display events for a specific day")
        print("4 - Display events for a specific period")

        choice = int(input())
        if choice == 1:
            year = input("Enter the year (yyyy):\n")
            result = self.event_logic.display_events_by_year(path_to_auth, year)
            self._handle_display_result(result)
            if result != "No events found for this year.":
                self.output_choice(path_to_auth)
        elif choice == 2:
            year = input("Enter the year (yyyy):\n")
            month = input("Enter the month (mm):\n")
            result = self.event_logic.display_events_by_month(path_to_auth, year, month)
            self._handle_display_result(result)
            if result != "No events found for this month.":
                self.output_choice(path_to_auth)

        elif choice == 3:
            date = input("Enter the date (dd-mm-yyyy):\n")
            result = self.event_logic.display_events_by_day(path_to_auth, date)
            self._handle_display_result(result)

        elif choice == 4:
            start_date = input("Enter the start date (dd-mm-yyyy):\n")
            end_date = input("Enter the end date (dd-mm-yyyy):\n")
            result = self.event_logic.display_events_by_period(path_to_auth, start_date, end_date)
            self._handle_display_result(result)
            if result != "No events found for this period.":
                self.output_choice(path_to_auth)

    def _handle_display_result(self, result):
        if isinstance(result, str):
            print(result)
        elif isinstance(result, list):
            for event in result:
                if isinstance(event, str):
                    print(event)
                elif isinstance(event, dict):
                    for key, value in event.items():
                        if isinstance(value, list) and not value:
                            value = "No participants"
                        print(f"{key}: {value}")
                    print()
        elif isinstance(result, dict):
            for key, value in result.items():
                if isinstance(value, list) and not value:
                    value = "No participants"
                print(f"{key}: {value}")
            print()

    def output_choice(self, path_to_auth):
        num = int(input("If you want to output a specific event, enter 1, otherwise, any other digit\n"))
        if num == 1:
            date = input("Enter the date (dd-mm-yyyy):\n")
            result = self.event_logic.display_events_by_day(path_to_auth, date)
            self._handle_display_result(result)
        else:
            pass