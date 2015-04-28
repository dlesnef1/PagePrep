
__author__ = 'Mariah and David'

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
import re

class cleaner:
        def removeCommon(self, text):
            newText=""
            cachedStopWords = stopwords.words("english")

            text = ' '.join([word for word in text.split() if word.lower() not in cachedStopWords])

            return text

        def tokenizeText(self,text):
            tokenizer = RegexpTokenizer(r'\w+')
            tokens = tokenizer.tokenize(text) # return the tokens
            stemmer = PorterStemmer()
            lower = []
            for token in tokens:
                if '@' in token:
                    continue
                lower.append(stemmer.stem(token.lower()))

            return lower

