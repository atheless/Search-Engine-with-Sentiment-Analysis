import time

from whoosh.index import create_in
from whoosh.fields import *
import os, os.path
from csv import DictReader
from transformers import pipeline

from LexiconSentimentAnalysis import FlatLexiconAnalyzer

# If dir does not exist
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")

schema = Schema(
    workName=TEXT(analyzer=analysis.StandardAnalyzer(), stored=True),
    workId=ID(stored=True),
    review=TEXT(stored=True, analyzer=analysis.StemmingAnalyzer()),
    sentimentLabel=ID(stored=True, sortable=True),
    sentimentScore=NUMERIC(stored=True, sortable=True, signed=False),
    sentimentLabelLexiconAnalysis=ID(stored=True, sortable=True),
    sentimentScoreLexiconAnalysis=NUMERIC(stored=True, sortable=True, signed=False),
)



classifier = pipeline("sentiment-analysis", model='distilbert-base-uncased-finetuned-sst-2-english')

ix = create_in("indexdir", schema, indexname='Test')
writer = ix.writer()

# workId - The Anime work ID labeled by https://myanimelist.net/anime/.... (to be stored)
# review - The comment content (to be stored/indexed)

MyLexiconAnalyzer = FlatLexiconAnalyzer()

start = time.process_time()


# iterate over each line as an ordered dictionary and print only few column by column name
with open('Results/Result_3.csv', 'r') as read_obj:
    csv_dict_reader = DictReader(read_obj)
    print(csv_dict_reader.fieldnames)

    for row in csv_dict_reader:
        if csv_dict_reader.line_num == 10000: break

        result = classifier(row['review'], truncation=True)

        LexiconAnalyzerScore, LexiconAnalyzerLabel = MyLexiconAnalyzer.analyze(row['review'])

        writer.add_document(
            workName=row['engName'],
            workId=row['workId'],
            review=row['review'],
            sentimentLabel=next(result.__iter__())['label'],
            sentimentScore=next(result.__iter__())['score'],
            sentimentLabelLexiconAnalysis=LexiconAnalyzerLabel,
            sentimentScoreLexiconAnalysis=LexiconAnalyzerScore,
        )

writer.commit()
print("Total added: ", writer.doc_count())
print("Time passed: ", time.process_time() - start)
