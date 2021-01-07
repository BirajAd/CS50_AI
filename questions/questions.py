import nltk
import sys
import os
import string
import numpy as np
from collections import Counter
import itertools

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)

def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    dictionary = dict()
    for docs in os.listdir(directory):
        with open(os.path.join(directory,docs)) as f:
            text = f.read()
            dictionary[docs] = text
    return dictionary

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = nltk.word_tokenize(document)
    final = []
    for word in words:
        if(word in nltk.corpus.stopwords.words('english')):
            continue
        if(word in string.punctuation):
            continue
        final.append(word)
    return [word.lower() for word in final]

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    #{'a': ['hello', 'hi'], 'b': ['hello', 'are', 'you']}
    all_words = []
    ans = {}
    for doc in documents:
        all_words.extend(documents[doc])
    
    for word in all_words:
        appearance = 0
        for doc in documents:
            if word in documents[doc]:
                appearance += 1
        ans[word] = np.log(len(documents)/appearance) #idf = ln(number_of_docs/in how many documents the word appeared in)
        # print(word, " -> ", appearance)
    return ans



def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfidfDictionary = dict()
    question =  query
    for f in files:
        totalIfDf = 0
        allCount = Counter(files[f]) #count of words(tf) of words within the file
        for word in question:
            if word in files[f]:
                tf = allCount[word] #term frequency of the word
                idf = idfs[word] #inverse document frequency of the word
                totalIfDf += (tf*idf)
        tfidfDictionary[f] = totalIfDf

    tfidfDictionary = dict(sorted(tfidfDictionary.items(), key=lambda item: item[1], reverse=True))
    return dict(itertools.islice(tfidfDictionary.items(), n))

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    question =  query
    tdDictionary = dict()
    for s in sentences:
        idf = 0
        td = 0
        for word in question:
            allCount = Counter(sentences[s])
            if word in sentences[s]:
                idf += idfs[word]
                td += allCount[word]/len(sentences[s])
        tdDictionary[s] = [idf, td]
    tdDictionary = sorted(tdDictionary, key=lambda x: (-tdDictionary[x][0], -tdDictionary[x][1])) #sort by idf and in tie sort by td
    return tdDictionary[:n]



if __name__ == "__main__":
    main()
