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
    # Regular expression to remove all numbers, English letters, and special characters
    # and retain Devanagari characters and spaces
    cleaned_text = re.sub(r'[^\u0900-\u097F\s।]', '', text)  # Devanagari Unicode range
    # Replace double or triple spaces with a single space
    cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text)
    # Replace the period (।) with a period followed by a newline
    cleaned_text = re.sub(r'।', '।\n', cleaned_text)
    return cleaned_text

