from dataclasses import dataclass

from typing import List, Optional
from datetime import datetime


@dataclass
class MessageCreateV1:
    text: str

    def __post_init__(self):
        if not isinstance(self.text, str):
            error = "Text must be of type <str>"
            raise ValueError(error)

        self.text = self.text.strip()

        if not self.text:
            error = "Text cannot be empty"
            raise ValueError(error)


@dataclass
class MessageResponseV1:
    id: int
    text: str


@dataclass
class MessageFoundV1:
    found: bool


@dataclass
class UserCreateV1:
    user_id: int
    message: MessageCreateV1
    ban_reason: Optional[str] | None = None
    additional_info: Optional[str] | None = None

    def __post_init__(self):
        errors = []
        if not isinstance(self.user_id, int):
            errors.append("User_id must be of type <int>")
        if not isinstance(self.message, MessageCreateV1):
            errors.append("Message must be of type <MessageCreateV1>")
        if self.ban_reason and not isinstance(self.ban_reason, str):
            errors.append("Ban_reason must be of type <str>")
        if self.additional_info and not isinstance(self.additional_info, str):
            errors.append("Additional_info must be of type <str>")

        if errors:
            errors = "\n\nThe following errors occurred:\n" + "\n".join(errors)
            raise ValueError(errors)

        self.ban_reason = self.ban_reason.strip() if self.ban_reason else None
        self.additional_info = (self.additional_info.strip()
                                if self.additional_info else None)


@dataclass
class UserResponseBaseV1:
    user_id: int
    ban_reason: str
    additional_info: str
    utc_created_at: datetime
    utc_created_at_formatted: str

    def __post_init__(self):
        self.utc_created_at = datetime.fromtimestamp(self.utc_created_at)  # noqa


@dataclass
class UserResponseV1(UserResponseBaseV1):
    message: MessageResponseV1

    def __post_init__(self):
        super().__post_init__()
        self.message = MessageResponseV1(**self.message.__dict__)


@dataclass
class UserResponseMessagesV1(UserResponseBaseV1):
    messages: List[MessageResponseV1]

    def __post_init__(self):
        super().__post_init__()
        self.messages = [MessageResponseV1(**message)  # noqa
                         for message in self.messages]


@dataclass
class UserFoundV1:
    found: bool
    user: Optional[UserResponseMessagesV1] | None = None

    def __post_init__(self):
        if self.user:
            self.user = UserResponseMessagesV1(**self.user)  # noqa
