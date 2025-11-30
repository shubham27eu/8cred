import spacy
from spacy.tokens import Span
import fitz

from spacy.pipeline import EntityRuler

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Add a custom EntityRuler to the pipeline for phone numbers and emails
ruler = nlp.add_pipe("entity_ruler", before="ner")
patterns = [
    {"label": "PHONE_NUMBER", "pattern": [{"SHAPE": "ddd"}, {"TEXT": "-"}, {"SHAPE": "ddd"}, {"TEXT": "-"}, {"SHAPE": "dddd"}]},
    {"label": "PHONE_NUMBER", "pattern": [{"TEXT": "("}, {"SHAPE": "ddd"}, {"TEXT": ")"}, {"SHAPE": "ddd"}, {"TEXT": "-"}, {"SHAPE": "dddd"}]},
    {"label": "PHONE_NUMBER", "pattern": [{"SHAPE": "ddd"}, {"TEXT": "."}, {"SHAPE": "ddd"}, {"TEXT": "."}, {"SHAPE": "dddd"}]},
    {"label": "EMAIL_ADDRESS", "pattern": [{"LIKE_EMAIL": True}]},
]
ruler.add_patterns(patterns)

# Define a mapping from custom categories to spaCy's entity labels
ENTITY_MAP = {
    "PERSON": "PERSON",
    "LOCATION": "GPE",
    "DATE": "DATE",
    # Note: spaCy's default model may not reliably detect phone numbers or emails.
    # Custom rules or models would be needed for higher accuracy.
    "PHONE_NUMBER": "PHONE_NUMBER",
    "EMAIL_ADDRESS": "EMAIL_ADDRESS",
}

def redact_entities(page: fitz.Page, semantic_rules: list[dict]):
    """
    Identifies and redacts named entities on a PDF page based on semantic rules.
    """
    words = page.get_text("words")
    if not words:
        return

    text_from_words = " ".join([w[4] for w in words])
    doc = nlp(text_from_words)

    # Get a set of required entity labels for efficiency
    required_labels = {ENTITY_MAP.get(rule["category"]) for rule in semantic_rules if ENTITY_MAP.get(rule["category"])}

    ents_to_redact = [ent for ent in doc.ents if ent.label_ in required_labels]

    if not ents_to_redact:
        return

    current_offset = 0
    for word in words:
        word_text = word[4]
        word_start = current_offset
        word_end = word_start + len(word_text)

        for ent in ents_to_redact:
            # Check for overlap between word and entity spans
            if max(word_start, ent.start_char) < min(word_end, ent.end_char):
                word_bbox = fitz.Rect(word[:4])
                page.add_redact_annot(word_bbox, fill=(0, 0, 0))
                break  # Move to the next word once redacted

        current_offset = word_end + 1
