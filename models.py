from pydantic import BaseModel

class User(BaseModel):
    email: str
    name: str

class Task(BaseModel):
    task_id: str
    user_id: str
    url: str
    status: str
    created_at: str
