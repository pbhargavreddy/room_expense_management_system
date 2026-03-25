from pydantic import BaseModel,ConfigDict

class UserCreate(BaseModel):
    username :str
    password:str

class UserValidate(BaseModel):
    username:str
    password : str
    
class RequestCreate(BaseModel):
    title : str
    description :str

class ResponseCreate(BaseModel):
    payment_screenshot : bytes   # image

    model_config = ConfigDict(from_attributes=True)  # ??

