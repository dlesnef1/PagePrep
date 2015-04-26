#This class is where we will implement Naive Bayes, kNN, and our old method of marking
#It will not do any of the "science", its purpose is to simply read from the DB and classify each status
#into either the negative, positive, or neutral classes

__author__ = 'Mariah and David'

from model import dbContainer
from cleaner import cleaner
import math

class Methods:
    def __init__(self):
        self.clean = cleaner()

        self.db = dbContainer()
        self.all = self.db.get_all()
        # 0 - original, 1 - rank, 2 - stemmed, 3 - no common
        # don't forget they aren't lists, simply strings separated by commas

    def rate_status(self,statusIn):
        status_clean = self.clean.tokenizeText(statusIn)
        self.naive_setup(2)
        self.naive_bayes(status_clean)

    def naive_setup(self,type):
        self.naive_classes_prior = {'neutral':0,'positive':0,'negative':0}
        self.naive_classes_count = {'neutral':0,'positive':0,'negative':0}
        self.naive_classes_words = {'neutral':[],'positive':[],'negative':[]}
        total = 0
        unique = []

        for some in self.all:
            status = some[type].split(",")
            if int(some[1]) == 0:
                typeC = 'neutral'
                self.naive_classes_prior['neutral'] += 1
                self.naive_classes_count['neutral'] += len(status)
                total += 1
            elif int(some[1]) > 0:
                typeC = 'positive'
                self.naive_classes_prior['positive'] += (math.fabs(int(some[1])))
                self.naive_classes_count['positive'] += len(status)
            else:
                typeC = 'negative'
                self.naive_classes_prior['negative'] += (math.fabs(int(some[1])))
                self.naive_classes_count['negative'] += len(status)

            total += math.fabs(int(some[1]))

            for word in status:
                self.naive_classes_words[typeC].append(word)
                if word not in unique:
                    unique.append(word)

        for i in self.naive_classes_prior:
            self.naive_classes_prior[i] = self.naive_classes_prior[i]/total

        self.unique = len(unique)

    def naive_bayes(self,status):
        scores = {}
        scores['positive'] = math.log(self.naive_classes_prior['positive'])
        scores['neutral'] = math.log(self.naive_classes_prior['neutral'])
        scores['negative'] = math.log(self.naive_classes_prior['negative'])

        for aType in self.naive_classes_prior:
            for word_status in status:
                count = 0
                for i in self.naive_classes_words[aType]:
                    if word_status == i:
                        count += 1
                scores[aType] += math.log((count +1)/(self.naive_classes_count[aType]+self.unique))

        print(scores)

test = Methods()