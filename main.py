from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
from pydantic import BaseModel
from datetime import datetime
import logging

from scheduler import SCHEDULER
from database import DATABASE


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


if __name__ == "__main__":
    uvicorn.run(backend, host="localhost", port=9000)
