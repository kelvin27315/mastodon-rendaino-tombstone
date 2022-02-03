from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, List, Optional


@dataclass
class Field:
    name: str
    value: str
    verified_at: Optional[str]


@dataclass
class Account:
    id: int
    username: str
    display_name: str
    acct: str = ""
    locked: bool = False
    bot: bool = False
    discoverable: bool = True
    group: bool = False
    created_at: datetime = datetime(2000, 1, 1, 0, 0, 0, 0, timezone.utc)
    note: str = ""
    url: str = ""
    avatar: str = ""
    avatar_static: str = ""
    header: str = ""
    header_static: str = ""
    followers_count: int = 0
    following_count: int = 0
    statuses_count: int = 0
    last_status_at: datetime = datetime(2000, 1, 1, 0, 0, 0, 0, timezone.utc)
    emojis: List[Any] = field(default_factory=list)
    fields: List[Field] = field(default_factory=list)
