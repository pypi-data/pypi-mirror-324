import requests
from requests.exceptions import HTTPError, JSONDecodeError

from .dataclasses import (
    MessageCreateV1, MessageResponseV1, MessageFoundV1,
    UserCreateV1, UserResponseV1, UserResponseMessagesV1, UserFoundV1
)

__all__ = [
    "YOASAPIWrapperV1",
    "MessageCreateV1", "MessageResponseV1", "MessageFoundV1",
    "UserCreateV1", "UserResponseV1", "UserResponseMessagesV1", "UserFoundV1"
]
__version__ = "1.0.0"


class YOASAPIWrapperV1:
    def __init__(self, api_server) -> None:
        self.api_server = api_server

        response = requests.get(self.api_server)
        is_welcome_text_right = False
        welcome_text_start = "This is YOAS (Your Own Anti-Spam System) API."

        if response.status_code == 200:

            try:
                response_json = response.json()
            except JSONDecodeError:
                error = "Invalid API server"
                raise ValueError(error)

            is_welcome_text = "welcome_text" in response_json
            if is_welcome_text:
                is_welcome_text_right = response_json[
                    "welcome_text"].startswith(welcome_text_start)

            if not is_welcome_text or not is_welcome_text_right:
                error = "Invalid API server"
                raise ValueError(error)

        elif response.status_code == 404:
            error = "Invalid API server or this endpoint does not exist"
            raise ValueError(error)

        else:
            error = {"code": response.status_code, "response": response.json()}
            raise HTTPError(error)

    def create_user(self, access_key: str, user: UserCreateV1) -> UserResponseV1:
        if not isinstance(access_key, str):
            error = "Access key must be of type <str>"
            raise ValueError(error)
        if not isinstance(user, UserCreateV1):
            error = "User must be of type <UserCreateV1>"
            raise ValueError(error)

        post_data = {
            "user_id": user.user_id,
            "message": user.message.text,
            "ban_reason": user.ban_reason,
            "additional_info": user.additional_info
        }
        response = requests.post(
            f"{self.api_server}/user?access_key={access_key}",
            json=post_data
        )

        if response.status_code == 400:
            error = response.json()["error"]
            raise ValueError(error)
        if response.status_code == 403:
            error = response.json()["error"]
            raise HTTPError(error)
        if response.status_code != 201:
            error = {"code": response.status_code, "response": response.json()}
            raise HTTPError(error)

        response = response.json()
        response["message"] = MessageResponseV1(**response["message"])
        return UserResponseV1(**response)

    def delete_user(self, access_key: str, user_id: int) -> UserFoundV1:
        if not isinstance(access_key, str):
            error = "Access key must be of type <str>"
            raise ValueError(error)
        if not isinstance(user_id, int):
            error = "User id must be of type <int>"
            raise ValueError(error)
        response = requests.delete(
            f"{self.api_server}/user?user_id={user_id}&access_key={access_key}"
        )

        if response.status_code == 400:
            error = response.json()["error"]
            raise ValueError(error)
        if response.status_code == 403:
            error = response.json()["error"]
            raise HTTPError(error)
        if response.status_code == 404:
            error = response.json()["error"]
            raise ValueError(error)
        if response.status_code != 200:
            error = {"code": response.status_code, "response": response.json()}
            raise HTTPError(error)

        return UserFoundV1(**response.json())

    def get_user(self, user_id: int) -> UserFoundV1:
        if not isinstance(user_id, int):
            error = "User id must be of type <int>"
            raise ValueError(error)
        response = requests.get(
            f"{self.api_server}/user?user_id={user_id}"
        )

        if response.status_code == 404:
            return UserFoundV1(**response.json())
        if response.status_code != 200:
            error = {"code": response.status_code, "response": response.json()}
            raise HTTPError(error)

        return UserFoundV1(**response.json())

    def get_message(self, message_text: str) -> MessageFoundV1:
        if not isinstance(message_text, str):
            error = "Message text must be of type <str>"
            raise ValueError(error)
        response = requests.get(
            f"{self.api_server}/message?message_text={message_text}"
        )

        if response.status_code == 404:
            return MessageFoundV1(**response.json())
        if response.status_code != 200:
            error = {"code": response.status_code, "response": response.json()}
            raise HTTPError(error)

        return MessageFoundV1(**response.json())
