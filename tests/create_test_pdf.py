import fitz
import os

def create_sample_pdf(path: str):
    """Creates a sample PDF for testing by inserting text line-by-line."""
    doc = fitz.open()
    page = doc.new_page()

    lines = [
        "This is a test PDF.",
        "My phone number is 123-456-7890.",
        "My email is test@example.com.",
        "This is some other text.",
        "Another email: another.test@example.com"
    ]

    y = 72
    for line in lines:
        page.insert_text((50, y), line, fontsize=11)
        y += 15

    doc.save(path)
    doc.close()

if __name__ == "__main__":
    if not os.path.exists("tests"):
        os.makedirs("tests")
    create_sample_pdf("tests/sample.pdf")