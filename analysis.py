import json
import operator
import collections
import pdb
import nltk
import random
import string
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
nltk.download('all');

from nltk.corpus import stopwords, words, product_reviews_2, brown, wordnet


total = 0
wcount = 0
wcount2 = 0
wcount3 = 0
wcount4 = 0
wcount5 = 0
wcount6 = 0

sno = nltk.stem.SnowballStemmer('english')
ps = nltk.stem.PorterStemmer()
stopWords = set(stopwords.words('english')+ list(string.punctuation))
wordlist = set(i.lower() for i in words.words())
prodworldlist = set(i.lower() for i in product_reviews_2.words())
brownwordlist = set(i.lower() for i in brown.words())
wordnetlist = set(i.lower() for i in wordnet.words())



def countProduct(productCount, productId):
    if productId not in productCount:
        productCount[data['asin']] = 1
    else:
        productCount[data['asin']] += 1

    return productCount

def countReview(reviewCount, reviewerId):
    if reviewerId not in reviewCount:
        reviewCount[data['reviewerID']] = 1
    else:
        reviewCount[data['reviewerID']] += 1

    return reviewCount

# Get top 10 products and reviewers
def getTop(dict, val):
    topTen = {}
    for x in xrange(0, val):
        currTop = max(dict, key=lambda key: dict[key])
        topTen[currTop] = dict[currTop]
        del dict[currTop]

    return topTen

# Sort dictionary by value
def sortByValue(dict):
    sortedlist = sorted(dict.items(), key=operator.itemgetter(1))
    sortedlist.reverse()

    return sortedlist

# Sort dictionary by key
def sortByKey(dict):
    od = collections.OrderedDict(sorted(dict.items()))
    return od

# Count the number of sentences in each review
def countSentence(text, sentCount):
    sentences = nltk.sent_tokenize(text)
    if len(sentences) not in sentCount:
        sentCount[len(sentences)] = 1
    else:
        sentCount[len(sentences)] += 1

    return sentCount

# Count the number of tokens in each review
def countWordsLength(tokens, tokenCountLength, tokenCountLengthStem):

    if len(tokens) not in tokenCountLength:
        tokenCountLength[len(tokens)] = 1
    else:
        tokenCountLength[len(tokens)] += 1
    stemmedtokens = [sno.stem(t) for t in tokens]
    if len(stemmedtokens) not in tokenCountLengthStem:
        tokenCountLengthStem[len(stemmedtokens)] = 1
    else:
        tokenCountLengthStem[len(stemmedtokens)] += 1

    return tokenCountLength, tokenCountLengthStem

# Count how often a word appears throughout the entire dataset
def countWordsFreq(tokens, tokenFreq, tokenFreqStem):
    for token in tokens:
        if token not in tokenFreq:
            tokenFreq[token] = 1
        else:
            tokenFreq[token] += 1

        stemmedToken = sno.stem(token)
        if stemmedToken not in tokenFreqStem:
            tokenFreqStem[stemmedToken] = 1
        else:
            tokenFreqStem[stemmedToken] += 1

    return tokenFreq, tokenFreqStem

def tokenize(text, removeStop = False):
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    if removeStop:
        tokens = [t for t in tokens if t not in stopWords]

    return tokens

def segBeforeTokenize(text, removeStop = False):
    tokens = []
    # text = text.lower()
    sentences = nltk.sent_tokenize(text)
    for s in sentences:
        tokens += nltk.word_tokenize(s)
    if removeStop:
        tokens = [t for t in tokens if t not in stopWords]

    return tokens

def tagPOS(text):
    tokens = segBeforeTokenize(text)
    return nltk.pos_tag(tokens)

def plotGraph(od, ylabel, xlabel, title, filename):
    pdb.set_trace()
    keys = od.keys()
    values = od.values()
    y_pos = np.arange(len(keys))
    fig = plt.figure()
    plt.plot(keys, values)
    fig.suptitle(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    dir = filename + '.png'
    fig.savefig(dir)

def getAcc(text):
    words = segBeforeTokenize(text)
    global total, wcount, wcount2, wcount3, wcount4
    total += len(words)
    for word in words:
        if word in wordlist:
            wcount += 1
        if word in prodworldlist:
            wcount2 += 1
        if word in brownwordlist:
            wcount3 += 1
        if word in wordnetlist:
            wcount4 += 1

def getAcc2(text):
    words = segBeforeTokenize(text)
    global wcount5, wcount6
    for word in words:
        w1 = ps.stem(word)
        w2 = sno.stem(word)
        if w1 in brownwordlist:
            wcount5 += 1
        if w2 in brownwordlist:
            wcount6 += 1
with open("CellPhoneReview.json") as datafile:
    productCount = {}
    reviewCount = {}
    sentCount = {}
    tokenCountLength = {}
    tokenCountLengthStem = {}
    tokenFreq = {}
    tokenFreqStem = {}
    numOfSentDisplayed = 0
    numOfSentTagged = 0
    totalTokens = 0
    c1 = 0
    c2 = 0
    for line in datafile:
        data = json.loads(line)
        c1 += len(tokenize(data['reviewText']))
        c2 += len(segBeforeTokenize(data['reviewText']))

        if len(tokenize(data['reviewText'])) != len(segBeforeTokenize(data['reviewText'])):
            print "Without sentence segmentation", tokenize(data['reviewText'])
            print "With sentence segmentation", segBeforeTokenize(data['reviewText'])

        if random.randint(1,100) < 5 and numOfSentDisplayed < 5:
            sentences = ""
            if len(nltk.sent_tokenize(data['reviewText'])) > 5 and numOfSentDisplayed < 2:
                sentences = nltk.sent_tokenize(data['reviewText'])
                numOfSentDisplayed += 1
            elif len(nltk.sent_tokenize(data['reviewText'])) < 5 and numOfSentDisplayed >= 2:
                sentences = nltk.sent_tokenize(data['reviewText'])
                numOfSentDisplayed += 1

            print "Sentence Segmentation: ", sentences

        if random.randint(1,100) < 5 and numOfSentTagged < 5:
            tagged = tagPOS(data['reviewText'])
            numOfSentTagged += 1
            print ("POS Tagged: ", tagged)


        productCount = countProduct(productCount, data['asin']) # Sentence Segmentation
        reviewCount = countReview(reviewCount, data['reviewerID']) # Sentence Segmentation
        sentCount = countSentence(data['reviewText'], sentCount)  # Count sentence length
        getAcc(data['reviewText'])
        getAcc2(data['reviewText'])
        tokenCountLength, tokenCountLengthStem = countWordsLength(segBeforeTokenize(data['reviewText']), tokenCountLength, tokenCountLengthStem)
        tokenFreq, tokenFreqStem = countWordsFreq(segBeforeTokenize(data['reviewText'], True), tokenFreq, tokenFreqStem)


    print ("Top  10 products: ", sortByValue(getTop(productCount, 10)))
    print ("Top  10 reviewers: ", sortByValue(getTop(reviewCount, 10)))

    plotGraph(sentCount, 'Number of reviews in each length', 'Length of review in number of sentences', 'Sentence count length', 'p1')
    plotGraph(tokenCountLength, 'Number of reviews in each length', 'Length of review in number of tokens', 'Token count length', 'p2')
    plotGraph(tokenCountLengthStem, 'Number of reviews in each length', 'Length of review in number of tokens', 'Stemmed token count length', 'p3')



    print ("Word dict: ", wcount) # Print result of getAcc
    print ("Prod dict: ", wcount2) # Print result of getAcc
    print ("Brown dict: ", wcount3) # Print result of getAcc
    print ("Wordnet dict: ", wcount4) # Print result of getAcc

    print ("Porter Stemmer: ", wcount5) # Print result of getAcc2
    print ("Snowball Stemmer: ", wcount6) # Print result of getAcc2
    print ("Total: ", total) # Print result of getAcc

    print ("Number of distinct tokens before stemming: ", len(tokenFreq.keys()))
    print ("Number of distinct tokens after stemming: ", len(tokenFreqStem.keys()))
    print ("Top 20 words before stemming: ", sortByValue((getTop(tokenFreq, 20))))
    print ("Top 20 words after stemming: ", sortByValue((getTop(tokenFreqStem, 20))))