from pydantic import BaseModel
from user_schema import UserResponse

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse