from django.test import SimpleTestCase

from requests_app.ai import triage


class TriageTests(SimpleTestCase):
    def test_billing_category(self):
        r = triage("Refund needed", "I was charged twice on my invoice.")
        self.assertEqual(r["category"], "billing")

    def test_account_category(self):
        r = triage("Locked out", "I forgot my password and cannot log in.")
        self.assertEqual(r["category"], "account")

    def test_urgent_priority(self):
        r = triage("Server", "Production down, please fix ASAP.")
        self.assertEqual(r["priority"], "urgent")

    def test_default_general_medium(self):
        r = triage("Hello", "Just saying hi to the team.")
        self.assertEqual((r["category"], r["priority"]), ("general", "medium"))

    def test_summary_truncated(self):
        r = triage("Long", "word " * 100)
        self.assertLessEqual(len(r["summary"]), 140)
