from whoosh.index import open_dir
from whoosh.qparser import QueryParser, MultifieldParser

import SearchingWhoosh
from MyParser import MyParser
from SearchingWhoosh import StartSearch, CustomRanking





# Query 1

""" UIN:
Trovare cartoni animati che parlano di 'magic' o 'happiness' ordinando risultati per commenti positivi
"""
Query1 =   'magic OR happiness --Msentiment positive --mf True'
Query1_2 = 'magic OR happiness --Lsentiment positive --mf True'





# Query 2
""" UIN:
Trovare tutti i review che esprimono sentimento negativo per un dato cartone animato e che contengono frasi/parole come "waste of time" o "bad" o "do not watch it"
"""

Query2  = '  "do not watch it" or bad or "waste of time" --Msentiment negative --mf True  '
Query2_2 = ' "do not watch it" or bad or "waste of time" --Lsentiment negative --mf True  '




# Query 3
""" UIN:
Trovare tutti i cartoni animati che finiscono per lettera 'Y' e hanno review che esprimono sentimento negativo
"""
Query3 = u'*y --Msentiment negative --mf False'
Query3_2 = ' *y --Lsentiment negative --mf False '




# Query #4
""" UIN:
Trovare tutti i review di cartoni animati che parlano di 'cat' e 'dog' e che esprimono sentimento positivo 
"""
Query4 = ' review:cat review:dog --Msentiment positive '
Query4_2 = ' review:cat review:dog --Lsentiment positive '


# Query #5
""" UIN:
Trovare tutti i cartoni animati con review che esprimono solo sentimento positivo e hanno parole come "like" e "love" e "recommended"
"""
Query5 = 'review:like review:love review:recommended --Msentiment positive'
Query5_2 = 'review:like review:love review:recommended --Lsentiment positive'

# Query #6
""" UIN:
Trovare tutti i cartoni animati con review di sentimento negativo e che hanno parole come "hate" e "skip" e "trash"
"""

Query6 = 'review:hate review:skip review:trash --Msentiment negative'
Query6_2 = 'review:hate review:skip review:trash --Lsentiment negative'



# Query #7
""" UIN:
Trovare tutti i review negativi per un cartone animato chimato 'bebop' e che fanno confronto con un cartone animato chimato "naruto" 
"""

Query7 = 'bebop review:naruto --Msentiment negative'
Query7_2 = 'bebop review:naruto --Lsentiment negative'

# Query #8
""" UIN:
Per un dato workID=100 trovare tutti i review negativi
"""

Query8 = 'workId:100 --Msentiment negative'
Query8_2 = ' workId:100 --Lsentiment negative'


# Query #9
""" UIN:
Trovare tutti i review positivi e che parlano di Scooby Doo 
"""
Query9 = ' review:"scooby doo" --Msentiment positive'
Query9_2 = 'review:"scooby doo" --Lsentiment positive'

# Query #10
""" UIN:
Trovare tutti i review negativi che parlano di 'adventure'
"""

Query10   =    '  adventure --Msentiment negative --mf True '
Query10_2 =     ' adventure --Lsentiment negative --mf True '

if __name__ == "__main__":
    SearchingWhoosh.main(Query8_2) # <--- Pass a query number