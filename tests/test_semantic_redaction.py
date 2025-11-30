import unittest
import os
import fitz
from src.redactor import redact_pdf

class TestSemanticRedaction(unittest.TestCase):
    def setUp(self):
        self.input_pdf = "test_semantic_input.pdf"
        self.output_pdf = "test_semantic_output.pdf"
        self.rules_file = "test_semantic_rules.yaml"

        # Create a dummy PDF for testing
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((50, 72), "Contact us at john.doe@example.com or 123-456-7890.")
        page.insert_text((50, 92), "Our office is in New York.")
        page.insert_text((50, 112), "The CEO is Jane Smith.")
        doc.save(self.input_pdf)
        doc.close()

        # Create a dummy rules file for testing
        with open(self.rules_file, "w") as f:
            f.write("""
rules:
  - name: "Redact Email Addresses"
    type: "semantic"
    category: "EMAIL_ADDRESS"
  - name: "Redact Phone Numbers"
    type: "semantic"
    category: "PHONE_NUMBER"
  - name: "Redact Locations"
    type: "semantic"
    category: "LOCATION"
  - name: "Redact People"
    type: "semantic"
    category: "PERSON"
""")

    def tearDown(self):
        os.remove(self.input_pdf)
        os.remove(self.output_pdf)
        os.remove(self.rules_file)

    def test_semantic_redaction(self):
        # Load the rules
        import yaml
        with open(self.rules_file, "r") as f:
            rules = yaml.safe_load(f).get("rules", [])
        patterns = [rule["pattern"] for rule in rules if rule.get("type") == "regex" and "pattern" in rule]
        semantic_rules = [rule for rule in rules if rule.get("type") == "semantic" and "category" in rule]

        # Run the redaction
        redact_pdf(self.input_pdf, self.output_pdf, patterns, semantic_rules)

        # Verify the redaction
        doc = fitz.open(self.output_pdf)
        page = doc[0]
        text = page.get_text("text")
        self.assertNotIn("john.doe@example.com", text)
        self.assertNotIn("123-456-7890", text)
        self.assertNotIn("New York", text)
        self.assertNotIn("Jane Smith", text)
        doc.close()

if __name__ == "__main__":
    unittest.main()
