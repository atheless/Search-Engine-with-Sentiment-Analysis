from whoosh import scoring, sorting
from whoosh.index import open_dir
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh.scoring import WeightingModel, BaseScorer

from MyParser import MyParser

input_class = None

SelectedAnalysisMethod = None

sentiment_classes = {
    0: 'POSITIVE',
    1: 'NEGATIVE',
}


class CustomRanking(WeightingModel):

    def __init__(self):
        self.fn = self.custom_scoring

    def scorer(self, searcher, fieldname, text, qf=1):
        return self.FunctionScorer(self.fn, searcher, fieldname, text, qf=qf)

    class FunctionScorer(BaseScorer):
        def __init__(self, fn, searcher, fieldname, text, qf=1):
            self.fn = fn
            self.searcher = searcher
            self.fieldname = fieldname
            self.text = text
            self.qf = qf

        def score(self, matcher):
            return self.fn(self.searcher, self.fieldname, self.text, matcher)

    @staticmethod
    def custom_scoring(searcher, fieldname, text, matcher):

        docid = matcher.id()
        doc = searcher.stored_fields(docid)

        if SelectedAnalysisMethod == 'Lexicon':
            if doc['sentimentLabelLexiconAnalysis'] != sentiment_classes[input_class]:
                return 0

        if SelectedAnalysisMethod == 'Machine':
            if doc['sentimentLabel'] != sentiment_classes[input_class]:
                return 0

        bm25 = scoring.BM25F().scorer(searcher, fieldname, text).score(matcher)
        tf_idf = scoring.TF_IDF().scorer(searcher, fieldname, text).score(matcher)

        finalscore = 0

        if SelectedAnalysisMethod == 'Lexicon':
            finalscore = bm25 + doc['sentimentScoreLexiconAnalysis']
        if SelectedAnalysisMethod == 'Machine':
            finalscore = tf_idf + doc['sentimentScore']

        return finalscore


def StartSearch(searcher, query, myparser):


    global input_class
    global SelectedAnalysisMethod

    user_query = myparser.parsed_user_query

    if myparser.Lsentiment is not None:
        input_class = myparser.Lsentiment
        SelectedAnalysisMethod = 'Lexicon'
    else:
        input_class = myparser.Msentiment
        SelectedAnalysisMethod = 'Machine'

    facet = sorting.FieldFacet("sentimentLabel")
    results = searcher.search(query, limit=None, groupedby=facet)  # limit=None
    dictT = results.groups()

    if len(results) == 0:
        print("Empty result!!")
        if searcher.suggest("workName", user_query):
            print('\t [?] Did you mean', end=' ')
            for x in searcher.suggest("workName", user_query):
                print(x, '?', end=' ')
    else:
        print(f'Total results found = {results.__len__()}')
        print(f'--------------------------------------')
        if SelectedAnalysisMethod != 'Lexicon':
            print(
                f'Total # of {len(dictT[sentiment_classes[input_class]])} {sentiment_classes[input_class]} review found. \n')

        for hit in results:
            if hit.rank < 30:
                print(f"Name = {hit['workName']}")
                print(f"workId = https://myanimelist.net/anime/{hit['workId']}")
                print(f'Rank = {hit.rank}')
                print(f'Score = {hit.score}')
                print(f'Review = {hit["review"]}')

                if SelectedAnalysisMethod == 'Lexicon':
                    print(f'LexiconAnalyzer Class = {hit["sentimentLabelLexiconAnalysis"]}')
                    print(f'LexiconAnalyzer Score = {hit["sentimentScoreLexiconAnalysis"]}')
                else:
                    print(f'Sentiment Class = {hit["sentimentLabel"]}')
                print('\n')


def main(user_query=None):
    ix = open_dir("indexdir", indexname='Test')
    searcher = ix.searcher(weighting=CustomRanking)


    print('\n\n')
    if user_query is None:
        user_query = input('Enter query:')
    myparser = MyParser(user_query)
    myparser.parse()

    parser = QueryParser("workName", schema=ix.schema, )
    mparser = MultifieldParser(["workName", "review"], schema=ix.schema)
    query = None

    if myparser.mf:
        query = mparser.parse(myparser.parsed_user_query)
    else:
        query = parser.parse(myparser.parsed_user_query)

    print('[>>>] Searching for:', user_query, end='\n')
    print('[>>>] Querying:', query)

    StartSearch(searcher, query, myparser)


if __name__ == "__main__":
    main()
