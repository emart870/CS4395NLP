# Import Statements
import math
import nltk
nltk.download("all")
from nltk.util import ngrams
from nltk.book import *
from nltk.corpus import wordnet as wn
from nltk.wsd import lesk
from nltk.corpus import sentiwordnet as swn
import pickle
from nltk.tokenize import word_tokenize

#Function that reads in a file, creates a unigram and a bigram list, and returns a count dictionary of each
def program1(filename):
  #Reading in file and removing newlines
  f = open(filename, "r")
  text = f.read().replace('\n', ' ')
  f.close()

  #Tokenizing the text and making a list of unigrams and a list of bigrams
  unigrams = word_tokenize(text)
  bigrams = list(ngrams(unigrams, 2))

  #Making a dictionary of unigrams and counts and of bigrams and counts
  unigramCounts = {t:unigrams.count(t) for t in set(unigrams)}
  bigramCounts = {b:bigrams.count(b) for b in set(bigrams)}

  #Returing the unigram and bigram dictionaries
  return (unigramCounts, bigramCounts)



def compute_prob(text, unigram_dict, bigram_dict, N, V):
    # N is the number of tokens in the training data
    # V is the vocabulary size in the training data (unique tokens)
    unigrams_test = word_tokenize(text)
    bigrams_test = list(ngrams(unigrams_test, 2))
    p_laplace = 1
    for bigram in bigrams_test:
        n = bigram_dict[bigram] if bigram in bigram_dict else 0
        d = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0
        p_laplace = p_laplace * ((n + 1) / (d + V))
    return p_laplace

def program2():
  #Reading in the pickled dictionaries
  with open('unigramCountEnglish', 'rb') as handle:
      unigramCountEnglish = pickle.load(handle)
  with open('bigramCountEnglish', 'rb') as handle:
      bigramCountEnglish = pickle.load(handle)

  with open('unigramCountFrench', 'rb') as handle:
      unigramCountFrench = pickle.load(handle)
  with open('bigramCountFrench', 'rb') as handle:
      bigramCountFrench = pickle.load(handle)

  with open('unigramCountItalian', 'rb') as handle:
      unigramCountItalian = pickle.load(handle)
  with open('bigramCountItalian', 'rb') as handle:
      bigramCountItalian = pickle.load(handle)

  #Reading in the test file
  f = open("LangId.test", "r")
  testLines = f.readlines()
  f.close()

  #Preprocessing the test file, i.e., removing the new-line characters
  for i in range(len(testLines)):
    testLines[i] = testLines[i].replace("\n", "")

  #Finding the number of total tokens in each language
  nEnglish = sum(unigramCountEnglish.values())
  nFrench = sum(unigramCountFrench.values())
  nItalian = sum(unigramCountItalian.values())

  #Finding the number of unique tokens in each language
  vEnglish = len(unigramCountEnglish)
  vFrench = len(unigramCountFrench)
  vItalian = len(unigramCountItalian)

  #Calculting the prob for each testline and writing our guess into the "LangId.guess" file
  f = open("LangId.guess", "w")
  lineCount = 1
  for testLine in testLines:
    pEnglish = compute_prob(testLine, unigramCountEnglish, bigramCountEnglish, nEnglish, vEnglish)
    pFrench = compute_prob(testLine, unigramCountFrench, bigramCountFrench, nFrench, vFrench)
    pItalian = compute_prob(testLine, unigramCountItalian, bigramCountItalian, nItalian, vItalian)

    if pEnglish == max(pEnglish, pFrench, pItalian):
      f.write(str(lineCount) + " English\n")
    elif pFrench == max(pFrench, pItalian):
      f.write(str(lineCount) + " French\n")
    else:
      f.write(str(lineCount) + " Italian\n")
    lineCount += 1
  f.close()

  # Reading in and preprocessing our guess file and the true solution file
  f = open("LangId.guess", "r")
  guessList = f.readlines()
  f.close()
  for i in range(len(guessList)):
    guessList[i] = guessList[i].replace("\n", "")

  f = open("LangId.sol", "r")
  solList = f.readlines()
  f.close()
  for i in range(len(solList)):
    solList[i] = solList[i].replace("\n", "")

  #Comparing our guess to the true solution
  total = len(guessList)
  correctGuessAmount = 0
  for i in range(total):
    if guessList[i] == solList[i]:
      correctGuessAmount += 1
    else:
      guessSpaceIndex = guessList[i].index(" ")
      solSpaceIndex = solList[i].index(" ")
      guessLang = guessList[i][guessSpaceIndex+1:]
      solLang = solList[i][solSpaceIndex+1:]
      print("On line " + str(i) + ", there was a mis-match. We guessed \'" + guessLang + "\' but the solution was \'" + solLang + "\'")

  #Accuracy of our guesses
  print("Accuracy: " + str(correctGuessAmount/total))

#Main Body of Code
if __name__ == "__main__":
  #Pickling the dictionaries
  (unigramCountEnglish, bigramCountEnglish) = program1("LangId.train.English")
  with open('unigramCountEnglish', 'wb') as handle:
      pickle.dump(unigramCountEnglish, handle)
  with open('bigramCountEnglish', 'wb') as handle:
      pickle.dump(bigramCountEnglish, handle)

  (unigramCountFrench, bigramCountFrench) = program1("LangId.train.French")
  with open('unigramCountFrench', 'wb') as handle:
      pickle.dump(unigramCountFrench, handle)
  with open('bigramCountFrench', 'wb') as handle:
      pickle.dump(bigramCountFrench, handle)

  (unigramCountItalian, bigramCountItalian) = program1("LangId.train.Italian")
  with open('unigramCountItalian', 'wb') as handle:
      pickle.dump(unigramCountItalian, handle)
  with open('bigramCountItalian', 'wb') as handle:
      pickle.dump(bigramCountItalian, handle)
  program2()