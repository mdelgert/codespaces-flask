import re

def remove_zero_width_chars(text):
    # Remove zero-width characters
    return re.sub(r'[\u200B\u200C\u200D]', '', text)

text = "This is some text\u200b with zero-width\u200c characters\u200d."
clean_text = remove_zero_width_chars(text)
print(clean_text)
