from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Account(_message.Message):
    __slots__ = ("id", "account_title", "created_at", "activated", "balance")
    ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_TITLE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    ACTIVATED_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    id: int
    account_title: str
    created_at: int
    activated: bool
    balance: float
    def __init__(self, id: _Optional[int] = ..., account_title: _Optional[str] = ..., created_at: _Optional[int] = ..., activated: bool = ..., balance: _Optional[float] = ...) -> None: ...
