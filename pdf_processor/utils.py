import unicodedata

def normalize_text(text):
    # Unicode normalization, strip, collapse whitespace
    text = unicodedata.normalize('NFKC', text)
    text = ' '.join(text.strip().split())
    return text 