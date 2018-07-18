####
# Script extracts raw text from .TMX files from https://transvision.mozfr.org/downloads/
# To run, use command, `python3 get_strings.py <source_folder_name> <output_folder_name>`
# Will write files called `filename_sents.txt` for each file to output directory
####
import sys, os
import re

def get_text(folderLocation):
	fileNames = []
	fileContents = []
	for file in os.listdir(folderLocation):
		filepath = os.path.join(folderLocation, file)

	# get just the lang code from the file name
		filename = file.split(".")
		code = filename[0]

		loc = code.split("/")

		fileNames.append(loc[-1])

	# read text from file
		openfile = open(filepath, 'r')
		texts = openfile.read().split("\n")
		openfile.close()

		sents = []

		cur = ""
		prev = ""

		for line in texts:

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
					sents.append(parts[2])

			prev = cur

		fileContents.append(sents)

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

		for line in mystuff[1][count]:
			wout.write(line + "\n")

		count += 1