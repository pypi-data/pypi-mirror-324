from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Position(_message.Message):
    __slots__ = ("timestamp", "bid_order_uuid", "entry_price", "volume", "ask_order_uuid", "created_at", "target_price")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    BID_ORDER_UUID_FIELD_NUMBER: _ClassVar[int]
    ENTRY_PRICE_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    ASK_ORDER_UUID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    TARGET_PRICE_FIELD_NUMBER: _ClassVar[int]
    timestamp: int
    bid_order_uuid: str
    entry_price: float
    volume: float
    ask_order_uuid: str
    created_at: str
    target_price: float
    def __init__(self, timestamp: _Optional[int] = ..., bid_order_uuid: _Optional[str] = ..., entry_price: _Optional[float] = ..., volume: _Optional[float] = ..., ask_order_uuid: _Optional[str] = ..., created_at: _Optional[str] = ..., target_price: _Optional[float] = ...) -> None: ...

class KeyRequest(_message.Message):
    __slots__ = ("db_auth",)
    DB_AUTH_FIELD_NUMBER: _ClassVar[int]
    db_auth: str
    def __init__(self, db_auth: _Optional[str] = ...) -> None: ...

class KeyResponse(_message.Message):
    __slots__ = ("status_code", "message")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    message: str
    def __init__(self, status_code: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class BatchPositionsResponse(_message.Message):
    __slots__ = ("batch",)
    BATCH_FIELD_NUMBER: _ClassVar[int]
    batch: _containers.RepeatedCompositeFieldContainer[Position]
    def __init__(self, batch: _Optional[_Iterable[_Union[Position, _Mapping]]] = ...) -> None: ...

class PositionsResponse(_message.Message):
    __slots__ = ("position_idx", "position", "timestamp")
    POSITION_IDX_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    position_idx: int
    position: Position
    timestamp: str
    def __init__(self, position_idx: _Optional[int] = ..., position: _Optional[_Union[Position, _Mapping]] = ..., timestamp: _Optional[str] = ...) -> None: ...

class MarketDataResponse(_message.Message):
    __slots__ = ("price", "timestamp_epoch")
    PRICE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_EPOCH_FIELD_NUMBER: _ClassVar[int]
    price: float
    timestamp_epoch: int
    def __init__(self, price: _Optional[float] = ..., timestamp_epoch: _Optional[int] = ...) -> None: ...
