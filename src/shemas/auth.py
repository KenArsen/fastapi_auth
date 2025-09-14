from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr


class AccountBaseShema(BaseModel):
    email: Annotated[str, EmailStr, MinLen(1), MaxLen(255)]


class AccountCreateShema(AccountBaseShema):
    username: Annotated[str, MinLen(1), MaxLen(100)]
    password: Annotated[str, MinLen(1), MaxLen(100)]

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "arsen@gmail.com",
                "password": "arsen2002",
                "username": "arsen",
            }
        }
    }


class AccountLoginShema(AccountBaseShema):
    password: Annotated[str, MinLen(1), MaxLen(100)]
    pass


class AccountReadShema(AccountBaseShema):
    id: int
    username: Annotated[str | None, MinLen(1), MaxLen(100)] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "email": "arsen@gmail.com",
                "username": "arsen",
            }
        },
    }
