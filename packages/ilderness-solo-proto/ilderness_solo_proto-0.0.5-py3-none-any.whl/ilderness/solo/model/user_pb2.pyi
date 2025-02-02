from ilderness.solo.model import account_pb2 as _account_pb2
from ilderness.solo.model import credential_pb2 as _credential_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class User(_message.Message):
    __slots__ = ("id", "credentials", "phone_number", "email", "createdAt", "accounts")
    ID_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    PHONE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    CREATEDAT_FIELD_NUMBER: _ClassVar[int]
    ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    id: int
    credentials: _credential_pb2.Credential
    phone_number: str
    email: str
    createdAt: int
    accounts: _containers.RepeatedCompositeFieldContainer[_account_pb2.Account]
    def __init__(self, id: _Optional[int] = ..., credentials: _Optional[_Union[_credential_pb2.Credential, _Mapping]] = ..., phone_number: _Optional[str] = ..., email: _Optional[str] = ..., createdAt: _Optional[int] = ..., accounts: _Optional[_Iterable[_Union[_account_pb2.Account, _Mapping]]] = ...) -> None: ...
