from more_itertools import peekable
from os import listdir
from os.path import isfile, join
import tokenize
from random import randrange

pronouns = {
    "m": {"genitive": "his", "nominative": "he", "accusative": "him"},
    "f": {"genitive": "her", "nominative": "she", "accusative": "her"},
    "n": {"genitive": "their", "nominative": "they", "accusative": "them"}
}

inv_pronouns = {v: k for defn in pronouns.values() for k, v in defn.items()}

to_replace = {"ascendant": "$ascendant", "god": "ascendant", "realm": "warren", "divine": ""}

to_replace.update(inv_pronouns)

onlyfiles = [q for f in listdir("./base_text/") if isfile((q := join("./base_text/", f)))]

class TransitionKey:
    def __init__(self):
        self.map = {}
        self.total = 0
    
    def add(self, word):
        self.total += 1
        if word in self.map:
            self.map[word] += 1
        else:
            self.map[word] = 1
    
    def __repr__(self):
        return str({k: v/self.total for k, v in self.map.items()})

prob_map = {"\n": TransitionKey()}

def gen_iterator(line):
    iterator = peekable(line.split())
    while True:
        try:
            token = next(iterator)
        except StopIteration:
            break
        
        while len(token) > 1 and token[-1:] in {",", ".", "!", "'", "\""}:
            iterator.prepend(token[-1:])
            token = token[:-1]
        
        while len(token) > 2 and token.endswith("'s"):
            iterator.prepend(token[-2:])
            token = token[:-2]
        
        yield token

for filename in onlyfiles:
    first = True

    for line in open(filename, "r"):
        iterator = peekable(iter(gen_iterator(line)))
        if first:
            iterator.prepend("$begin")
            first = False
        else:
            iterator.prepend("\n")
            
        while True:
            try:
                val = next(iterator).lower()
                peek = iterator.peek().lower()
            
            except StopIteration:
                break

            if peek in to_replace:
                next(iterator)
                iterator.prepend(to_replace[peek])
                peek = to_replace[peek]
            
            if val not in prob_map:
                prob_map[val] = TransitionKey()
            
            prob_map[val].add(peek)
        
        prob_map[val].add("\n")
        
    prob_map[val].add("$end")


text = ""

def gen_words(name):
    word = "$ascendant"
    gender = ("m", "f", "n")[randrange(3)]
    pronoun_dict = pronouns[gender]
    
    while True:
        if word == "$end":
            yield word
            break

        elif word == "$ascendant":
            yield name

        elif word in pronouns[gender]:
            yield pronoun_dict[word]

        else:
            yield word

        trans = prob_map[word]
        randnum = randrange(trans.total)

        for word, prominence in trans.map.items():
            randnum -= prominence
            if randnum < 0:
                break

def gen_text(name):
    name = name[0].upper() + name[1:]
    iterator = peekable(iter(gen_words(name)))

    text = ""

    while True:
        try:
            val = next(iterator)
            peek = iterator.peek()
        except StopIteration:
            break
        
        if val in {".", "\n", "$begin"}:
            next(iterator)
            iterator.prepend(peek[0].upper() + peek[1:])
            if val == "$begin":
                continue
        
        if peek not in {",", ".", "!", "'", "\"", "'s"}:
            val = val + " "
        
        text += val
    
    return text

if __name__ == "__main__":
    print(gen_text("steve"))