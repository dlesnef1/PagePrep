from methods import Methods


class testing:
    def __init__(self):
        self.method = Methods()
        self.test()

    def test(self):
        badWords = ['fuck','damn','work','cunt','bitch','whore']

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

