import os
import json
from datetime import datetime, timedelta
from validate import Date

class Event:
    def __init__(self):
        self.title = ""
        self.description = ""
        self.date = ""
        self.participant = []

    def add_event(self, path_to_auth, title=None, description=None, date=None, participant=None):
        obj_date = Date()
        if title is not None and description is not None and date is not None and participant is not None:
            self.title = title
            self.description = description
            self.date = date
            self.participant = participant
        else:
            raise ValueError("Input required from an interface class")

        data = {
            "title": self.title,
            "description": self.description,
            "date": self.date,
            "participants": self.participant
        }

        day, month, year = self.date.split("-")
        year_dir = f"{path_to_auth}/{year}"
        os.makedirs(year_dir, exist_ok=True)
        with open(os.path.join(year_dir, f"all_events_{year}.txt"), 'a') as year_file:
            year_file.write(f"{self.date} {self.title}\n")

        month_dir = os.path.join(year_dir, f"{month}")
        os.makedirs(month_dir, exist_ok=True)
        with open(os.path.join(month_dir, f"all_events_{month}.txt"), "a") as month_file:
            month_file.write(f"{self.date} {self.title}\n")

        day_dir = os.path.join(month_dir, f"{day}")
        os.makedirs(day_dir, exist_ok=True)
        path = os.path.join(day_dir, f"{self.date}.json")
        with open(path, 'w', encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

    def update_event(self, path_to_auth, date, updated_data):
        obj_date = Date()
        day, month, year = date.split("-")
        path_to_json = f"{path_to_auth}/{year}/{month}/{day}/{date}.json"

        if os.path.exists(path_to_json):
            with open(path_to_json) as file:
                data = json.load(file)
            origin_data = data.copy()
            new_data = {**data, **updated_data}

            if date == new_data["date"]:
                with open(path_to_json, 'w', encoding="utf-8") as json_file:
                    json.dump(new_data, json_file, ensure_ascii=False, indent=4)
            else:
                self._handle_date_change(path_to_auth, origin_data, new_data, date, day, month, year)
        else:
            raise FileNotFoundError("Event not found")

    def _handle_date_change(self, path_to_auth, origin_data, new_data, old_date, day, month, year):
        old_path = f"{path_to_auth}/{year}/{month}/{day}/{old_date}.json"
        new_day, new_month, new_year = new_data["date"].split("-")
        new_path = f"{path_to_auth}/{new_year}/{new_month}/{new_day}/{new_data['date']}.json"

        os.makedirs(os.path.dirname(new_path), exist_ok=True)

        with open(new_path, 'w', encoding="utf-8") as new_file:
            json.dump(new_data, new_file, ensure_ascii=False, indent=4)

        if os.path.exists(old_path):
            os.remove(old_path)

        self._remove_event_from_logs(path_to_auth, year, month, day, origin_data["title"])
        self._update_event_logs(path_to_auth, new_data["date"], new_data["title"])

    def _remove_event_from_logs(self, path_to_auth, year, month, day, title):
        year_file_path = f"{path_to_auth}/{year}/all_events_{year}.txt"
        month_file_path = f"{path_to_auth}/{year}/{month}/all_events_{month}.txt"

        def remove_line_from_file(file_path, line_to_remove):
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                with open(file_path, 'w') as file:
                    for line in lines:
                        if line.strip() != line_to_remove:
                            file.write(line)

        remove_line_from_file(year_file_path, f"{day}-{month}-{year} {title}")
        remove_line_from_file(month_file_path, f"{day}-{month}-{year} {title}")

    def _update_event_logs(self, path_to_auth, new_date, title):
        new_day, new_month, new_year = new_date.split("-")
        year_log_path = f"{path_to_auth}/{new_year}/all_events_{new_year}.txt"
        month_log_path = f"{path_to_auth}/{new_year}/{new_month}/all_events_{new_month}.txt"

        with open(year_log_path, 'a') as year_log:
            year_log.write(f"{new_date} {title}\n")

        with open(month_log_path, 'a') as month_log:
            month_log.write(f"{new_date} {title}\n")

    def delete_event(self, path_to_auth, date):
        day, month, year = date.split("-")
        path_to_file = f"{path_to_auth}/{year}/{month}/{day}/{date}.json"

        if os.path.exists(path_to_file):
            with open(path_to_file, 'r') as file:
                data = json.load(file)
            title = data.get('title', 'nothing')
            os.remove(path_to_file)
            self._remove_event_from_logs(path_to_auth, year, month, day, title)
        else:
            raise FileNotFoundError("Event not found")

    def display_events_by_year(self, path_to_auth, year):
        path = f"{path_to_auth}/{year}/all_events_{year}.txt"
        if os.path.exists(path):
            with open(path, 'r') as file:
                return file.read()
        else:
            return "No events found for this year."

    def display_events_by_month(self, path_to_auth, year, month):
        path = f"{path_to_auth}/{year}/{month}/all_events_{month}.txt"
        if os.path.exists(path):
            with open(path, 'r') as file:
                return file.read()
        else:
            return "No events found for this month."

    def display_events_by_day(self, path_to_auth, date):
        day, month, year = date.split("-")
        path = f"{path_to_auth}/{year}/{month}/{day}/{date}.json"
        if os.path.exists(path):
            with open(path, 'r') as file:
                event = json.load(file)
                return event
        else:
            return "No events found for this day."

    def display_events_by_period(self, path_to_auth, start_date, end_date):
        start_dt = datetime.strptime(start_date, "%d-%m-%Y")
        end_dt = datetime.strptime(end_date, "%d-%m-%Y")
        current_date = start_dt
        events_summary = []

        while current_date <= end_dt:
            date_str = current_date.strftime("%d-%m-%Y")
            day, month, year = date_str.split("-")
            path = f"{path_to_auth}/{year}/{month}/{day}/{day}-{month}-{year}.json"

            if os.path.exists(path):
                with open(path, 'r') as file:
                    uploaded_data = json.load(file)
                    date = uploaded_data.get("date", "")
                    title = uploaded_data.get("title", "")
                    events_summary.append(date + " " + title)

            current_date += timedelta(days=1)

        return events_summary if events_summary else "No events found for this period."