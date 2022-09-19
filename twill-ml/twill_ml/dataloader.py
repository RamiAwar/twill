from twill_ml import logger
from twill_ml.config import get_env, get_data_path
from twill_ml.utils import preprocess_tweet

import pandas as pd

class DataLoader:
    def __init__(self, env, mode):
        self.env = env
        if env == 'dev' and not mode:
            self.mode = 'local'
        elif env == 'prod' and not mode:
            self.mode = 'remote'
        else:
            self.mode = mode
        

    def load(self):
        logger.info('Loading data', data=self.data)
        return self.data

class TwitterDataLoader(DataLoader):
    def __init__(self, env=get_env(), mode=None):
        super().__init__(env, mode)
        self.data = self.load()
        self.data['tweet'] = self.data['text']

    def load_from_csv(self):
        path = get_data_path() / 'twitter' / 'twitter.csv'
        if not path.exists():
            logger.error('File not found', path=path)
            raise FileNotFoundError
        return pd.read_csv(path)

    def load(self):
        if self.mode == 'local':
            return self.load_from_csv()
        else:
            logger.error('Mode not supported', mode=self.mode)
            raise NotImplementedError
    
    def preprocess(self):
        self.data['tweet'] = self.data['tweet'].apply(preprocess_tweet)
        return self.data
        