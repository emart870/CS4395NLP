from turtle import clear
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from nltk import sent_tokenize
import urllib
from urllib import request
from bs4 import BeautifulSoup
import pickle

#Functions
def webCrawler(url):
    soup = BeautifulSoup(request.urlopen(url).read().decode('utf8'), features="html.parser")
    links = [link for link in soup.find_all('a') if link.get('href') is not None]
    #Hardcoding for the Bible Wikipedia Page
    links = links[4:6] + links[13:24] + links[27:29]
    return links

def writingLinksFile(links):
    f = open("linksFile.txt", "w")
    for i in range(len(links)-1):
        f.write(links[i])
        f.write("\n")
    f.write(links[-1])
    f.close()

def preProcessText(text):
    text = [t for t in text if t.isascii()]
    return ''.join(text)


def webScraping(links):
    for i in range(len(links)):
        f = open("file" + str(i+1) + ".txt", "w")
        url = "https://en.wikipedia.org"+links[i].get('href')
        soup = BeautifulSoup(request.urlopen(url).read().decode('utf8'), features="html.parser")
        for p in soup.select('p'):
            text = preProcessText(p.get_text())
            f.write(str(re.sub("\[.*\]", "", text)))
        f.close()

def sentencesFromFile(fileNum):
    fileToRead = open("file" + str(fileNum) + ".txt", "r")
    fileToWrite = open("file" + str(fileNum) + "sentences.txt", "w")
    for paragraph in fileToRead:
        sentences = sent_tokenize(paragraph)
        for sentence in sentences:
           fileToWrite.write(sentence + "\n")
    fileToWrite.close()
    fileToRead.close()

def filesToString():
    #Storing all the files into one big string
    output = ""
    for i in range(15):
        f = open("file" + str(i+1) + "sentences.txt", "r")
        output += f.read()
        output += " "
        f.close()
    
    #Preprocessing the string by making everything lowercase and by removing newlines, tabs, punctuation, and stopwards
    output.lower()
    output.replace("\n", " ")
    output.replace("\t", " ")
    output = "".join([t for t in output if t.isalpha() or t==" "])
    stopwordList = stopwords.words('english')
    tokens = output.split(" ")
    tokens = [t.lower() for t in tokens if not t.lower() in stopwordList]
    output = " ".join(tokens)
    
    return output

def getImportantWords():
    text = filesToString()
    wordCount = {word:text.count(word + " ") for word in set(text.split(" "))}
    wordCount = sorted(wordCount.items(), key=lambda item: item[1], reverse=True)
    return wordCount

def generateKnowledgeBase(importantWordArr):
    importantWordDictionary = {}
    for word in importantWordArr:
        sentencesContainingWord = ""
        for i in range(15):
            f = open("file" + str(i+1) + "sentences.txt", "r")
            for line in f:
                if word in line.lower():
                    sentencesContainingWord += line
            f.close()
        importantWordDictionary[word] = sentencesContainingWord
    return importantWordDictionary

if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Bible"
    links = webCrawler(url)
    webScraping(links)
    for i in range(len(links)):
        sentencesFromFile(i+1)
    importantWordList = ["books", "testament", "new", "bible", "canon",
                         "canonical", "church", "hebrew", "christian", "apocrypha"]
    importantWordDictionary = generateKnowledgeBase(importantWordList)
    pickle.dump(importantWordDictionary, open('knowledgeBase.p', 'wb'))