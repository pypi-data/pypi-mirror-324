# bodoTK/tokenize.py
import re

def sentence_tokenize(text):
    """Tokenize text into sentences."""
    # Basic approach: split by common sentence-ending punctuation
    sentences = re.split(r'(?<=[.!?]) +', text.strip())
    return sentences


def word_tokenize(text):
    """Tokenize text into words."""
    # Updated regex for Devanagari words
    words = re.findall(r'[\u0900-\u097F]+', text)  # This captures words in the Devanagari script
    return words


def char_tokenize(text):
    """Tokenize text into characters."""
    words = re.findall(r'\b\w+\b', text)
    return list(text)


def clean_bodotext(text):
    # Remove English characters (a-z, A-Z), numbers (0-9), and other non-Devanagari characters
    cleaned_text = re.sub(r'[a-zA-Z0-9]', '', text)
    # Remove all characters except for Devanagari characters
    cleaned_text = re.sub(r'[^\u0900-\u097F]', ' ', cleaned_text)  # Unicode range for Devanagari characters
    # Replace multiple spaces with a single space
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    # Trim leading and trailing spaces
    cleaned_text = cleaned_text.strip()
    # Replace Devanagari danda '।' with a newline
    cleaned_text = re.sub(r'।', '\n', cleaned_text)
    return cleaned_text