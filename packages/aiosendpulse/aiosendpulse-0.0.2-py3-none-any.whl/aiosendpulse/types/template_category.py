from typing import Union

from .base import MutableSendPulseObjectObject


__all__ = ["TemplateCategory"]


class TemplateCategory(MutableSendPulseObjectObject):
    id: int
    name: str
    meta_description: Union[str, None] = None
    full_description: Union[str, None] = None
    code: str
    sort: int
