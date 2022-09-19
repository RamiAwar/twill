import preprocessor as p
from twill_ml import logger

def preprocess_tweet(tweet):
    return p.tokenize(tweet)