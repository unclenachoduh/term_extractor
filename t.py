from nltk.tokenize import word_tokenize, TweetTokenizer

text1 = "He had Jeremy's cake.\nHe wanted to play games, but he couldn't.\nShe said, \"We\'ll try again later."

text2 = "we'll\ncouldn't\na's"

tkn = TweetTokenizer()

text1 = text1.lower()

text1_lines = text1.split("\n")

for line in text1_lines:
	print(tkn.tokenize(line))

print(tkn.tokenize(text2))