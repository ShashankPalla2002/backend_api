import nltk
nltk.download('stopwords')
import string

from nltk.stem     import PorterStemmer
from nltk.corpus   import stopwords
from sklearn.base  import BaseEstimator, TransformerMixin

class PREPROCESSING:    
    def __init__(self, logger):
        self.logger = logger


    def convert_to_lower(self, value:str):
        try:
            self.logger.info(f"value converted to lower case: {value.lower()}")
            return value.lower()
        
        except Exception as e:
            self.logger.error(f"error in converting to lowercase: {e}")

    
    def remove_special_characters_punctuation(self, value:str):
        try:
            punctuation  = list(string.punctuation)
            final_string = ""

            for word in value.split(" "):
                if word not in punctuation:
                    final_string += " " + word

            self.logger.info(f"value after removing special characters: {final_string}")
            return final_string
        
        except Exception as e:
            self.logger.error(f"error in removing special characters: {e}")
    
    
    def remove_stopwords(self, value:str):
        try:
            stopwords_to_remove = stopwords.words('english')
            final_value         = ""

            for word in value.split(" "):
                if word not in stopwords_to_remove:
                    final_value += " " + word

            self.logger.info(f"value after removing stopwords: {final_value.strip()}")
            return final_value.strip()
        
        except Exception as e:
            self.logger.error(f"error in removing stopwords: {e}")

    
    def stemmetize(self, value:str):
        try:
            porter_stemmer = PorterStemmer()
            final_value    = ""

            for word in value.split(" "):
                final_value += " " + porter_stemmer.stem(word)

            self.logger.info(f"value after stemmetizing: {final_value}")
            return final_value

        except Exception as e:
            self.logger.error(f"error in stemmetizing: {e}")
    

class CONVERT_TO_LOWER(BaseEstimator, TransformerMixin, PREPROCESSING):
    def __init__(self, logger):
        self.logger = logger

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X = X.apply(lambda x: PREPROCESSING(self.logger).convert_to_lower(x))
        return X
    

class REMOVE_SPECIAL_CHARACTERS(BaseEstimator, TransformerMixin, PREPROCESSING):
    def __init__(self, logger):
        self.logger = logger

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X = X.apply(lambda x: PREPROCESSING(self.logger).remove_special_characters_punctuation(x))
        return X
    

class REMOVE_STOPWORDS(BaseEstimator, TransformerMixin, PREPROCESSING):
    def __init__(self, logger):
        self.logger = logger

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X = X.apply(lambda x: PREPROCESSING(self.logger).remove_stopwords(x))
        return X
    

class STEMMETIZATION(BaseEstimator, TransformerMixin, PREPROCESSING):
    def __init__(self, logger):
        self.logger = logger

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X = X.apply(lambda x: PREPROCESSING(self.logger).stemmetize(x))
        return X