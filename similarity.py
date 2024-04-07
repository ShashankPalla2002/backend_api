import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
                d['uuid']            = value['uniq_id']
                d['name']            = value['name']
                d['profession']      = value['profession']
                d['company']         = value['company']
                d['experience']      = value['experience']
                d['skills']          = value['skills']['skills']
                d['combined skills'] = ' '.join(d['skills'])
                skills.append(d)
                
            self.logger.info(f"total number of skills fetched: {len(skills)}")            
            self.logger.info(f"fetched the data from the database succesfully")

            return skills
        
       except Exception as e:
           self.logger.error(f"error while fetching data from the database: {e}")

    
    def calculate_similar_mentors(self, values, mentors, topn=50):
        try:
            skills_to_compare = []
            results           = []
            values            = ' '.join(values)

            self.logger.info(f'skills to compare: {values}')

            for mentor in mentors:
                skills_to_compare.append(mentor['combined skills'])

            skills_to_compare.append(values)
            self.logger.info(f'length of total skills: {len(skills_to_compare)}')

            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(skills_to_compare)

            cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
            self.logger.info(f'Calculated cosine similarites')

            cosine_similarities = list(zip(skills_to_compare, cosine_similarities[0]))

            cosine_similarities = sorted(cosine_similarities, key=lambda x: x[1], reverse=True)
            cosine_similarities = cosine_similarities[:topn]
            self.logger.info(f'sorted the skills in descending order')

            for val in cosine_similarities:
                ind = skills_to_compare.index(val[0])
                results.append(mentors[ind])

            return results

        except Exception as e:
            self.logger.error(f'Error while calculating similarites: {e}')
            return []


if __name__ == "__main__":
    pass