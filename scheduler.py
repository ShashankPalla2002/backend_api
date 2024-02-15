import json
from datetime import datetime

class SCHEDULER:
    def __init__(self, logger, database):
        self.logger   = logger
        self.database = database

    
    def find_existing_slots(self, mentor_email):
        try:
            booked_slots = self.database.table("schedule_mentors").select("*").eq('mentor_email', mentor_email).execute()
            booked_slots = json.loads(booked_slots.model_dump_json())['data']    
            self.logger.info(f"booked_slots: {booked_slots}")

            slots = []
            for i in range(len(booked_slots)):
                start_date = datetime.strptime(booked_slots[i]['start_time'], "%Y-%m-%dT%H:%M:%S")           
                end_date = datetime.strptime(booked_slots[i]['end_time'], "%Y-%m-%dT%H:%M:%S")
                slots.append([start_date, end_date])

                self.logger.info(f"start_date: {start_date}, end_date: {end_date}")


            return sorted(slots, key=lambda x: x[0])
        
        except Exception as e:
            self.logger.info(e)
            return []


    def isValid(self, req_start_date, req_end_date, mentor_email):

        req_start_date = datetime.strptime(req_start_date, "%Y-%m-%dT%H:%M:%S")
        req_end_date   = datetime.strptime(req_end_date, "%Y-%m-%dT%H:%M:%S")
        
        self.logger.info(f"req_start_date: {req_start_date}, req_end_date: {req_end_date}")
        
        existing_slots = self.find_existing_slots(mentor_email)
        self.logger.info(f"existing slots: {existing_slots}")

        for slot in existing_slots:
            if req_end_date > slot[0] and req_start_date < slot[1]:
                return False
            
        return True

        


if __name__ == "__main__":
    # from database import DATABASE
    # import logging

    # logger = logging.getLogger()
    # logger.setLevel(logging.INFO)

    # database  = DATABASE(logger).connect()
    # scheduler = SCHEDULER(logger, database)
    # logger.info(scheduler.isValid("2024-02-17T01:00:00", "2024-02-17T01:30:00", "divyas@gmail.com"))
    pass