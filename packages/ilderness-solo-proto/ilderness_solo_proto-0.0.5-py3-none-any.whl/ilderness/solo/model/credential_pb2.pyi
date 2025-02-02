from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Credential(_message.Message):
    __slots__ = ("username", "password", "auth_token")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    AUTH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    username: str
    password: str
    auth_token: str
    def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ..., auth_token: _Optional[str] = ...) -> None: ...
