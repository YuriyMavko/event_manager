import unittest
import os
import json
from event import Event

class TestEvent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.path_to_auth = 'test_events'
        os.makedirs(cls.path_to_auth, exist_ok=True)
        cls.event = Event()

    @classmethod
    def tearDownClass(cls):
        for root, dirs, files in os.walk(cls.path_to_auth, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(cls.path_to_auth)

    def test_add_event(self):
        event_data = {
            "title": "Meeting",
            "description": "Project discussion",
            "date": "15-11-2024",
            "participant": ["Alice", "Bob"]
        }
        self.event.add_event(self.path_to_auth, **event_data)
        date_path = os.path.join(self.path_to_auth, '2024', '11', '15', '15-11-2024.json')
        self.assertTrue(os.path.exists(date_path))

        with open(date_path, 'r') as file:
            data = json.load(file)
            self.assertEqual(data['title'], "Meeting")

    def test_update_event(self):
        self.event.add_event(self.path_to_auth, "Meeting", "Project discussion", "15-11-2024", ["Alice", "Bob"])

        updated_data = {
            "title": "Updated Meeting",
            "description": "Updated discussion",
            "date": "15-11-2024",
            "participant": ["Alice", "Charlie"]
        }
        self.event.update_event(self.path_to_auth, "15-11-2024", updated_data)

        date_path = os.path.join(self.path_to_auth, '2024', '11', '15', '15-11-2024.json')
        with open(date_path, 'r') as file:
            data = json.load(file)
            self.assertEqual(data['title'], "Updated Meeting")

    def test_display_events_by_year(self):
        self.assertEqual(self.event.display_events_by_year(self.path_to_auth, "2023"), "No events found for this year.")

    def test_display_events_by_month(self):
        self.assertEqual(self.event.display_events_by_month(self.path_to_auth, "2024", "12"), "No events found for this month.")

    def test_delete_event(self):
        self.event.add_event(self.path_to_auth, "Meeting", "Project discussion", "15-11-2024", ["Alice", "Bob"])
        self.event.delete_event(self.path_to_auth, "15-11-2024")
        date_path = os.path.join(self.path_to_auth, '2024', '11', '15', '15-11-2024.json')
        self.assertFalse(os.path.exists(date_path))


if __name__ == '__main__':
    unittest.main()
