__author__ = 'Mariah and David'

from model import dbContainer
from cleaner import cleaner
import math
import operator

class Methods:
    def __init__(self):
        self.clean = cleaner()
        self.allWords={}
        self.tfDictTrain={}
        self.tfDictNew={}
        self.sharedTermsDict={}
        self.simDict={}
        self.db = dbContainer()
        self.all = self.db.get_all()
        # 0 - original, 1 - rank, 2 - stemmed, 3 - no common
        # don't forget they aren't lists, simply strings separated by commas

    def rate_status(self,statusIn,testIn,badIn):
        status_clean = self.clean.tokenizeText(statusIn)
        self.naive_setup(testIn)
        scores = self.naive_bayes(status_clean,badIn)
        return self.rank_it(scores)

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

    def naive_bayes(self,status,bad_words):
        scores = {}
        scores['positive'] = math.log(self.naive_classes_prior['positive'])
        scores['neutral'] = math.log(self.naive_classes_prior['neutral'])
        scores['negative'] = math.log(self.naive_classes_prior['negative'])

        for aType in self.naive_classes_prior:
            for word_status in status:
                count = 0
                for i in self.naive_classes_words[aType]:
                    if word_status == i:
                        if bad_words != []:
                            if word_status in bad_words:
                                count += 10
                            else:
                                count += 1
                        else:
                            count += 1
                scores[aType] += math.log((count + 1)/(self.naive_classes_count[aType]+self.unique))

        return scores

    def rank_it(self,scores):
        sorted_S = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)

        if (math.fabs(sorted_S[0][1])+1) < math.fabs(sorted_S[1][1]) :
            return (sorted_S[0][0])
        else:
            return ('neutral')

    #start kNN implementation
    def kNN_fillDict(self,type):
        #for each term in the docs add the index it occurs to the dictionary
        for i in range(len(self.all)):
            status=self.all[i][type].split(",")
            for j in range(len(status)):
                term = status[j]
                if term not in self.allWords:
                    self.allWords[term]={i: [j]}

                elif i not in self.allWords[term]:
                    self.allWords[term][i]=[j]
                else:
                    self.allWords[term][i].append(j)
        self.kNN_getTrainedTermFreq()

    def kNN_getTrainedTermFreq(self):
        #get weighted term frequencies of each term per doc
        for term in self.allWords:
            for id in self.allWords[term]:
                termFreq=(1+math.log10(len(self.allWords[term][id])))*(math.log10(len(self.all)/len(self.allWords[term].keys())))
                if term not in self.tfDictTrain:
                    self.tfDictTrain[term] = {id: termFreq}
                elif id not in self.tfDictTrain[term]:
                    self.tfDictTrain[term][id]=termFreq

    def kNN_getNewTermFreq(self,newDoc):
        #get term frequencies for the new text you are trying to classify
        newDoc_clean=self.clean.removeCommon(newDoc)
        newDoc_clean=self.clean.tokenizeText(newDoc_clean)
        for term in newDoc_clean:
            if term not in self.tfDictNew:
                self.tfDictNew[term]=1
            else:
                self.tfDictNew[term]+=1

        for term in self.allWords:
            if term in self.tfDictNew:
                self.tfDictNew[term]=1+math.log10(self.tfDictNew[term])*(math.log10(len(self.all)/len(self.allWords[term].keys())))

        return newDoc_clean

    def kNN_getCommonTerms(self,queryDoc,badWords):
        #find what trained docs have common terms with new doc
        #make note of docs id and the common terms
        newDoc = self.kNN_getNewTermFreq(queryDoc)

        for term in self.allWords:
            if term in newDoc:
                for id in self.allWords[term]:
                    if id not in self.sharedTermsDict:
                        self.sharedTermsDict[id]=[term]
                    else:
                        self.sharedTermsDict[id].append(term)
        self.kNN_calculateSim(badWords)

    def kNN_calculateSim(self,badWords):
        newTerms=0
        trainTerms=0
        badWords=self.clean.tokenizeText(badWords)

        for id in self.sharedTermsDict:
            for term in self.sharedTermsDict[id]:
                if id not in self.simDict:
                    self.simDict[id]=self.tfDictNew[term]*self.tfDictTrain[term][id]
                else:
                    self.simDict[id]+=self.tfDictNew[term]*self.tfDictTrain[term][id]

                if term in badWords:
                        self.simDict[id] += 2

        for term in self.tfDictNew:
                newTerms+=self.tfDictNew[term]*self.tfDictNew[term]
        for term in self.tfDictTrain:
            for id in self.tfDictTrain[term]:
                trainTerms+=self.tfDictTrain[term][id]*self.tfDictTrain[term][id]
        newTerms=math.sqrt(newTerms)
        trainTerms=math.sqrt(trainTerms)
        for id in self.simDict:
            self.simDict[id]=self.simDict[id]/(newTerms*trainTerms)


    def kNN_getClass(self,newDoc,type,badWords):
        self.kNN_fillDict(type)
        self.kNN_getCommonTerms(newDoc,badWords)
        sortedSims = sorted(self.simDict.items(), key=operator.itemgetter(1),reverse=True)
        cDocsSum=[0,0,0]
        kDocsSum=0
        k=5
        for i in sortedSims[0:k-1]:
            if self.all[i[0]][1]<0:
                cDocsSum[0]+=i[1]
            if self.all[i[0]][1]>0:
               cDocsSum[1]+=i[1]
            if self.all[i[0]][1]==0:
                cDocsSum[2]+=i[1]


        for i in sortedSims[0:k-1]:
            kDocsSum+=i[1]



        for i in range(0,3):
             if kDocsSum==0:
                 cDocsSum[i]=0
             else:
                 cDocsSum[i]=cDocsSum[i]/kDocsSum

        finalClass=max(cDocsSum)

        if finalClass==cDocsSum[0]:
             return("negative")
        elif finalClass==cDocsSum[1]:
             return("positive")
        elif finalClass==cDocsSum[2]:
            return("neutral")






