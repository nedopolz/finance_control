from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class UserCreatedMessage(_message.Message):
    __slots__ = ["email", "externalID", "username"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    EXTERNALID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    email: str
    externalID: str
    username: str
    def __init__(self, externalID: _Optional[str] = ..., email: _Optional[str] = ..., username: _Optional[str] = ...) -> None: ...
