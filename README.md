# PDF Redaction Tool

This is a command-line tool for automatically redacting sensitive information from PDF documents using regular expressions.

## Features

*   **Regex-Based Redaction**: Define custom patterns using regular expressions to find and redact sensitive text.
*   **Batch Processing**: Process a single PDF, multiple PDFs, or an entire directory of PDFs at once.
*   **Simple CLI**: Easy-to-use command-line interface for specifying inputs, outputs, and redaction rules.
*   **Secure Redaction**: Redacted content is permanently removed from the PDF.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Install the required dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

## Usage

The tool is run from the command line.

### Command-Line Arguments

*   `-i`, `--input`: (Required) One or more input PDF files or a directory containing PDF files.
*   `-o`, `--output`: (Required) The directory where redacted PDFs will be saved.
*   `-r`, `--rules`: (Required) Path to a file containing redaction rules (one regex per line).

### Example

1.  **Create a rules file.**
    Create a file named `rules.txt` and add your regular expression patterns. Each pattern should be on a new line. For example, to redact phone numbers and email addresses:
    ```
    \d{3}-\d{3}-\d{4}
    [\w\.-]+@[\w\.-]+\.\w+
    ```

2.  **Prepare your input files.**
    Place the PDF files you want to redact into a directory (e.g., `input_pdfs/`).

3.  **Create an output directory.**
    This is where the redacted PDFs will be saved.
    ```bash
    mkdir output_pdfs
    ```

4.  **Run the redaction tool.**

    *   **To process a single file:**
        ```bash
        python3 -m src.cli -i input_pdfs/document1.pdf -o output_pdfs/ -r rules.txt
        ```

    *   **To process all PDFs in a directory:**
        ```bash
        python3 -m src.cli -i input_pdfs/ -o output_pdfs/ -r rules.txt
        ```

After the script finishes, the `output_pdfs` directory will contain the redacted versions of your PDF files.