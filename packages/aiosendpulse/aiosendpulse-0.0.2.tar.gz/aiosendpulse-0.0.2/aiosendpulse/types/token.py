from pydantic import SecretStr

from .base import MutableSendPulseObjectObject


__all__ = ["Token"]


class Token(MutableSendPulseObjectObject):
    access_token: SecretStr
    token_type: str
    expires_in: int
