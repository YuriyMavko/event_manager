import unittest
from datetime import datetime
from event import Event
from file_manager import FileManager


class TestEvent(unittest.TestCase):
    def setUp(self):
        self.file_manager = FileManager()
        self.event = Event(self.file_manager)
        self.test_path = "test_events"

    def test_add_event(self):
        title = "Test Event"
        description = "Test Description"
        date = "01-01-2024"
        participants = ["John", "Jane"]

        self.event.add_event(self.test_path, title, description, date, participants)
        file_path = f"{self.test_path}/01-01-2024/{date}.json"
        self.assertTrue(self.file_manager.file_exists(file_path))
        data = self.file_manager.read_json(file_path)
        self.assertEqual(data["title"], title)
        self.assertEqual(data["description"], description)
        self.assertEqual(data["date"], date)
        self.assertEqual(data["participants"], participants)

    def test_update_event(self):
        self.event.add_event(self.test_path, "Original Title", "Original Desc", "01-01-2024", ["John"])
        updated_data = {
            "title": "Updated Title",
            "description": "Updated Description"
        }

        self.event.update_event(self.test_path, "01-01-2024", updated_data)
        file_path = f"{self.test_path}/01-01-2024/01-01-2024.json"
        data = self.file_manager.read_json(file_path)
        self.assertEqual(data["title"], "Updated Title")
        self.assertEqual(data["description"], "Updated Description")

    def test_delete_event(self):
        date = "01-01-2024"
        self.event.add_event(self.test_path, "Test Event", "Test Description", date, ["John"])

        self.event.delete_event(self.test_path, date)
        file_path = f"{self.test_path}/01-01-2024/{date}.json"
        self.assertFalse(self.file_manager.file_exists(file_path))

    def test_display_events_by_year(self):
        self.event.add_event(self.test_path, "Event 1", "Desc 1", "01-01-2024", ["John"])
        self.event.add_event(self.test_path, "Event 2", "Desc 2", "01-02-2024", ["Jane"])

        events = self.event.display_events_by_year(self.test_path, "2024")
        self.assertEqual(len(events), 2)
        self.assertTrue(any("Event 1" in event for event in events))
        self.assertTrue(any("Event 2" in event for event in events))

    def test_display_events_by_period(self):
        self.event.add_event(self.test_path, "Event 1", "Desc 1", "01-01-2024", ["John"])
        self.event.add_event(self.test_path, "Event 2", "Desc 2", "15-01-2024", ["Jane"])
        self.event.add_event(self.test_path, "Event 3", "Desc 3", "01-02-2024", ["Bob"])

        events = self.event.display_events_by_period(self.test_path, "01-01-2024", "20-01-2024")
        self.assertEqual(len(events), 2)
        self.assertTrue(any("Event 1" in event for event in events))
        self.assertTrue(any("Event 2" in event for event in events))
        self.assertFalse(any("Event 3" in event for event in events))

    def tearDown(self):
        import shutil
        import os
        if os.path.exists(self.test_path):
            shutil.rmtree(self.test_path)


if __name__ == '__main__':
    unittest.main()