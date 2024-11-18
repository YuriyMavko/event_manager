from datetime import datetime, timedelta
from file_manager import FileManager
from validate import Date


class Event:
    def __init__(self, file_manager):
        self.title = ""
        self.description = ""
        self.date = ""
        self.participant = []
        self.file_manager = file_manager

    def add_event(self, title, description, date, participants):
        obj_date = Date()
        if not obj_date.validate_date(date):
            raise ValueError("Invalid date format.")

        self.title = title
        self.description = description
        self.date = date
        self.participant = participants

        day, month, year = date.split("-")
        file_path = f"{day}-{month}-{year}/{date}.json"
        data = {
            "title": self.title,
            "description": self.description,
            "date": self.date,
            "participants": self.participant
        }
        self.file_manager.write_file(file_path, data)
        self._update_all_events_file(date, title)

    def _update_all_events_file(self, date, title):
        all_events_path = "all_events.txt"
        new_entry = f"{date} {title}\n"
        events = self.file_manager.read_file(all_events_path).splitlines() if self.file_manager.file_exists(all_events_path) else []

        events.append(new_entry)
        events.sort(key=lambda x: datetime.strptime(x.split()[0], "%d-%m-%Y"))

        self.file_manager.write_file(all_events_path, "\n".join(events))

    def delete_event(self, date):
        day, month, year = date.split("-")
        file_path = f"{day}-{month}-{year}/{date}.json"

        if self.file_manager.file_exists(file_path):
            data = self.file_manager.read_file(file_path)
            title = data.get('title', 'unknown')
            self.file_manager.delete_file(file_path)
            self._remove_event_from_all_events(date, title)
        else:
            raise FileNotFoundError("Event not found.")

    def _remove_event_from_all_events(self, date, title):
        all_events_path = "all_events.txt"
        if self.file_manager.file_exists(all_events_path):
            events = self.file_manager.read_file(all_events_path).splitlines()
            events = [event for event in events if not event.startswith(f"{date} {title}")]
            self.file_manager.write_file(all_events_path, "\n".join(events))
