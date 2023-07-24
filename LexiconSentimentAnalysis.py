import time

import nltk.tokenize
from nltk.tokenize import word_tokenize

example_sent2 = """
There was just something about Beet that didn’t work. While there were plenty of cool bits and interesting characters (as well as a world setup I thought to be quite novel) it just didn’t seem to gel for me. Perhaps it was the sheer scope of the story and the (correct) feeling one gets that it’s just not going to be fully addressed. By the end of the first series (52 episodes) we've only really seen the coming together of four out of what looks to be a five man team and the series cuts off right in the middle. But apart from that there's                  something that just doesn’t work for me, something that I find rather hard to put my finger on. This is still worth a watch, because if it works for you there’s plenty there and even if it isn’t it may be worth watching the first five or so episodes just for the novelty value of the world setup and the Vandel designs. I'm hoping that the sequel to this (Beet the Vandel Buster: Excellion) will manage to draw out and sustain the high points of the series.         ...
"""
example_sent = "I don't like it"

class FlatLexiconAnalyzer:
    """
    Lexicon-based sentiment analysis that calculates the sentiment score using words present in a text.

    Formula = (number of positive words) / (number of negative words + 1)
        calc < 0,98 -> NEGATIVE
        calc => 0,98 -> POSITIVE
    """

    def __init__(self):
        self._NEGATIVE_WORDS = list()
        self._POSITIVE_WORDS = list()

        with open('opinion-lexicon-English/positive-words.txt', 'r', encoding="utf-8") as f:
            for line in f.readlines():
                self._POSITIVE_WORDS.append(line.strip())

        with open('opinion-lexicon-English/negative-words.txt', 'r', encoding="utf-8") as f:
            for line in f.readlines():
                self._NEGATIVE_WORDS.append(line.strip())

    def analyze(self, text):
        word_tokens = word_tokenize(text)  # Tokenize
        stopwords = nltk.corpus.stopwords.words("english")

        # Removing Stopwords and Punctuation
        cleaned_sentence = [w.lower() for w in word_tokens if w.isalpha() if w.lower() not in stopwords]

        # Lemming
        wnl = nltk.WordNetLemmatizer()
        cleaned_sentence = [wnl.lemmatize(t) for t in cleaned_sentence]

        SentimentP = 0
        SentimentN = 0


        for w in cleaned_sentence:
            if self.BinarySearch(w, self._NEGATIVE_WORDS):
                SentimentN += 1
            if self.BinarySearch(w, self._POSITIVE_WORDS):
                SentimentP += 1

        score = (SentimentP) / (SentimentN + 1)


        Label = None

        if score >= 0.98:
            Label = 'POSITIVE'
        else:
            Label = 'NEGATIVE'

        return score, Label

    @staticmethod
    def BinarySearch(word, wordList):
        first = 0
        last = len(wordList) - 1
        found = False
        while first <= last and not found:
            middle = (first + last) // 2
            if wordList[middle] == word:
                found = True
            else:
                if word < wordList[middle]:
                    last = middle - 1
                else:
                    first = middle + 1
        return found


if __name__ == "__main__":
    MyLA = FlatLexiconAnalyzer()
    start = time.process_time()
    score, Label = MyLA.analyze(example_sent)
    print("Score:", score, " Label:", Label)
    print("Time passed:", time.process_time() - start)
