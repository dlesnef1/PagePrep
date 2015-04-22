

__author__ = 'Mariah and David'
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import re
class cleaner:
        def removeCommon(self, text):
            newText=""
            cachedStopWords = stopwords.words("english")

            text = ' '.join([word for word in text.split() if word not in cachedStopWords])
            text=text.split(" ")

            for word in text:
                if word.__contains__("@")==False:
                    newText+=(word+" ")

            re.sub(r'[^\w]', ' ', newText)
            return newText

        def tokenizeText(self,text):
            tokenizer = RegexpTokenizer(r'\w+')
            tokens = tokenizer.tokenize(text)  # return the tokens
            return tokens


test=cleaner()
commonRemoved=test.removeCommon("@hisart76 Nothing soothes a smoker like a cloud of 2nd-hand smoke.")
print(commonRemoved)
print(test.tokenizeText(commonRemoved))