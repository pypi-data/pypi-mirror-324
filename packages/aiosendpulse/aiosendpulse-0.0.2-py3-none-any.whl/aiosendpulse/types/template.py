from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Union

from pydantic import HttpUrl
from pydantic_extra_types.language_code import LanguageAlpha2

from .base import MutableSendPulseObjectObject


if TYPE_CHECKING:
    from .template_category import TemplateCategory


__all__ = ["Template"]


class Template(MutableSendPulseObjectObject):
    id: str
    real_id: int
    lang: LanguageAlpha2
    name: str
    name_slug: Union[str, None] = None
    created: datetime
    full_description: Union[str, None] = None
    is_structured: bool
    category: str
    category_info: TemplateCategory
    tags: dict[str, str] = {}
    owner: str
    preview: HttpUrl
