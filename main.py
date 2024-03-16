from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
from pydantic import BaseModel
import logging
import json

from scheduler  import SCHEDULER
from database   import DATABASE
from recommend  import RECOMMEND
from similarity import SIMILARITY

backend = FastAPI()

class SCHEDULE_REQUEST(BaseModel):
    req_start_date : str
    req_end_date   : str
    mentor_email   : str
    

@backend.post('/schedule')
def schedule(input: SCHEDULE_REQUEST):

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    database = DATABASE(logger)
    response = database.connect()

    if not database.connection:
        return JSONResponse(content=None)
    
    try:
        scheduler = SCHEDULER(logger, response)
        res = scheduler.isValid(input.req_start_date, input.req_end_date, input.mentor_email)

        return JSONResponse(content={'Error': '', 'response': res}, status_code=200)
    
    except Exception as e:
        return JSONResponse(content={'Error': e, 'response': ''}, status_code=422)
    

@backend.post('/recommend')
def recommend_mentors(input:str, topn_skills:int=10, topn_mentors:int=50):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    database = DATABASE(logger)
    response = database.connect()

    if not database.connection:
        return JSONResponse(content=None)
    
    try:
        recommend = RECOMMEND(logger)
        skills = recommend.recommend(response, input, topn_skills)

        similarity          = SIMILARITY(logger)
        mentors             = similarity.fetch_data(response)
        recommended_mentors = similarity.jaccard_similarity(skills, mentors, topn_mentors)

        return JSONResponse(content={'Error': '', 'response':json.dumps(recommended_mentors, indent=2)}, status_code=200)


    except Exception as e:
        return JSONResponse(content={'Error': e, 'response': ''}, status_code=422)



if __name__ == "__main__":
    uvicorn.run(backend, host="127.0.0.1", port=9000)
