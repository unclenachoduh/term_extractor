from nltk.tokenize import word_tokenize
from nltk import ngrams

def get_grams(line):

    list_of_grams = []

    words = word_tokenize(line)

    if words[-1] == '.':
        words = words[:-1]

    gram_count = 0

    while gram_count < len(words):
        gram_count += 1
        temp = ngrams(words, gram_count)
        list_of_grams.append(temp)

    return list_of_grams