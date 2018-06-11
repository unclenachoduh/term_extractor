####
# Script extracts raw text from .TMX files from https://transvision.mozfr.org/downloads/
# To run, use command, `python3 get_strings.py <file_name>`
# Will write a file called `filename_sents.txt` to run directory
####
import sys
import re

filename = sys.argv[1]

# print(filename)

text = open(filename).read().split("\n")

sents = []

cur = ""
prev = ""

for line in text:

	cur = re.sub("\s\s*", " ", line)
	cur = re.sub("^ ", "", cur)

	if re.search("\<tuv xml:lang=\"en-US\"\>", cur):
		# print(cur)

		parts = re.split("(<seg>|</seg>)", cur)

		# print(parts[2])

		if cur != prev:
			sents.append(parts[2])
			# print("^added")

	prev = cur

loc = filename.split("/")

stem = loc[-1].split(".")

wout = open("txt/" + stem[0] + "_sents.txt", "w+")

for line in sents:
	wout.write(line + "\n")