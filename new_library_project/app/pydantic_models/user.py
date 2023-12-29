from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    nickname: str
    email: str
    password: str

class UserHistory(BaseModel):
    user_id : int
    action :str