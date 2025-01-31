from typing import Union

from aiosendpulse.methods.smtp import SendEmail
from aiosendpulse.services.base import BaseService
from aiosendpulse.types import Recipient, Result, Sender, TemplateMeta


__all__ = ["SmtpService"]


class SmtpService(BaseService):
    async def send_email(
        self,
        subject: str,
        sender: Union[Sender, dict],
        to: list[Union[Recipient, dict]],
        html: Union[str, None] = None,
        text: Union[str, None] = None,
        template: Union[TemplateMeta, dict] = None,
        auto_plain_text: bool = False,
        cc: Union[list[Union[Recipient, dict]], None] = None,
        bcc: Union[list[Union[Recipient, dict]], None] = None,
        attachments: Union[dict[str, str], None] = None,
        attachments_binary: Union[dict[str, str], None] = None,
    ) -> Result:
        return await SendEmail(
            html=html,
            text=text,
            template=template,
            auto_plaint_text=auto_plain_text,
            subject=subject,
            sender=sender,
            to=to,
            cc=cc,
            bcc=bcc,
            attachments=attachments,
            attachments_binary=attachments_binary,
        )(client=self.http_client, auth=self.auth)
