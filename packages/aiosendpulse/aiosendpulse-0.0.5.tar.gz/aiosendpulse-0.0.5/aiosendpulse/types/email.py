from typing import Union

from pydantic import EmailStr

from .base import SendPulseObject


__all__ = ["EmailDetail"]


class EmailDetail(SendPulseObject):
    email: EmailStr
    status: Union[int, None] = None
    status_explain: Union[str, None] = None
    variables: Union[dict[str, str], None] = None
