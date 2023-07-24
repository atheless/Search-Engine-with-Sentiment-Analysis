import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()

    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    return text

def analyze_sentiment(text):
    # Load DistilBERT tokenizer and model
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=2)
    
    preprocessed_text = preprocess_text(text)

    sentences = sent_tokenize(preprocessed_text)

    overall_sentiment_score = 0
    num_sentences = len(sentences)

    ner = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(preprocessed_text)))
    stop_words = set(stopwords.words('english'))

    for sentence in sentences:
        # Analyze sentiment using DistilBERT
        inputs = tokenizer(sentence, return_tensors='pt', truncation=True, padding=True)
        outputs = model(**inputs)
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=1)
        sentiment_scores = probabilities[:, 1].item() - probabilities[:, 0].item()

        # Aspect-Based Sentiment Analysis
        aspect_sentiments = {}
        for word, tag in ner:
            if tag == 'PERSON' or tag == 'ORGANIZATION':
                if word.lower() not in stop_words:
                    if word.lower() in preprocessed_text:
                        aspect_sentiments[word] = sentiment_scores

        # Adjust sentiment score for negation words
        if "not" in sentence or "n't" in sentence:
            sentiment_scores *= -1

        # Adjust sentiment score for intensity modifiers
        for word in word_tokenize(sentence):
            if word in sid.lexicon:
                sentiment_scores *= 1.5

        overall_sentiment_score += sentiment_scores

    # Determine the overall sentiment label based on the average score
    overall_sentiment_score /= num_sentences
    if overall_sentiment_score >= 0.05:
        sentiment_label = 'positive'
    elif overall_sentiment_score <= -0.05:
        sentiment_label = 'negative'
    else:
        sentiment_label = 'neutral'

    return sentiment_label, overall_sentiment_score, aspect_sentiments

if __name__ == "__main__":
    #text example for sentiment analysis
    sample_text = "The service was good, but the food was just okay"

    #perform sentiment analysis on the sample text
    sentiment, overall_score, aspect_sentiments = analyze_sentiment(sample_text)

    #print the results
    print("Text:", sample_text)
    print("Sentiment:", sentiment)
    print("Overall Sentiment Score:", overall_score)
    print("Aspect-Based Sentiments:", aspect_sentiments)
