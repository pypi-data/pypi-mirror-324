from typing import Union

from aiosendpulse.methods.email.templates import CreateTemplate, EditTemplate, GetTemplate
from aiosendpulse.services.base import BaseService
from aiosendpulse.types import CreateTemplateResult, Result, Template


__all__ = ["TemplateService"]


class TemplateService(BaseService):
    async def create(self, html: str, lang: str, name: str = None) -> CreateTemplateResult:
        return await CreateTemplate(
            name=name,
            body=html,
            lang=lang,  # noqa
        )(client=self.http_client, auth=self.auth)

    async def edit(self, template_id: Union[str, int], html: str) -> Result:
        return await EditTemplate(
            id=template_id,
            body=html,
        )(client=self.http_client, auth=self.auth)

    async def get(self, template_id: Union[str, int]) -> Template:
        return await GetTemplate(
            template_id=template_id,
        )(client=self.http_client, auth=self.auth)
