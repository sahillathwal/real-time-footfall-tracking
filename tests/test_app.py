import unittest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

class TestAPI(unittest.TestCase):
    def test_health_check(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Real-time Footfall Tracking API"})

if __name__ == "__main__":
    unittest.main()
