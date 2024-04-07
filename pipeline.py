import sys
from sklearn.pipeline                import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

from preprocessing import CONVERT_TO_LOWER, REMOVE_SPECIAL_CHARACTERS, REMOVE_STOPWORDS, LEMMETIZATION

class PIPELINE:
    def __init__(self, logger):
        self.logger = logger

    def make_pipeline(self):
        try:
            self.logger.info(f'generating the pipeline')
            pipe = Pipeline(steps=[
                ('convert_to_lower',          CONVERT_TO_LOWER(self.logger)),
                ('remove_special_characters', REMOVE_SPECIAL_CHARACTERS(self.logger)),
                ('remove_stopwords',          REMOVE_STOPWORDS(self.logger)),
                ('stemmetization',            LEMMETIZATION(self.logger)),
                ('vetorizer',                 TfidfVectorizer())
            ])

            self.logger.info(f"generated the pipeline: {pipe}")
            return pipe
        
        except Exception as e:
            self.logger.error(f"error while generating the pipeline: {e}")