from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Transaction(_message.Message):
    __slots__ = ("bid_uuid", "bid_created_at", "bid_price", "bid_krw", "bid_fee", "bid_failed", "ask_failed", "order_status", "tether_volume", "bid_filled_at", "ask_uuid", "ask_created_at", "ask_filled_at", "ask_price", "ask_fee", "revenue")
    BID_UUID_FIELD_NUMBER: _ClassVar[int]
    BID_CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    BID_PRICE_FIELD_NUMBER: _ClassVar[int]
    BID_KRW_FIELD_NUMBER: _ClassVar[int]
    BID_FEE_FIELD_NUMBER: _ClassVar[int]
    BID_FAILED_FIELD_NUMBER: _ClassVar[int]
    ASK_FAILED_FIELD_NUMBER: _ClassVar[int]
    ORDER_STATUS_FIELD_NUMBER: _ClassVar[int]
    TETHER_VOLUME_FIELD_NUMBER: _ClassVar[int]
    BID_FILLED_AT_FIELD_NUMBER: _ClassVar[int]
    ASK_UUID_FIELD_NUMBER: _ClassVar[int]
    ASK_CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    ASK_FILLED_AT_FIELD_NUMBER: _ClassVar[int]
    ASK_PRICE_FIELD_NUMBER: _ClassVar[int]
    ASK_FEE_FIELD_NUMBER: _ClassVar[int]
    REVENUE_FIELD_NUMBER: _ClassVar[int]
    bid_uuid: str
    bid_created_at: str
    bid_price: float
    bid_krw: float
    bid_fee: float
    bid_failed: int
    ask_failed: int
    order_status: int
    tether_volume: float
    bid_filled_at: str
    ask_uuid: str
    ask_created_at: str
    ask_filled_at: str
    ask_price: float
    ask_fee: str
    revenue: str
    def __init__(self, bid_uuid: _Optional[str] = ..., bid_created_at: _Optional[str] = ..., bid_price: _Optional[float] = ..., bid_krw: _Optional[float] = ..., bid_fee: _Optional[float] = ..., bid_failed: _Optional[int] = ..., ask_failed: _Optional[int] = ..., order_status: _Optional[int] = ..., tether_volume: _Optional[float] = ..., bid_filled_at: _Optional[str] = ..., ask_uuid: _Optional[str] = ..., ask_created_at: _Optional[str] = ..., ask_filled_at: _Optional[str] = ..., ask_price: _Optional[float] = ..., ask_fee: _Optional[str] = ..., revenue: _Optional[str] = ...) -> None: ...

class TransactionRequest(_message.Message):
    __slots__ = ("db_auth", "bot_name")
    DB_AUTH_FIELD_NUMBER: _ClassVar[int]
    BOT_NAME_FIELD_NUMBER: _ClassVar[int]
    db_auth: str
    bot_name: str
    def __init__(self, db_auth: _Optional[str] = ..., bot_name: _Optional[str] = ...) -> None: ...

class ScopedTransactionRequest(_message.Message):
    __slots__ = ("db_auth", "start_time", "end_time")
    DB_AUTH_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    db_auth: str
    start_time: int
    end_time: int
    def __init__(self, db_auth: _Optional[str] = ..., start_time: _Optional[int] = ..., end_time: _Optional[int] = ...) -> None: ...

class TransactionsResponse(_message.Message):
    __slots__ = ("transactions",)
    TRANSACTIONS_FIELD_NUMBER: _ClassVar[int]
    transactions: _containers.RepeatedCompositeFieldContainer[Transaction]
    def __init__(self, transactions: _Optional[_Iterable[_Union[Transaction, _Mapping]]] = ...) -> None: ...

class DBCommitResponse(_message.Message):
    __slots__ = ("status_code", "message")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    message: str
    def __init__(self, status_code: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class BidPlaceRequest(_message.Message):
    __slots__ = ("db_auth", "bid_uuid", "bid_price", "tether_volume")
    DB_AUTH_FIELD_NUMBER: _ClassVar[int]
    BID_UUID_FIELD_NUMBER: _ClassVar[int]
    BID_PRICE_FIELD_NUMBER: _ClassVar[int]
    TETHER_VOLUME_FIELD_NUMBER: _ClassVar[int]
    db_auth: str
    bid_uuid: str
    bid_price: float
    tether_volume: float
    def __init__(self, db_auth: _Optional[str] = ..., bid_uuid: _Optional[str] = ..., bid_price: _Optional[float] = ..., tether_volume: _Optional[float] = ...) -> None: ...

class BidFillRequest(_message.Message):
    __slots__ = ("db_auth", "bid_uuid")
    DB_AUTH_FIELD_NUMBER: _ClassVar[int]
    BID_UUID_FIELD_NUMBER: _ClassVar[int]
    db_auth: str
    bid_uuid: str
    def __init__(self, db_auth: _Optional[str] = ..., bid_uuid: _Optional[str] = ...) -> None: ...

class AskPlaceRequest(_message.Message):
    __slots__ = ("db_auth", "bid_uuid", "ask_uuid", "ask_price")
    DB_AUTH_FIELD_NUMBER: _ClassVar[int]
    BID_UUID_FIELD_NUMBER: _ClassVar[int]
    ASK_UUID_FIELD_NUMBER: _ClassVar[int]
    ASK_PRICE_FIELD_NUMBER: _ClassVar[int]
    db_auth: str
    bid_uuid: str
    ask_uuid: str
    ask_price: float
    def __init__(self, db_auth: _Optional[str] = ..., bid_uuid: _Optional[str] = ..., ask_uuid: _Optional[str] = ..., ask_price: _Optional[float] = ...) -> None: ...

class AskFillRequest(_message.Message):
    __slots__ = ("db_auth", "ask_uuid", "ask_fee")
    DB_AUTH_FIELD_NUMBER: _ClassVar[int]
    ASK_UUID_FIELD_NUMBER: _ClassVar[int]
    ASK_FEE_FIELD_NUMBER: _ClassVar[int]
    db_auth: str
    ask_uuid: str
    ask_fee: str
    def __init__(self, db_auth: _Optional[str] = ..., ask_uuid: _Optional[str] = ..., ask_fee: _Optional[str] = ...) -> None: ...

class UuidRequest(_message.Message):
    __slots__ = ("db_auth", "uuid")
    DB_AUTH_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    db_auth: str
    uuid: str
    def __init__(self, db_auth: _Optional[str] = ..., uuid: _Optional[str] = ...) -> None: ...
