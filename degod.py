import sys
import tokenize

files = sys.argv[1:]

for filename in files:
    with open(filename, "r") as f:
        for line in f:
            for token in tokenize.generate_tokens(lambda: line):
                string = token[1]
                if string[0].isupper():
                    string = "$ASCENDANT"
