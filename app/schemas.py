from pydantic import BaseModel
class ChatQuery(BaseModel):
    job_id:str
    query:str
    