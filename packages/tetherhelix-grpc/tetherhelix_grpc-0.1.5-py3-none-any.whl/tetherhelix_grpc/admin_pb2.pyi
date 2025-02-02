from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LoginRequest(_message.Message):
    __slots__ = ("admin_certificate",)
    ADMIN_CERTIFICATE_FIELD_NUMBER: _ClassVar[int]
    admin_certificate: str
    def __init__(self, admin_certificate: _Optional[str] = ...) -> None: ...

class LoginResponse(_message.Message):
    __slots__ = ("success", "message", "db_auth")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DB_AUTH_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    db_auth: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., db_auth: _Optional[str] = ...) -> None: ...
