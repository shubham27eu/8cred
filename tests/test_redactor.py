import unittest
import os
import fitz
import sys

# Add the project root to the Python path to allow for absolute imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.redactor import redact_pdf
from tests.create_test_pdf import create_sample_pdf

class TestRedactor(unittest.TestCase):

    def setUp(self):
        """Set up for the test."""
        self.sample_pdf_path = "tests/sample.pdf"
        self.redacted_pdf_path = "tests/redacted_sample.pdf"
        self.rules_path = "tests/rules.txt"

        # Create a sample PDF for testing
        if not os.path.exists("tests"):
            os.makedirs("tests")
        create_sample_pdf(self.sample_pdf_path)

        # Create a rules file with normal strings
        with open(self.rules_path, "w") as f:
            f.write("\\d{3}-\\d{3}-\\d{4}\n")
            f.write("[\\w\\.-]+@[\\w\\.-]+\\.\\w+\n")

    def tearDown(self):
        """Clean up after the test."""
        if os.path.exists(self.sample_pdf_path):
            os.remove(self.sample_pdf_path)
        if os.path.exists(self.redacted_pdf_path):
            os.remove(self.redacted_pdf_path)
        if os.path.exists(self.rules_path):
            os.remove(self.rules_path)

    def test_redaction(self):
        """Test if sensitive information is redacted correctly."""
        # Get patterns from rules file
        with open(self.rules_path, "r") as f:
            patterns = [line.strip() for line in f if line.strip()]

        # Redact the PDF
        redact_pdf(self.sample_pdf_path, self.redacted_pdf_path, patterns)

        # Verify the redaction
        doc = fitz.open(self.redacted_pdf_path)
        redacted_text = ""
        for page in doc:
            redacted_text += page.get_text()

        doc.close()

        # Assert that the sensitive information is no longer in the text
        self.assertNotIn("123-456-7890", redacted_text)
        self.assertNotIn("test@example.com", redacted_text)
        self.assertNotIn("another.test@example.com", redacted_text)

        # Assert that other text is still present
        self.assertIn("This is a test PDF.", redacted_text)
        self.assertIn("This is some other text.", redacted_text)

if __name__ == "__main__":
    unittest.main()