from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str

class SOPQuery(BaseModel):
    query: str
