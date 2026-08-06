"""Acceptance tests for the Module 16 FastAPI exercise.

Install the supplied requirements before running this file:
    python -m pip install -r requirements.txt
    python test_app.py
"""

import unittest

from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


class ApiTests(unittest.TestCase):
    def test_health_baseline(self):
        response = client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_analyze_text_returns_length_and_checksum(self):
        response = client.post("/analyze-text", json={"text": "GitHub Foundations"})
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["length"], len("GitHub Foundations"))
        self.assertIsInstance(payload["checksum"], str)
        self.assertGreaterEqual(len(payload["checksum"]), 16)

    def test_analyze_text_is_deterministic(self):
        first = client.post("/analyze-text", json={"text": "same input"}).json()
        second = client.post("/analyze-text", json={"text": "same input"}).json()
        self.assertEqual(first["checksum"], second["checksum"])

    def test_blank_text_is_rejected(self):
        response = client.post("/analyze-text", json={"text": "   "})
        self.assertGreaterEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
