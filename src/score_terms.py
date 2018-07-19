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

import statistics
from statistics import mean

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

# def termGetter(foldername, output, mult):
def termGetter(foldername, output):
	stop_words = getStopWords()

	terms_d = {} # key = term , value = [tally , [docID]] # len of uniqueID([docID]) = doc freq

	terms = [] # list of all terms

	document_length = 0 # this should be per document

	for file in os.listdir(foldername):
		filepath = os.path.join(foldername, file)

		text = open(filepath).read().lower().split("\n")

		for line in text:
			if line != "":

				tokens = ngrams.get_grams(line)

				words = []
				for x in tokens:
					for e in x:
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
							words.append(" ".join(e))

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

	# wout = open("results/testing_output", "w+") # File that shows tf, df, and tfidf

	scores = []

	# stats = []

	outCount = 0
	for t in terms:
		outTmp = terms_d[t]

		tf = outTmp[0] / document_length
		df = uniqueID(outTmp[1])
		idf = len(os.listdir(foldername)) / (1+ math.log10(df))
		# tfidf = tf * idf
		tfdf = tf * df
		tfdfidf = tfdf * idf

		# stats.append(tfidf)

		# wout.write(t + "\t" + str(outTmp[0]) + "\t" + str(docFreq) + "\t" + str(tfidf) + "\n")

		# scores.append([t, tfidf])
		scores.append([t, tfdfidf])

	scores = sorted(scores, key=itemgetter(1), reverse=True)


# Need a good way to choose how many terms to return
	# sd = statistics.stdev(stats)
	# maximum = max(stats)
	# avg = statistics.mean(stats)
	# limit = float(mult)
	# margin = avg+(limit*sd)
	# margin = (float(sys.argv[3]) / 100) * len(scores)
	margin = 100
	# print("MAX: ", maximum)
	# print("SD:  ", sd)
	# print("AVG: ", avg)
	# print("MRG: ", margin)

	wout = open(output, "w+")
	count = 0
	for x in scores:

		score = x[1]
		# if loss > prevLoss*.9 or count < 10:
		# while score > margin:
		if count < margin:
			wout.write(x[0] + "\t" + str(score) + "\n")
			count += 1
		else:
			# print("STOP:", x[0], str(score))
			break

if __name__ == '__main__':
	# termGetter(sys.argv[1], sys.argv[2], sys.argv[3])
	termGetter(sys.argv[1], sys.argv[2])