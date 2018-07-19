# Terminology Extractor

This simple extractor selects terms from translation memory exchange files (`.tmx`) based on the [TF\*IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) weighting method.

*This system is built to extract terms from TMX files, downloaded from Mozilla's [Transvision](https://transvision.mozfr.org/downloads/) website. This system is not guaranteed to read all TMX files.*

## Running the system

First use the command:

`python3 src/get_strings.py <tmx_folder> <output_folder>`

from the home directory. `<tmx_folder>` is a folder with at least one TMX file and `<output_folder>` is a directory when the output files will be written. This command will output one file per source doc with the extracted strings from your TMX to the given output folder. 

*Source docs are found in the tuid and reference the source where the string originates from.*

Then, use the command:

`python3 src/score_terms.py <folder> <output>`

from the home directory. This command will output a file with the 100 highest-scoring terms and their scores.

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

This system treats individual words and all sequences of words from a source file as a term. Any term that scores in the top 100 is included in the output. 