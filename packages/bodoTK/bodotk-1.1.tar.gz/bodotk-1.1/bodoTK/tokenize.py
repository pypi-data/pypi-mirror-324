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
