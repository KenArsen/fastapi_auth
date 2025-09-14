from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr

class TokenShema(BaseModel):
    access_token: str
    token_type: str


class TokenDataShema(BaseModel):
    email: Annotated[str, EmailStr, MinLen(1), MaxLen(255)]
    password: Annotated[str, MinLen(1), MaxLen(100)]

    model_config = {
        "json_schema_extra": {
            "example": {"email": "arsen@gmail.com", "password": "arsen2002"}
        }
    }