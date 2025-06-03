import ftfy
import re
import sys
import argparse
import logging
from typing import List, Tuple
import importlib.metadata

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def define_replacement_patterns() -> List[Tuple[str, str]]:
    """
    Define regex patterns and replacements for all 87 Unicode characters from Originality.AI,
    plus AI-specific artifacts and a placeholder for additional patterns.
    Each tuple contains (pattern, replacement).
    """
    patterns = [
        # Visible Characters
        (r'\u00A0', ' '),  # No-Break Space → space
        (r'\u0009', '    '),  # Tab → 4 spaces
        (r'\u000C', ''),  # Form Feed → remove
        (r'\u001C', ''),  # File Separator → remove
        (r'\u000D', ''),  # Carriage Return → remove
        (r'\u2000', ' '),  # En Quad → space
        (r'\u2001', ' '),  # Em Quad → space
        (r'\u2002', ' '),  # En Space → space
        (r'\u2003', ' '),  # Em Space → space
        (r'\u2004', ' '),  # Three-Per-Em Space → space
        (r'\u2005', ' '),  # Four-Per-Em Space → space
        (r'\u2006', ' '),  # Six-Per-Em Space → space
        (r'\u2007', ' '),  # Figure Space → space
        (r'\u2008', ' '),  # Punctuation Space → space
        (r'\u2009', ' '),  # Thin Space → space
        (r'\u200A', ' '),  # Hair Space → space
        (r'\u202F', ' '),  # Narrow NBSP → space
        (r'\u205F', ' '),  # Math Space → space
        (r'\u3000', ' '),  # Ideographic Space → space
        (r'\u1680', ' '),  # Ogham Space Mark → space
        (r'\u2014', '-'),  # Em Dash → hyphen
        (r'\u2013', '-'),  # En Dash → hyphen
        (r'\u2019', "'"),  # Right Single Quote → '
        (r'\u201C', '"'),  # Left Double Quote → "
        (r'\u201D', '"'),  # Right Double Quote → "
        (r'\u2018', "'"),  # Left Single Quote → '
        (r'\u2026', '...'),  # Horizontal Ellipsis → ...
        (r'\u2800', ' '),  # Braille Blank → space
        (r'\u3164', ' '),  # Hangul Filler → space
        (r'\u115F', ''),  # Hangul Choseong Filler → remove
        (r'\u1160', ''),  # Hangul Jungseong Filler → remove
        (r'\u17B4', ''),  # Khmer Vowel Inherent AQ → remove
        (r'\u17B5', ''),  # Khmer Vowel Inherent AA → remove
        (r'\u180E', ' '),  # Mongolian Vowel Separator → space
        (r'\uFFA0', ' '),  # Half-width Hangul Filler → space
        (r'\uFFFC', '[OBJECT]'),  # Object Replacement → [OBJECT]

        # Invisible Characters
        (r'\u200B', ' '),  # Zero-Width Space → space
        (r'\u200C', ''),  # Zero-Width Non-Joiner → remove
        (r'\u200D', ''),  # Zero-Width Joiner → remove
        (r'\u200E', ''),  # Left-To-Right Mark → remove
        (r'\u200F', ''),  # Right-To-Left Mark → remove
        (r'\u202A', ''),  # LTR Embedding → remove
        (r'\u202B', ''),  # RTL Embedding → remove
        (r'\u202C', ''),  # Pop Directional Fmt → remove
        (r'\u202D', ''),  # LTR Override → remove
        (r'\u202E', ''),  # RTL Override → remove
        (r'\u2060', ''),  # Word Joiner → remove
        (r'\u2061', ''),  # Function Application → remove
        (r'\u2062', 'x'),  # Invisible Times → x
        (r'\u2063', ','),  # Invisible Separator → ,
        (r'\u2064', '+'),  # Invisible Plus → +
        (r'\u2066', ''),  # LTR Isolate → remove
        (r'\u2067', ''),  # RTL Isolate → remove
        (r'\u2068', ''),  # First Strong Isolate → remove
        (r'\u2069', ''),  # Pop Directional Isolate → remove
        (r'\u206A', ''),  # Inhibit Symmetric Swap → remove
        (r'\u206B', ''),  # Activate Symmetric Swap → remove
        (r'\u206C', ''),  # Inhibit Arabic Form Shaping → remove
        (r'\u206D', ''),  # Activate Arabic Form Shaping → remove
        (r'\u206E', ''),  # National Digit Shapes → remove
        (r'\u206F', ''),  # Nominal Digit Shapes → remove
        (r'\u2028', '\n'),  # Line Separator → \n
        (r'\u2029', '\n\n'),  # Paragraph Separator → \n\n
        (r'\u00AD', ''),  # Soft Hyphen → remove
        (r'\u034F', ''),  # Grapheme Joiner → remove
        (r'\u180B', ''),  # Mongolian VS-1 → remove
        (r'\u180C', ''),  # Mongolian VS-2 → remove
        (r'\u180D', ''),  # Mongolian VS-3 → remove
        (r'\uFE00', ''),  # Variation Selector-1 → remove
        (r'\uFE01', ''),  # Variation Selector-2 → remove
        (r'\uFE02', ''),  # Variation Selector-3 → remove
        (r'\uFE03', ''),  # Variation Selector-4 → remove
        (r'\uFE04', ''),  # Variation Selector-5 → remove
        (r'\uFE05', ''),  # Variation Selector-6 → remove
        (r'\uFE06', ''),  # Variation Selector-7 → remove
        (r'\uFE07', ''),  # Variation Selector-8 → remove
        (r'\uFE08', ''),  # Variation Selector-9 → remove
        (r'\uFE09', ''),  # Variation Selector-10 → remove
        (r'\uFE0A', ''),  # Variation Selector-11 → remove
        (r'\uFE0B', ''),  # Variation Selector-12 → remove
        (r'\uFE0C', ''),  # Variation Selector-13 → remove
        (r'\uFE0D', ''),  # Variation Selector-14 → remove
        (r'\uFE0E', ''),  # Variation Selector-15 → remove
        (r'\uFE0F', ''),  # Variation Selector-16 → remove
        (r'\uFEFF', ''),  # Zero-Width NBSP / BOM → remove

        # AI-Specific Artifacts
        (r'#{2,}', ''),  # Remove Markdown headers (##, ###, etc.)
        (r'\*\*+', ''),  # Remove excessive bold markers (**)
        (r'\[INST\]', ''),  # Remove instruction tags
        (r'\[SEP\]', ''),  # Remove separator tags
        (r'```+', ''),  # Remove code block markers

        # Placeholder for Additional Patterns
        # Add new Unicode characters or AI-specific patterns here
        # Example: (r'\uXXXX', ''),  # New Unicode character → replacement
        # Example: (r'some_pattern', ''),  # New AI artifact → remove
        (r'###+', ''),  # Remove three or more # symbols
        # (r'your_pattern_here', 'your_replacement_here'),
    ]
    return patterns

def clean_text(text: str) -> str:
    """
    Clean the input text by normalizing with ftfy and applying Unicode and AI artifact replacements.
    """
    try:
        # Check ftfy version
        try:
            ftfy_version = importlib.metadata.version("ftfy")
            logger.info(f"Using ftfy version: {ftfy_version}")
        except importlib.metadata.PackageNotFoundError:
            logger.warning("ftfy version not found, assuming compatible version")
            ftfy_version = "unknown"

        # Use minimal ftfy parameters
        ftfy_params = {
            'normalization': 'NFC',
            'fix_latin_ligatures': True,
            'remove_terminal_escapes': True,
            'fix_entities': True,
        }

        # Normalize text with ftfy
        cleaned = ftfy.fix_text(text, **ftfy_params)
        logger.info("ftfy normalization completed")

        # Apply all replacement patterns
        patterns = define_replacement_patterns()
        for pattern, replacement in patterns:
            cleaned = re.sub(pattern, replacement, cleaned)

        # Normalize non-standard spaces to regular spaces, preserving newlines
        # List of non-standard space characters (excluding U+0020)
        non_standard_spaces = (
            r'\u00A0|\u2000|\u2001|\u2002|\u2003|\u2004|\u2005|\u2006|'
            r'\u2007|\u2008|\u2009|\u200A|\u202F|\u205F|\u3000|\u1680|'
            r'\u180E|\uFFA0|\u200B|\u2800|\u3164'
        )
        cleaned = re.sub(non_standard_spaces, ' ', cleaned)

        # Preserve newlines and normalize multiple spaces (but not newlines)
        # Replace multiple spaces with a single space, excluding newlines
        cleaned = re.sub(r'[ \t]+', ' ', cleaned)

        # Normalize multiple newlines (3+ → 2)
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)

        # Remove trailing spaces from each line, preserving newlines
        cleaned = '\n'.join(line.rstrip() for line in cleaned.split('\n'))

        return cleaned
    except Exception as e:
        logger.error(f"Error cleaning text: {e}")
        return text  # Return original text on error

def process_file(input_file: str, output_file: str) -> None:
    """
    Read input file, clean its contents, and write to output file.
    """
    try:
        # Read input file
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        logger.info(f"Successfully read input file: {input_file}")

        # Clean the text
        cleaned_text = clean_text(text)
        logger.info("Text cleaning completed")

        # Write to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
        logger.info(f"Cleaned text written to: {output_file}")

    except FileNotFoundError:
        logger.error(f"Input file not found: {input_file}")
        sys.exit(1)
    except PermissionError:
        logger.error(f"Permission denied for file: {input_file} or {output_file}")
        sys.exit(1)
    except UnicodeDecodeError:
        logger.error(f"Invalid encoding in file: {input_file}. Ensure it's UTF-8.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

def main():
    """
    Parse command-line arguments and run the file cleaning process.
    """
    parser = argparse.ArgumentParser(
        description="Clean hidden Unicode characters and AI artifacts from a text file."
    )
    parser.add_argument(
        'input_file',
        type=str,
        help="Path to the input text file"
    )
    parser.add_argument(
        'output_file',
        type=str,
        help="Path to the output cleaned text file"
    )
    args = parser.parse_args()

    process_file(args.input_file, args.output_file)

if __name__ == "__main__":
    main()