import ftfy
import re

def clean_text(text):
    # First, apply ftfy to fix text
    text = ftfy.fix_text(text)
    # Then, remove specific zero-width characters
    text = re.sub(r'[\u200B\u200C\u200D]', '', text)
    return text

text = "Some problematic text\u200b with hidden\u200c characters\u200d."
cleaned = clean_text(text)
print(cleaned)