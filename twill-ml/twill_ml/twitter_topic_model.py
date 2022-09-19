from twill_ml import logger
from twill_ml.config import get_env, get_data_path
from twill_ml.dataloader import TwitterDataLoader
from bertopic import BERTopic

class TwitterTopicModel:
    def __init__(self, dl: TwitterDataLoader):
        self.dl = dl
        self.model = BERTopic()

    def train(self, tweets=None):
        logger.info('Training model...')
        if not tweets:
            tweets = self.dl.data['tweet']
        topics, probs = self.model.fit_transform(tweets)
        self.topics = topics
        self.probs = probs
        return self.topics, self.probs

    def predict(self, tweet):
        logger.info('Predicting topic', tweet=tweet)
        return self.model.transform([tweet])