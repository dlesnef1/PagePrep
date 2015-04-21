__author__ = 'Mariah and David'
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
class cleaner:
        def removeCommon(self, text):
            cachedStopWords = stopwords.words("english")
            text = ' '.join([word for word in text.split() if word not in cachedStopWords])
            return text
        def tokenizeText(self,text):
            tokenizer = RegexpTokenizer(r'\w+')
            tokens = tokenizer.tokenize(text)  # return the tokens
            return tokens


test=cleaner()
commonRemoved=test.removeCommon("Not long till the lunchtime beer session begins")
print(test.tokenizeText(commonRemoved))