from .api_versions.v1 import (
    YOASAPIWrapperV1,
    MessageCreateV1, MessageResponseV1, MessageFoundV1,
    UserCreateV1, UserResponseV1, UserResponseMessagesV1, UserFoundV1
)

__all__ = [
    "YOASAPIWrapperLatest",
    "MessageCreateLatest", "MessageResponseLatest", "MessageFoundLatest",
    "UserCreateLatest", "UserResponseLatest", "UserResponseMessagesLatest",
    "UserFoundLatest",
    "YOASAPIWrapperV1",
    "MessageCreateV1", "MessageResponseV1", "MessageFoundV1",
    "UserCreateV1", "UserResponseV1", "UserResponseMessagesV1", "UserFoundV1"
]
__version__ = "1.0.0"

YOASAPIWrapperLatest = YOASAPIWrapperV1

MessageCreateLatest = MessageCreateV1
MessageResponseLatest = MessageResponseV1
MessageFoundLatest = MessageFoundV1

UserCreateLatest = UserCreateV1
UserResponseLatest = UserResponseV1
UserResponseMessagesLatest = UserResponseMessagesV1
UserFoundLatest = UserFoundV1
