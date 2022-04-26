from typing import List, Optional

from flask_mail import Mail, Message

from extension.mail_client import mail
from extension.project_config import get_config

sender = get_config().MAIL_USERNAME


class OneEmail:
    """
    email
    """

    def __init__(self):
        self.mail: Mail = mail
        self.message: Optional[Message] = None

    def add_message(
        self, subject: str, recipients: List[str], body: str
    ) -> None:
        self.message = Message(
            subject,
            sender=sender,
            recipients=recipients,
            body=body,
            charset='gbk'
        )

    def add_attach(
        self, filename: str, content_type: str, file_path: str
    ) -> None:
        with open(file_path, 'rb') as fp:
            self.message.attach(
                filename=filename, content_type=content_type, data=fp.read()
            )

    def send(self) -> bool:
        # 保持 connect
        self.mail.connect()

        # send
        try:
            self.mail.send(self.message)
        except Exception as ex:
            print(ex)
            return False

        return True
