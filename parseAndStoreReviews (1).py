
from __future__ import print_function
import os
import nltk.classify.util, nltk.metrics
import pickle

from nltk.tokenize import word_tokenize
from nltk.corpus import CategorizedPlaintextCorpusReader
from nltk.classify import DecisionTreeClassifier
import string
import math
from tabulate import tabulate
import collections
import itertools
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk import precision
from nltk.classify import NaiveBayesClassifier
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import TrigramAssocMeasures


corpus_root1='C:/TTU_CS/FALL - 2018/Pattern Recognition/Project/Sentiment Analysis/CS5341_Final_proj_submission/Dataset/train'
train=CategorizedPlaintextCorpusReader(corpus_root1,r'(pos|neg)/.*\.txt',cat_pattern=r'(pos|neg)/.*\.txt')

corpus_root2='C:/TTU_CS/FALL - 2018/Pattern Recognition/Project/Sentiment Analysis/CS5341_Final_proj_submission/Dataset/test'
test=CategorizedPlaintextCorpusReader(corpus_root2,r'(pos|neg)/.*\.txt',cat_pattern=r'(pos|neg)/.*\.txt')

# create list of all reviews. List of tuples - each tuple contains full text, id, rating, sentiment (0 = negative, 1 = positive)
def parseReviews(directory, includeFullText):
    reviewList = []
    for root, dirs, files in os.walk(directory):
        for name in files:
            if name.endswith(".txt"):
                fullPath = os.path.join(root, name)
                file = open(fullPath)
                text = file.read()
                splitter = name.index("_")
                dot = name.index(".")
                id = int(name[:splitter])
                rating = int(name[splitter+1:dot])
                sentiment = "pos"
                if rating <= 4:
                    sentiment = "neg"
                file.close()
                text = text.encode('ascii','ignore')
                #text = text.decode('unicode_escape').encode('ascii','ignore')
                if (includeFullText):
                    reviewList.append((id, rating, sentiment, text, word_tokenize(text)))
                else:
                    reviewList.append((id, rating, sentiment, word_tokenize(text)))
    print (reviewList)

    return reviewList


def parseTestReviews(directory):
    reviewList = []
    for root, dirs, files in os.walk(directory):
        for name in files:
            if name.endswith(".txt"):
                fullPath = os.path.join(root, name)
                file = open(fullPath)
                text = file.read()
                splitter = name.index("_")
                dot = name.index(".")
                id = int(name[:splitter])
               # rating = int(name[splitter+1:dot])
                file.close()
               # dot = name.index(".")
               # id = int(name[:dot])


                text = text.decode('unicode_escape').encode('ascii','ignore')
                reviewList.append((id, word_tokenize(text)))
    return reviewList

def evaluate_classifier_euclidieanDistance(instance1, instance2, length)
	distance = 0
	for x in range(length):
		distance += pow((instance1[x] - instance2[x]), 2)
	return math.sqrt(distance)

def getNeighbors(trainingSet, testInstance, k):
	distances = []
	length = len(testInstance)-1
	for x in range(len(trainingSet)):
		dist = euclideanDistance(testInstance, trainingSet[x], length)
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors
	accuracy1 = nltk.classify.util.accuracy(getNeighbors, instance1, instance2)

def getResponse(neighbors):
	classVotes = {}
	for x in range(len(neighbors)):
		response = neighbors[x][-1]
		if response in classVotes:
			classVotes[response] += 1
		else:
			classVotes[response] = 1
	sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]

def evaluate_classifier_Naive(featx):

    train_negids = train.fileids('neg')
    train_posids = train.fileids('pos')
    test_negids = test.fileids('neg')
    test_posids = test.fileids('pos')
    train_negfeats = [(featx(train.words(fileids=[f])), 'neg') for f in train_negids]
    train_posfeats = [(featx(train.words(fileids=[f])), 'pos') for f in train_posids]
    test_negfeats = [(featx(test.words(fileids=[f])), 'neg') for f in test_negids]
    test_posfeats = [(featx(test.words(fileids=[f])), 'pos') for f in test_posids]
    trainfeats = train_negfeats + train_posfeats
    testfeats = test_negfeats + test_posfeats

    Naive_classifier = NaiveBayesClassifier.train(trainfeats)
    refsets = collections.defaultdict(set)
    testsets_Naive = collections.defaultdict(set)

    for i, (feats, label) in enumerate(testfeats):
            refsets[label].add(i)
            observed_Naive = Naive_classifier.classify(feats)
            testsets_Naive[observed_Naive].add(i)

    accuracy1 = nltk.classify.util.accuracy(Naive_classifier, testfeats)
    pos_precision1 = nltk.precision(refsets['pos'], testsets_Naive['pos'])
    pos_recall1 = nltk.recall(refsets['pos'], testsets_Naive['pos'])
    neg_precision1 = nltk.precision(refsets['neg'], testsets_Naive['neg'])
    neg_recall1 = nltk.recall(refsets['neg'], testsets_Naive['neg'])

    Naive_classifier.show_most_informative_features(50)

    return(['NaiveBayes',accuracy1,pos_precision1,pos_recall1,neg_precision1,neg_recall1])



def evaluate_classifier_Decision(featx):

    train_negids = train.fileids('neg')
    train_posids = train.fileids('pos')
    test_negids = test.fileids('neg')
    test_posids = test.fileids('pos')
    train_negfeats = [(featx(train.words(fileids=[f])), 'neg') for f in train_negids]
    train_posfeats = [(featx(train.words(fileids=[f])), 'pos') for f in train_posids]
    test_negfeats = [(featx(test.words(fileids=[f])), 'neg') for f in test_negids]
    test_posfeats = [(featx(test.words(fileids=[f])), 'pos') for f in test_posids]
    trainfeats = train_negfeats + train_posfeats
    testfeats = test_negfeats + test_posfeats

    train_negcutoff = int(len(train_negfeats)*1/100)
    train_poscutoff = int(len(train_posfeats)*1/100)
    trainfeats_Decision = train_negfeats[:train_negcutoff] + train_posfeats[:train_poscutoff]
    DecisionTree_classifier = DecisionTreeClassifier.train(trainfeats_Decision)
    refsets = collections.defaultdict(set)
    testsets_Decision = collections.defaultdict(set)

    for i, (feats, label) in enumerate(testfeats):
            refsets[label].add(i)
            observed_Decision = DecisionTree_classifier.classify(feats)
            testsets_Decision[observed_Decision].add(i)

    accuracy3 = nltk.classify.util.accuracy(DecisionTree_classifier, testfeats)
    pos_precision3 = nltk.precision(refsets['pos'], testsets_Decision['pos'])
    pos_recall3 = nltk.recall(refsets['pos'], testsets_Decision['pos'])
    neg_precision3 = nltk.precision(refsets['neg'], testsets_Decision['neg'])
    neg_recall3 = nltk.recall(refsets['neg'], testsets_Decision['neg'])

    return(['DecisionTree',accuracy3,pos_precision3,pos_recall3,neg_precision3,neg_recall3])


def evaluate_classifier_SVM(featx):

	# split the data into training and testing set 
	train_negids = train.fileids('neg')
    train_posids = train.fileids('pos')
    test_negids = test.fileids('neg')
    test_posids = test.fileids('pos')
    train_negfeats = [(featx(train.words(fileids=[f])), 'neg') for f in train_negids]
    train_posfeats = [(featx(train.words(fileids=[f])), 'pos') for f in train_posids]
    test_negfeats = [(featx(test.words(fileids=[f])), 'neg') for f in test_negids]
    test_posfeats = [(featx(test.words(fileids=[f])), 'pos') for f in test_posids]
    trainfeats = train_negfeats + train_posfeats
    testfeats = test_negfeats + test_posfeats
    pipeline_svm = make_pipeline(vectorizer, SVC(probability=True, kernel="linear", class_weight="balanced"))

	grid_svm = GridSearchCV(pipeline_svm,
                    param_grid = {'svc__C': [0.01, 0.1, 1]}, 
                    cv = kfolds,
                    scoring="roc_auc",
                    verbose=1,   
                    n_jobs=-1) 

	grid_svm.fit(train_posids, train_negids)
	grid_svm.score(test_posids, test_negids)


from nltk.corpus import stopwords
stopset = set(stopwords.words('english'))

def stopword_filtered_word_feats(words):
    return dict([(word, True) for word in words if word not in stopset])

table4 = []
table4.append(evaluate_classifier_Decision(stopword_filtered_word_feats))
table4.append(evaluate_classifier_Naive(stopword_filtered_word_feats))

print('Stop words features:')
print(tabulate(table4, headers=["No of Experiemnts","Number of reviews in training data","Classifier","Accuracy","Positive precision", "Positive recall"]))


def word_feats(words):
    return dict([(word, True) for word in words])

table1 = []
table1.append(evaluate_classifier_Decision(word_feats))
table1.append(evaluate_classifier_Naive(word_feats))

print('Single word features:')
print(tabulate(table1, headers=["No of Experiemnts","Number of reviews in training data","Classifier","Accuracy", "Negative precision", "Negative recall"]))



def bigram_word_feats(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
    words_nopunc = [word for word in words if word not in string.punctuation]
    bigram_finder = BigramCollocationFinder.from_words(words_nopunc)
    bigrams = bigram_finder.nbest(score_fn, n)
    return dict([(ngram, True) for ngram in itertools.chain(words_nopunc, bigrams)])

table2 = []
table2.append(evaluate_classifier_Decision(bigram_word_feats))
table2.append(evaluate_classifier_Naive(bigram_word_feats))

print('Bigram word features:')
print(tabulate(table2, headers=["No of Experiemnts","Number of reviews in training data","Classifier","Accuracy", "Negative precision", "Negative recall"]))

print('correct classifications')
print(tabulate(table3, headers=["No of Experiemnts","Classifier","Accuracy","Correct Sample", "Incorrect Sample"]))


if __name__ == "__main__":
    reviews = parseReviews("C:/TTU_CS/FALL - 2018/Pattern Recognition/Project/Sentiment Analysis/CS5341_Final_proj_submission/Dataset/train", False)
    testreviews = parseReviews("C:/TTU_CS/FALL - 2018/Pattern Recognition/Project/Sentiment Analysis/CS5341_Final_proj_submission/Dataset/train", False)
    pickle.dump(reviews, open("C:/TTU_CS/FALL - 2018/Pattern Recognition/Project/Sentiment Analysis/CS5341_Final_proj_submission/dumpTrain.p", "wb"))
    pickle.dump(testreviews, open("C:/TTU_CS/FALL - 2018/Pattern Recognition/Project/Sentiment Analysis/CS5341_Final_proj_submission/dumpTest.p", "wb"))
