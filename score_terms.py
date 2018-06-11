####
# Script finds TF*IDF scores for terms in a text file with format
# one doc per line.
# To run, use command, `python3 score_terms.py <file_name>`
# Will write a file called `plot` to run directory with <term, score>
####

#### Todo
# I can preprocess to find multi-word entities and merge them 
# with the symbol "_" or some other method to ensure they are 
# processed as terms, rather than words. It is unknown if there
# is a need to process additinal word types (POS).

#### Todo
# Common N-grams may be more comprehensive for collecting compound
# terms. Start with separate TF*IDF scores for N-grams. Then, try 
# evaluating all N-grams into the same list

#### Todo
# Add common HTML and other code snippets that get into output
# to stop words list

import sys
import re
from nltk.tokenize import word_tokenize
import math
from operator import itemgetter
# from stemming.porter2 import stem
# stem(w)

filename = sys.argv[1]

# print(filename)

stop_file = open("stop_words.txt").read().split("\n")

stop_words = []

stop_line = ""

for stop in stop_file:

	stop_token = word_tokenize(stop)

	for token in stop_token:
		if token not in stop_words:
			stop_words.append(token)

text = open(filename).read().split("\n")

terms_d = {} # key = term , value = [tally , doc count]
terms = [] # list of all terms

for line in text:
	line = re.sub("\’", "\'", line)
	line = line.lower()

	if line != "":
		words = word_tokenize(line)

		unq = []
		for w in words:
			if w in terms_d:
				tmp = terms_d[w]
				tmp[0] += 1
				terms_d[w] = tmp
			else:
				terms_d[w] = [1, 0]
				terms.append(w)

			if w not in unq:
				unq.append(w)

		for u in unq:
			tmp = terms_d[u]
			tmp[1] += 1
			terms_d[u] = tmp


term_vals = []

for t in terms:
	if t not in stop_words and re.search("[a-zA-Z]", t):

		if t == "ll":
			print("PROBLEM", t)
		tcount = terms_d[t][0]
		dcount = terms_d[t][1]

		tf = tcount / len(terms)
		idf = len(text) / (1+ math.log10(dcount))
		tfidf = tf * idf
		# print("Term data:", len(terms), t, tcount, dcount, tf, idf, tfidf)

		term_vals.append([t, tfidf])

graph = open("plot", "w+")

#### Todo
# Find a good way to manage the number of terms kept
keep = int(len(terms) * 1 /10) # collect 10% of terms
# keep = int(len(terms) * 3 /10) # collect 30% of terms
# keep = len(terms) # collect all terms
####

count = 1

term_vals = sorted(term_vals, key=itemgetter(1), reverse=True)
for x in term_vals:
	count += 1
	if count < keep:
		graph.write(x[0] + "\t" + str(x[1]) + "\n")
	else:
		break
