# PDF Redaction Tool

This is a command-line tool for automatically redacting sensitive information from PDF documents using regular expressions and semantic analysis.

## Features

*   **Regex-Based Redaction**: Define custom patterns using regular expressions to find and redact sensitive text.
*   **Semantic Redaction**: Redact common categories of information like phone numbers, email addresses, and names without writing custom regex.
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
    python3.11 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Download the spaCy language model:**
    This is required for the semantic redaction feature.
    ```bash
    python -m spacy download en_core_web_sm
    ```

## Usage

The tool is run from the command line.

### Command-Line Arguments

*   `-i`, `--input`: (Required) One or more input PDF files or a directory containing PDF files.
*   `-o`, `--output`: (Required) The directory where redacted PDFs will be saved.
*   `-r`, `--rules`: (Required) Path to a YAML file containing redaction rules.

### Rule File Format

The redaction rules are defined in a YAML file. The file should contain a list of rules, where each rule has a `name`, `type`, and either a `pattern` (for regex) or a `category` (for semantic).

**Example `rules.yaml`:**

```yaml
rules:
  - name: "Redact Social Security Numbers"
    type: "regex"
    pattern: "\\b\\d{3}-\\d{2}-\\d{4}\\b"
  - name: "Redact Email Addresses"
    type: "semantic"
    category: "EMAIL_ADDRESS"
  - name: "Redact Phone Numbers"
    type: "semantic"
    category: "PHONE_NUMBER"
  - name: "Redact People's Names"
    type: "semantic"
    category: "PERSON"
  - name: "Redact Locations"
    type: "semantic"
    category: "LOCATION"
  - name: "Redact Dates"
    type: "semantic"
    category: "DATE"
```

### Example

This repository includes sample files in the `examples/` directory to help you get started.

*   `examples/input/sample.pdf`: A sample PDF containing sensitive information.
*   `examples/rules.yaml`: A sample rules file with both regex and semantic rules.

To run the tool with the sample files:

1.  **Create an output directory for the redacted files:**
    ```bash
    mkdir output_pdfs
    ```

2.  **Run the redaction tool:**
    ```bash
    python3 redactor_cli.py -i examples/input/sample.pdf -o output_pdfs/ -r examples/rules.yaml
    ```

After the script finishes, a redacted version of `sample.pdf` will be available in the `output_pdfs` directory.
