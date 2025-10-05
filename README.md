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

This repository includes sample files in the `examples/` directory to help you get started.

*   `examples/input/sample.pdf`: A sample PDF containing sensitive information like phone numbers and email addresses.
*   `examples/rules.txt`: A sample rules file with patterns to redact the information found in `sample.pdf`.

To run the tool with the sample files:

1.  **Create an output directory for the redacted files:**
    ```bash
    mkdir output_pdfs
    ```

2.  **Run the redaction tool:**
    This command will process `sample.pdf` using the provided rules and save the redacted version in the `output_pdfs` directory.
    ```bash
    python3 redactor_cli.py -i examples/input/sample.pdf -o output_pdfs/ -r examples/rules.txt
    ```

After the script finishes, a redacted version of `sample.pdf` will be available in the `output_pdfs` directory. You can adapt this command to use your own input files and rules.