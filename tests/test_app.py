import importlib
import sys
import unittest
from unittest.mock import patch


class FakeCollection:
    def __init__(self):
        self.docs = []

    def find(self):
        return list(self.docs)

    def insert_one(self, data):
        doc = dict(data)
        doc["_id"] = "1"
        doc["createdAt"] = "2024-01-01T00:00:00"
        self.docs.append(doc)
        return type("Result", (), {"inserted_id": "1"})()

    def update_one(self, *args, **kwargs):
        return None


class FakeDB:
    def __init__(self):
        self.attendence = FakeCollection()

    def __getitem__(self, name):
        return self.attendence


class FakeClient:
    def __init__(self):
        self.db = FakeDB()

    def __getitem__(self, name):
        return self.db


class AppRouteTests(unittest.TestCase):
    def test_add_member_returns_updated_attendance_json(self):
        with patch("pymongo.MongoClient", return_value=FakeClient()):
            sys.modules.pop("app", None)
            app_module = importlib.import_module("app")
            client = app_module.app.test_client()

            response = client.post(
                "/add_member",
                json={"name": "Ada", "gender": "Female"},
            )

            self.assertEqual(response.status_code, 200)
            payload = response.get_json()
            self.assertTrue(payload["success"])
            self.assertEqual(payload["data"][0]["name"], "Ada")
            self.assertEqual(payload["data"][0]["gender"], "Female")


if __name__ == "__main__":
    unittest.main()
