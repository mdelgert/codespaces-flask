import ftfy

text = "This is some text with hidden characters: \u200b\u200c\u200d"
clean_text = ftfy.fix_text(text)
print(clean_text)
