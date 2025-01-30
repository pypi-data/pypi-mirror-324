from typing import Union

from .base import MutableSendPulseObjectObject


__all__ = ["Result", "CreateTemplateResult"]


class Result(MutableSendPulseObjectObject):
    result: bool
    id: Union[str, int, None] = None


class CreateTemplateResult(Result):
    real_id: int
