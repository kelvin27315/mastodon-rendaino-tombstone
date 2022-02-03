from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, List, Optional

from rendaino_tombstone.account import Account


class Visibility(Enum):
    public = "public"
    unlisted = "unlisted"
    private = "private"
    direct = "direct"


@dataclass
class Toot:
    id: int
    created_at: datetime
    content: str
    account: Account
    in_reply_to_id: Optional[Any] = None
    in_reply_to_account_id: Optional[Any] = None
    sensitive: bool = False
    spoiler_text: str = ""
    visibility: Visibility = Visibility.public
    language: str = "ja"
    uri: str = ""
    url: str = ""
    replies_count: int = 0
    reblogs_count: int = 0
    favourited: bool = False
    reblogged: bool = False
    muted: bool = False
    bookmarked: bool = False
    reblog: Optional[Any] = None
    application: Optional[Any] = None
    media_attachments: List[Any] = field(default_factory=list)
    mentions: List[Any] = field(default_factory=list)
    tags: List[Any] = field(default_factory=list)
    emojis: List[Any] = field(default_factory=list)
    card: Optional[Any] = None
    poll: Optional[Any] = None
