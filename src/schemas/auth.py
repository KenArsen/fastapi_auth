from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr


class AccountBaseSchema(BaseModel):
    email: Annotated[str, EmailStr, MinLen(1), MaxLen(255)]


class AccountCreateSchema(AccountBaseSchema):
    username: str | None = None
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


class AccountLoginSchema(AccountBaseSchema):
    password: Annotated[str, MinLen(1), MaxLen(100)]

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "arsen@gmail.com",
                "password": "arsen2002",
            }
        }
    }


class AccountReadSchema(AccountBaseSchema):
    id: int
    username: str | None = None

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
