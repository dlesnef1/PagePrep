#This class is where we will implement Naive Bayes, kNN, and our old method of marking
#It will not do any of the "science", its purpose is to simply read from the DB and classify each status
#into either the negative, positive, or neutral classes

__author__ = 'Mariah and David'

from model import dbContainer
from cleaner import cleaner
class Methods:

    def __init__(self):
        self.clean = cleaner()

        self.db = dbContainer()
        self.all = self.db.get_all()
        # 0 - original, 1 - rank, 2 - stemmed, 3 - no common
        # don't forget they aren't lists, simply strings separated by commas

    def rate_status(self,statusIn):
        status_clean = self.clean.tokenizeText(statusIn)
        print(status_clean)
        self.naive_setup(2)
    def naive_setup(self,type):
        self.naive_classes = {'neutral':0,'positive':0,'negative':0}
        total = 0
        unique = []
        for some in self.all:
            status = some[type].split(",")
            if int(some[1]) == 0:
                self.naive_classes['neutral'] +=1
            elif int(some[1]) > 0:
                self.naive_classes['positive'] += int(some[1])
            else:
                self.naive_classes['negative'] += (-1 * int(some[1]))
                print(status)
        print(self.naive_classes)

test = Methods()
test.rate_status("Fucking bitches, cannot fucking stand dumb sloots")