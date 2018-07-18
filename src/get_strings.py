####
# Script extracts raw text from .TMX files from https://transvision.mozfr.org/downloads/
# To run, use command, `python3 get_strings.py <source_folder_name> <output_folder_name>`
# Will write files called `filename_sents.txt` for each file to output directory
####
import sys, os
import re

def get_text(folderLocation):
	nameInd = {} # dict for getting name index in fileNames
	fileNames = [] # list of filenames from tmx tuid. Filenames = docs
	fileContents = [] # list of contents for the correlating doc
	lineCounts = [] #list of counts of the number of items per doc
	for file in os.listdir(folderLocation):
		filepath = os.path.join(folderLocation, file)

		# fileNames.append()

	# read text from file
		openfile = open(filepath, 'r')
		text = openfile.read()
		openfile.close()

		text = re.sub(">\s*<seg>", "><seg>", text)

		texts = text.split("\n")
		cur = ""
		prev = ""

		docName = "XXX"
		docInd = -1

		for line in texts:

			if re.search("<tu tuid=", line):
				lineChunks = line.split("\"")
				docChunks = lineChunks[1].split(":")
				docName = docChunks[0]
				docName = re.sub("(/|-|\.)", "_", docName)

				if docName in nameInd:
					docInd = nameInd[docName]
				else:
					docInd = len(fileNames)
					fileNames.append(docName)
					nameInd[docName] = docInd

					fileContents.append("")

					lineCounts.append(0)

			else:
				cur = re.sub("\s\s*", " ", line)
				cur = re.sub("^ ", "", cur)
				cur = re.sub("&lt;", "<", cur)
				cur = re.sub("&gt;", ">", cur)
				# |&lt;/a&gt;|&lt;strong&gt;|&lt;/strong&gt;&lt;span&gt;|&lt;/span&gt;|&lt;|&gt;|")
				cur = re.sub("&amp;", "and", cur)

				if re.search("\<tuv xml:lang=\"en-US\"\>", cur):

					parts = re.split("(<seg>|</seg>)", cur)

					parts[2] = re.sub("<(.*?)>", "", parts[2])

					if cur != prev:
						fileContents[docInd] += parts[2] + "\n"

						lineCounts[docInd] += 1

				prev = cur

	return [fileNames, fileContents]


if __name__ == '__main__':
	folderLocation = sys.argv[1]
	outbound_location = sys.argv[2]

	if folderLocation[-1] != "/":
		folderLocation += "/"

	if outbound_location[-1] != "/":
		outbound_location += "/"

	if not os.path.exists(outbound_location):
		os.makedirs(outbound_location)
	
	mystuff = get_text(folderLocation)

	count = 0
	for x in mystuff[0]:

		wout = open(outbound_location + x + "_sents.txt", "w+")

		wout.write(mystuff[1][count])

		count += 1