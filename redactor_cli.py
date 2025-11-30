import argparse
import os
from src.redactor import redact_pdf

def main():
    parser = argparse.ArgumentParser(description="Redact sensitive information from PDF files.")
    parser.add_argument(
        "-i", "--input",
        nargs="+",
        required=True,
        help="One or more input PDF files or a directory containing PDF files."
    )
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="The directory where redacted PDFs will be saved."
    )
    parser.add_argument(
        "-r", "--rules",
        required=True,
        help="Path to a file containing redaction rules (one regex per line)."
    )

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    # Load redaction rules from the YAML file
    with open(args.rules, "r") as f:
        try:
            import yaml
            rules = yaml.safe_load(f).get("rules", [])
        except yaml.YAMLError as e:
            print(f"Error parsing YAML rule file: {e}")
            return

    # Separate patterns and semantic rules for processing
    patterns = [rule["pattern"] for rule in rules if rule.get("type") == "regex" and "pattern" in rule]
    semantic_rules = [rule for rule in rules if rule.get("type") == "semantic" and "category" in rule]

    # Process input files
    input_paths = []
    for item in args.input:
        if os.path.isdir(item):
            for filename in os.listdir(item):
                if filename.lower().endswith(".pdf"):
                    input_paths.append(os.path.join(item, filename))
        elif os.path.isfile(item) and item.lower().endswith(".pdf"):
            input_paths.append(item)

    if not input_paths:
        print("No PDF files found in the specified input.")
        return

    for input_path in input_paths:
        base_name = os.path.basename(input_path)
        output_path = os.path.join(args.output, base_name)
        print(f"Redacting {input_path} -> {output_path}")
        redact_pdf(input_path, output_path, patterns, semantic_rules)

    print("Redaction complete.")

if __name__ == "__main__":
    main()