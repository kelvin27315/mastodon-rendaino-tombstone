from dataclasses import dataclass
from datetime import datetime
from typing import List, Any, Optional


@dataclass
class Field:
    name: str
    value: str
    verified_at: Optional[str]

@dataclass
class Account:
    id: int
    username: str
    acct: str
    display_name: str
    locked: bool
    bot: bool
    discoverable: bool
    group: bool
    created_at: datetime
    note: str
    url: str
    avatar: str
    avatar_static: str
    header: str
    header_static: str
    followers_count: int
    following_count: int
    statuses_count: int
    last_status_at: datetime
    emojis: List[Any]
    fields: List[Field]

