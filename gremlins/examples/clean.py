import ftfy
import re

def clean_text(text):
    # First, apply ftfy to fix text
    text = ftfy.fix_text(text)
    
    # Define a mapping of specific Unicode characters to their replacements
    replacements = {
        '\u00A0': ' ',  # No-Break Space
        '\u200B': '',   # Zero-Width Space
        '\u200C': '',   # Zero-Width Non-Joiner
        '\u200D': '',   # Zero-Width Joiner
        '\u200E': '',   # Left-To-Right Mark
        '\u200F': '',   # Right-To-Left Mark
        '\u202A': '',   # Left-To-Right Embedding
        '\u202B': '',   # Right-To-Left Embedding
        '\u202C': '',   # Pop Directional Formatting
        '\u202D': '',   # Left-To-Right Override
        '\u202E': '',   # Right-To-Left Override
        '\u2060': '',   # Word Joiner
        '\u2061': '',   # Function Application
        '\u2062': 'x',  # Invisible Times
        '\u2063': ',',  # Invisible Separator
        '\u2064': '+',  # Invisible Plus
        '\u2066': '',   # Left-To-Right Isolate
        '\u2067': '',   # Right-To-Left Isolate
        '\u2068': '',   # First Strong Isolate
        '\u2069': '',   # Pop Directional Isolate
        '\u00AD': '-',  # Soft Hyphen
        '\u034F': '',   # Combining Grapheme Joiner
        '\uFEFF': '',   # Zero-Width No-Break Space
        '\uFFFC': '[OBJECT]',  # Object Replacement Character
        # Add more mappings as needed
    }
    
    # Replace characters based on the mapping
    for target, replacement in replacements.items():
        text = text.replace(target, replacement)
    
    # Optionally, remove other control characters
    text = re.sub(r'[\u0000-\u001F\u007F]', '', text)
    
    return text

def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python clean.py <input_file>")
        sys.exit(1)
    input_path = sys.argv[1]
    if '.' in input_path:
        output_path = input_path.rsplit('.', 1)[0] + ".cleaned.txt"
    else:
        output_path = input_path + ".cleaned.txt"
    with open(input_path, "r", encoding="utf-8") as infile:
        content = infile.read()
    cleaned = clean_text(content)
    with open(output_path, "w", encoding="utf-8") as outfile:
        outfile.write(cleaned)
    print(f"Cleaned file written to: {output_path}")

if __name__ == "__main__":
    main()

# Example usage:
# python clean.py test.txt
# This script cleans text by fixing encoding issues and removing unwanted Unicode characters.
# It can be used to preprocess text files before further processing or analysis.
# This script cleans text by fixing encoding issues and removing unwanted Unicode characters.