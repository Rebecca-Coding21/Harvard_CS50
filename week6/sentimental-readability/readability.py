from cs50 import get_string

text = get_string("Text:")
letters = 0
words = 1
sentences = 0
n = len(text)

text = text.lower()

for c in text:

    # count letters

    if (64 < ord(c) < 91) or (96 < ord(c) < 123):
        letters = letters + 1

    # count words

    elif c == " ":
        words = words + 1

    # count sentences

    elif c == "." or c == "!" or c == "?":
        sentences = sentences + 1

# calculate index

L = (letters / words) * 100
S = (sentences / words) * 100
index = 0.0588 * L - 0.296 * S - 15.8

grade = round(index)

# print(grade)
if grade < 1:
    print("Before Grade 1")
elif grade >= 16:
    print("Grade 16+")
else:
    print(f"Grade {grade}")

