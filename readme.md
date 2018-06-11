# Terminology Extractor

This simple extractor selects terms from translation memory exchange files (`.tmx`) based on the [TF\*IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) weighting method.

## Running the system

First use the command:

`python3 src/get_strings.py <file_name>`

from the home directory. This command will output a file with the extracted string from your TMX to the `txt/` folder.

*This system is built to extract terms from TMX files, downloaded from Mozilla's [Transvision](https://transvision.mozfr.org/downloads/) website. This system is not guaranteed to read all TMX files.*

Then, use the command:

`python3 src/score_terms.py txt/<file_name>`

from the home directory. This command will output a file with the highest-scoring terms and their scores in the `results/` folder. 

*System default is the top 10% of all terms. To change this, you must edit the `keep` variable in `score_terms.py`.*

## Dependencies

System requires Python 3 and the `NLTK` package.

## About the system

### TF\*IDF

TF\*IDF is a weighting schema for terms in a document set. It's purpose is to find topic words by selecting words that are clustered in a document set. 

TF is the term's frequency, similar to a term count. 

IDF is the inverse document frequency, meaning the inverse of number of documents in which the term is present. IDF weighting increases the weight of a term that appears in fewer documents.

Terms that appear many times and in few documents recieve the highest scores. This system assumes that words that follow that pattern are likely topic words.

### Term Definition

A term is a reference to an idea. A term may be an entity, a characteristic, a description, or any other kind of reference to an idea. 

Terms may be any kind of word or part of speech, and may also consist of several sequential words. 

This system does not currently support compound-word terms. 