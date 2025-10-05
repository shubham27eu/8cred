import fitz
import re

def redact_pdf(input_path: str, output_path: str, patterns: list[str]):
    """
    Redacts a PDF file by finding words that match given regex patterns.
    Note: This approach works best for sensitive information that is a single "word"
    (e.g., email, phone number) and does not span across multiple words.
    """
    doc = fitz.open(input_path)

    # Compile regex patterns for efficiency
    compiled_patterns = [re.compile(p) for p in patterns]

    for page in doc:
        # Get all words on the page with their bounding boxes
        words = page.get_text("words")

        for word in words:
            word_text = word[4]
            word_bbox = fitz.Rect(word[:4])

            for pattern in compiled_patterns:
                # Use search to find a match within the word
                if pattern.search(word_text):
                    # If a match is found, redact the entire word's bounding box
                    page.add_redact_annot(word_bbox, fill=(0, 0, 0))
                    # Once a word is marked for redaction, no need to check other patterns
                    break

        # Apply all redactions for the current page
        page.apply_redactions()

    # Save the redacted document
    doc.save(output_path)
    doc.close()

if __name__ == '__main__':
    # Example usage:
    # This part is for demonstration and won't be executed when imported.
    # To run this, you would need to create a sample PDF and a rules file.
    pass