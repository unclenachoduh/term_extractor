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

#### Todo
# Try stemming words to unify word counts

#### Todo
# Coreference resolution to ensure consistency

import sys, os, math
import re
from nltk.tokenize import word_tokenize
from operator import itemgetter
import ngrams
# from stemming.porter2 import stem
# stem(w)

def getStopWords():
	stop_file = open("src/stop_words.txt").read().split("\n")

	stop_words = {}

	stop_line = ""

	for stop in stop_file:

		stop_token = word_tokenize(stop)

		for token in stop_token:
			if token not in stop_words:
				stop_words[token] = 0

	return stop_words

def uniqueID(docNames):
	uniqueDocs = []

	for doc in docNames:
		if doc not in uniqueDocs:
			uniqueDocs.append(doc)

	return len(uniqueDocs)

def termGetter(foldername, output):
	stop_words = getStopWords()

	# ------------------
	# My terminology stuff should go here

	terms_d = {} # key = term , value = [tally , [docID]] # len of uniqueID([docID]) = doc freq

	terms = [] # list of all terms

	document_length = 0 # this should be per document

	for file in os.listdir(foldername):
		filepath = os.path.join(foldername, file)
	
		# print(file)

		text = open(filepath).read().lower().split("\n")

		# print(text)
		for line in text:
			if line != "":

				tokens = ngrams.get_grams(line)

				words = []
				for x in tokens:
					for e in x:
						# print(e)
						check = False # make sure words count

						not_garbage = 0
						garbage = 0
						for t in e:
							if t not in stop_words and re.search("[a-zA-Z]", t):
								check = True
								not_garbage += 1
							else:
								garbage += 1

						if not_garbage - 1 > garbage:
							words.append("_".join(e))
							# print("_".join(e))

				unq = []
				for w in words:

					document_length += 1

					if w in terms_d:
						tmp = terms_d[w]
						tmp[0] += 1
						tmp[1].append(file)
						terms_d[w] = tmp
					else:
						terms_d[w] = [1, [file]]
						terms.append(w)

					if w not in unq:
						unq.append(w)

				# for u in unq:
				# 	tmp = terms_d[u]
				# 	tmp[1] += 1
				# 	terms_d[u] = tmp

		# # TODO
		# # firefox_for
		# # firefox_for_android
		# # eliminate these dumb repetitions


		# term_vals = []

		# for t in terms:
		# 	tcount = terms_d[t][0]
		# 	dcount = terms_d[t][1]

		# 	tf = tcount / document_length
		# 	idf = len(text) / (1+ math.log10(dcount))
		# 	tfidf = tf * idf
		# 	# print("Term data:", len(terms), t, tcount, dcount, tf, idf, tfidf)

		# 	term_vals.append([t, tfidf])

	wout = open(output, "w+")

	scores = []

	outCount = 0
	for t in terms:
		outTmp = terms_d[t]

		docFreq = uniqueID(outTmp[1])

		tf = outTmp[0] / document_length
		idf = len(os.listdir(foldername)) / (1+ math.log10(docFreq))
		tfidf = tf * idf

		# wout.write(t + "\t" + str(outTmp[0]) + "\t" + str(docFreq) + "\n")

		scores.append([t, tfidf])

	scores = sorted(scores, key=itemgetter(1), reverse=True)

	for x in scores:
		# if terms_d[x[0]][0] > min_count:
		# 	graph.write(x[0] + "\t" + str(x[1]) + "\n")
		# else:
		# 	break

		wout.write(x[0] + "\t" + str(x[1]) + "\n")






	# #### Todo
	# # Find a good way to manage the number of terms kept
	# keep = int(len(terms) * 1 /10) # collect 10% of terms
	# # keep = int(len(terms) * 3 /10) # collect 30% of terms
	# # keep = len(terms) # collect all terms
	# ####

	# count = 1

	# term_vals = sorted(term_vals, key=itemgetter(1), reverse=True)
	# # for x in term_vals:
	# # 	count += 1
	# # 	if count < keep:
	# # 		graph.write(x[0] + "\t" + str(x[1]) + "\n")
	# # 	else:
	# # 		break

	# min_count = 6


if __name__ == '__main__':
	# input = sys.argv[1]
	# if out[-1] != "/":
	# 	out += "/"
	termGetter(sys.argv[1], sys.argv[2])