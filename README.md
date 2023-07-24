# Search Engine with Sentiment analysis

Search engine using Whoosh library for opinions from various data sources, such as product reviews, movie reviews, service reviews, forums, and blogs. It will allow users to formulate requests using a customized query language to obtain relevant and sorted results based on the content and opinions expressed in the text items.

- Pretrained Text classification model used: DistilBERT base uncased finetuned SST-2
https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english

- Two types of sentiment analsysis techniques used: 
1. Machine Learning approach (DistilBERT SST-2)
2. Dictionary Lexicon based approach
