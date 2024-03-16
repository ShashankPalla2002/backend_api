import json

from database import DATABASE

class SIMILARITY:
    def __init__(self, logger):
        self.logger = logger


    def fetch_data(self, object:DATABASE):
       try:
            skills = []
            queried_data = object.table("mentors").select("*").execute()
            resp = json.loads(queried_data.model_dump_json())['data']

            for value in resp:
                d = {}
                d['uuid']       = value['uniq_id']
                d['name']       = value['name']
                d['profession'] = value['profession']
                d['company']    = value['company']
                d['skills']     = value['skills']['skills']
                skills.append(d)
                
            self.logger.info(f"total number of skills fetched: {len(skills)}")            
            self.logger.info(f"fetched the data from the database succesfully")

            return skills
        
       except Exception as e:
           self.logger.error(f"error while fetching data from the database: {e}")

    
    def jaccard_similarity(self, values:list, mentors:list, topn=50):
        try:
            similarity_dict = {}

            for mentor in mentors:
                skill = mentor['skills']

                intersection = len(list(set(values).intersection(skill)))
                self.logger.info(f"number of intersected values: {intersection}")

                union = len(values)+len(skill) - intersection
                self.logger.info(f"total number of values: {union}")

                similarity = float(intersection)/union
                self.logger.info(f"similarity found between 2 sets: {similarity}")

                similarity_dict[similarity] = mentor
                self.logger.info(f"added the mentor and the similarity pair to dictionary")

            similarity_dict = dict(sorted(similarity_dict.items(), key=lambda item: item[0], reverse=True))
            results         = list(similarity_dict.values())[:topn]

            self.logger.info(f"found top {topn} results from the database: {results}")
            return results

        except Exception as e:
            self.logger.error(f"error while calculating jaccard similarity: {e}") 


if __name__ == "__main__":
    pass
#     import logging
#     logger = logging.getLogger()
#     logger.setLevel(logging.INFO)

#     database = DATABASE(logger)
#     database = database.connect()
#     similarity = SIMILARITY(logger)
#     skills = similarity.fetch_data(database)
#     # print(skills)
#     similarity.jaccard_similarity(['Java', 'Bytecode', 'Spring', 'Ruby', 
# 'Vaadin', 'C', 'Compilers', 'Web Development', 'Node.js', 'Interpreters'] , skills)