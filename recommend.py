import json
import pickle
import pandas as pd
import numpy  as np

from sklearn.metrics.pairwise import cosine_similarity

from database                         import DATABASE
from pipeline   import PIPELINE
from llm        import LLM
from similarity import SIMILARITY


class RECOMMEND:
    def __init__(self, logger):
        self.logger = logger

    
    def serialize_model(self, type, value):
        try:
            if type == "values":
                with open(r'sparse_matrix.pkl', 'wb') as file:
                    pickle.dump(value, file)
                    file.close()
                
                self.logger.info(f"serialized the values into sparse_matrix.pkl file")

            else:
                with open(r'pipeline.pkl', 'wb') as file:
                    pickle.dump(value, file)
                    file.close()
                
                self.logger.info(f"serialized the values into pipeline.pkl file")

        except Exception as e:
            self.logger.error(f"error while serializing: {e}")

    
    def deserialize_model(self, type):
        try:
            if type == "values":
                with open(r'sparse_matrix.pkl', 'rb') as file:
                    loaded_values = pickle.load(file)
                    file.close()

                self.logger.info(f"deserialized the values from the sparse_matrix.pkl file")
                return loaded_values
            
            else:
                with open(r'pipeline.pkl', 'rb') as file:
                    loaded_values = pickle.load(file)
                    file.close()

                self.logger.info(f"deserialized the values from the pipeline.pkl file")
                return loaded_values
        
        except Exception as e:
            self.logger.error(f"error while deserializing values: {e}")

    
    def fetch_data(self, object:DATABASE):
        try:
            queried_data = object.table("domains").select("*").execute()
            json_data    = json.loads(queried_data.model_dump_json())['data']
            final_data   = pd.DataFrame(json_data)
            
            self.logger.info(f"fetched the data from the database succesfully")
            return final_data

        except Exception as e:
            self.logger.error(f"error while fetching data from the database: {e}")


    def train(self, data: pd.DataFrame):
        try:
            self.logger.info(f"training of data started")
            pipeline       = PIPELINE(self.logger)
            pipeline       = pipeline.make_pipeline()
            trained_values = pipeline.fit_transform(data['description'])
            self.serialize_model('values', trained_values)
            self.serialize_model('pipeline', pipeline)

        except Exception as e:
            self.logger.error(f"error while training data: {e}")


    def process_value(self, value, description):
        try:
            data = pd.DataFrame([{'name': value, 'description': description}])
            self.logger.info(f"processed data: {data}")
            return data
        
        except Exception as e:
            self.logger.error(f"error while processing value: {e}")
        
    
    def recommend(self, object: DATABASE, value, topn=10):
        try:
            recommendations = []
            llm = LLM(self.logger)

            description = llm.generate_response(value)

            if description != 'None':
                new_data = self.process_value(value, description)
                pipeline = self.deserialize_model('pipeline')

                transformed_data = pipeline.transform(new_data['description'])
                trained_values   = self.deserialize_model("values")

                similarity       = cosine_similarity(transformed_data, trained_values)
                self.logger.info(f'calculated the similarity matrix')
                
                similar_indices  = np.argsort(similarity[0])[::-1][:topn] 
                self.logger.info(f'total number of skill recommended: {len(similar_indices)}')       
                data = self.fetch_data(object)

                for ind in similar_indices:
                    recommendations.append(data.name.loc[ind])

            self.logger.info(f'recommended skills: {recommendations}')
            return recommendations
        
        except Exception as e:
            self.logger.error(f"error in generating recommendation for: {value}: {e}")
        


if __name__ == "__main__":
    import logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    database = DATABASE(logger)
    database = database.connect()

    recommend = RECOMMEND(logger)
    # data = recommend.fetch_data()
    # recommend.train(data)
    similarity = SIMILARITY(logger)
    data = similarity.fetch_data(database)
    print(recommend.recommend(database, 'Power BI'), data)