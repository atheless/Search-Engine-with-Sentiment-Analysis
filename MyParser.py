import argparse



class MyParser:

    def __init__(self, user_query):
        self.mf = 0
        self.Lsentiment = None
        self.Msentiment = None
        self.parsed_user_query = None
        self.user_query = user_query

    def parse(self):
        parser = argparse.ArgumentParser()

        group = parser.add_mutually_exclusive_group()

        # Main query
        parser.add_argument('MainQuery', type=str, nargs='+', help='Main query')

        # Sentiment Analysis based on Machine Learning trained model.
        group.add_argument('--Msentiment', type=str, help='Machine Learning Sentiment Analysis')

        # Sentiment Analysis based on Lexicon dictionary analysis.
        group.add_argument('--Lsentiment', type=str, help='Lexicon Sentiment Analysis')

        # Multifield Search option.
        parser.add_argument('--mf', type=str, help='Multifield Search')

        args = parser.parse_args(self.user_query.split())


        if args.Msentiment: # If Msentiment was defined
            if args.Msentiment not in ['positive', 'negative']:
                raise Exception("--Msentiment: Invalid argument.")

            if args.Msentiment == 'positive':
                self.Msentiment = 0
            else:
                self.Msentiment = 1

        if args.Lsentiment: # If Lsentiment was defined
            if args.Lsentiment not in ['positive', 'negative', 'neutral']:
                raise Exception("--Lsentiment: Invalid argument.")

            if args.Lsentiment == 'positive':
                self.Lsentiment = 0
            else:
                self.Lsentiment = 1

        if args.mf: # If mf was defined
            if args.mf not in ['True', 'False']:
                raise Exception("--mf: Invalid argument.")
            if args.mf == 'True':
                self.mf = 1
            else:
                self.mf = 0

        self.parsed_user_query = ' '.join(args.MainQuery)


