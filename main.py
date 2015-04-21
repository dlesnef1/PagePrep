# 1. need to remove punctuation from original documents
# 2. need to keep in back of mind total score of corpus, as if we have 50 to 1 good to bad, the [-2:2] ranking won't work
# 3. instead of making 0 do nothing, maybe it should even out the number a bit, as those words do have significance
# 4. should weigh important words higher as they mean more to status

# Answer 3: move the weight to 0 by taking the score and multiplying by total % of 0's in corpus
#   if corpus = 20, and 15 are 0s, multiply weight by .75
from nltk.stem import PorterStemmer
import string

class createIndex:
    def __init__(self):
        self.index = {}
        self.totalDocs = 0
        self.netTotal = 0
        self.buildIndex()

    def buildIndex(self):
        openedFile = open('fakeCorpus.txt','r')
        lines = openedFile.readlines()
        #first pass, get total number of 0s, also add up (for future?) net total score, and total number of docs
        zeros = 0
        for doc in lines:
            if len(doc) > 1:
                self.totalDocs+= 1
                if doc.split()[0] == '0':
                    zeros += 1
                else:
                    self.netTotal += int(doc.split()[0])

        #fraction of zeros to total documents
        fracZeros = zeros/self.totalDocs

        for doc in lines:
            docList = doc.split()
            for word in docList[1:]:
                #first normalize it, then store in dictionary (also remove common words)
                word = self.normalizeWord(word)
                if word == 'NonImp':
                    continue
                if word not in self.index:
                    self.index[word] = float(docList[0])
                else:
                    if docList[0] == '0':
                        self.index[word] *= fracZeros
                    else:
                        self.index[word]+= float(docList[0])

        openedFile.close()

    def rateDoc(self,stringIn):
        rating = 0
        listIn = stringIn.split()
        for word in listIn:
            word = self.normalizeWord(word)
            if word in self.index:
                rating += self.index[word]
        return rating

    def normalizeWord(self,wordIn):
        #lowercase it
        word = wordIn.lower()

        #remove common words (do we want to do this?)
        if word in ['a','the','and','an','or','he','she','they','our','his','her']:
            return 'NonImp'

        #stem it
        stemmer=PorterStemmer()
        word = stemmer.stem(word)
        return word

    def cleanFile(self,fileName):
        #read in a file and save back to in normalized form
        openedFile = open(fileName,'r')
        lines = openedFile.readlines()
        for line in lines:
            for c in string.punctuation:
                line = line.replace(c,'')
            line = line.split()
            newLine = []
            for word in line:
                word = self.normalizeWord(word)
                print (word)
                if word != 'NonImp':
                    newLine.append(word)
            newStr = "".join(newLine)
            print (newStr)



index = createIndex()
rating = index.rateDoc('working on charity tomorrow')
print(rating)
index.cleanFile('fakeCorpus.txt')


