from methods import Methods


class experiment:
    def __init__(self):
        self.method = Methods()


    def testNB(self):
        badWords = ['fuck','damn','work','cunt','bitch','whore','asshole']

        lines = self.openFile("testing.txt")
        results_NB = []
        results_NB_noC = []
        results_NB_bad = []
        results_NB_noC_bad = []


        for toCheck in lines:
            status = toCheck.split(";")[1]

            results_NB.append(self.method.rate_status(status,2,[]))
            results_NB_noC.append(self.method.rate_status(status,3,[]))
            results_NB_bad.append(self.method.rate_status(status,2,badWords))
            results_NB_noC_bad.append(self.method.rate_status(status,3,badWords))


        scores = [0,0,0,0]
        scoresn =[0,0,0,0]
        for i in range(len(lines)):
            rate = lines[i].split(";")[0]
            if rate == 'negative':
                if rate == results_NB[i]:
                    scoresn[0] +=1
                if rate == results_NB_noC[i]:
                    scoresn[1] +=1
                if rate == results_NB_bad[i]:
                    scoresn[2] +=1
                if rate == results_NB_noC_bad[i]:
                    scoresn[3] +=1
            if rate == results_NB[i]:
                scores[0] +=1
            if rate == results_NB_noC[i]:
                scores[1] +=1
            if rate == results_NB_bad[i]:
                scores[2] +=1
            if rate == results_NB_noC_bad[i]:
                scores[3] +=1

        print(scores)
        print(scoresn)

    def openFile(self,name):
        this = open(name,'r')
        toReturn = []
        for i in this.readlines():
            toReturn.append(i[:-1])
        return toReturn

    def testKNN(self):
        badWords= "fuck damn work cunt bitch whore asshole horny shit"
        lines = self.openFile("testing.txt")

        results_KNN = []
        results_KNN_noC = []
        results_KNN_bad = []
        results_KNN_noC_bad = []

        for toCheck in lines:
            status = toCheck.split(";")[1]

            results_KNN.append(self.method.kNN_getClass(status,2,""))
            results_KNN_noC.append(self.method.kNN_getClass(status,3,""))
            results_KNN_bad.append(self.method.kNN_getClass(status,2,badWords))
            results_KNN_noC_bad.append(self.method.kNN_getClass(status,3,badWords))


        scores = [0,0,0,0]
        scoresn =[0,0,0,0]
        for i in range(len(lines)):

            rate = lines[i].split(";")[0]
            if rate == 'negative':
                if rate == results_KNN[i]:
                    scoresn[0] +=1
                if rate == results_KNN_noC[i]:
                    scoresn[1] +=1
                if rate == results_KNN_bad[i]:
                    scoresn[2] +=1
                if rate == results_KNN_noC_bad[i]:
                    scoresn[3] +=1
            if rate == results_KNN[i]:
                scores[0] +=1
            if rate == results_KNN_noC[i]:
                scores[1] +=1
            if rate == results_KNN_bad[i]:
                scores[2] +=1
            if rate == results_KNN_noC_bad[i]:
                scores[3] +=1

        print(scores)
        print(scoresn)


test1=experiment()
test1.testNB()
test1.testKNN()