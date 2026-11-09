"""Tests for the reply engine. Run: python -m unittest discover -s tests -v"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.reply_engine import analyse_email, generate_replies  # noqa: E402


class TestAnalysis(unittest.TestCase):
    def test_detects_price_and_meeting(self):
        a = analyse_email("What is your price? Can we schedule a call on Friday?")
        self.assertIn("price", a.intents)
        self.assertIn("meeting", a.intents)
        self.assertEqual(len(a.questions), 2)
        self.assertIn("Friday", a.mentioned_dates)

    def test_detects_urgency_and_sender(self):
        a = analyse_email("This is urgent, please reply today. Regards, Ahmed")
        self.assertTrue(a.urgent)
        self.assertEqual(a.sender_name, "Ahmed")

    def test_detects_complaint(self):
        a = analyse_email("I am not happy, the delivery was late and I want a refund.")
        self.assertIn("complaint", a.intents)


class TestGeneration(unittest.TestCase):
    def test_three_variants_and_signoff(self):
        r = generate_replies("Hi, thank you for the great work!", your_name="Hasnaat")
        self.assertEqual(set(r["replies"]), {"detailed", "balanced", "short"})
        for reply in r["replies"].values():
            self.assertIn("Hasnaat", reply)

    def test_unknown_tone_falls_back_to_professional(self):
        r = generate_replies("Hello there.", tone="angry")
        self.assertIn("Best regards", r["replies"]["detailed"])

    def test_purpose_is_included(self):
        r = generate_replies("Any update?", purpose="Confirm delivery on Friday.")
        self.assertIn("Confirm delivery on Friday.", r["replies"]["detailed"])


if __name__ == "__main__":
    unittest.main()
