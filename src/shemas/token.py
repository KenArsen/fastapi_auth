from pydantic import BaseModel, EmailStr

class TokenShema(BaseModel):
    access_token: str
    token_type: str
