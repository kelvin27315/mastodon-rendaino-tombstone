from dataclasses import dataclass
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
    in_reply_to_id: Optional[Any]
    in_reply_to_account_id: Optional[Any]
    sensitive: bool
    spoiler_text: str
    visibility: Visibility
    language: str
    uri: str
    url: str
    replies_count: int
    reblogs_count: int
    favourited: bool
    reblogged: bool
    muted: bool
    bookmarked: bool
    content: str
    reblog: Optional[Any]
    application: Optional[Any]
    account: Account
    media_attachments: List[Any]
    mentions: List[Any]
    tags: List[Any]
    emojis: List[Any]
    card: Optional[Any]
    poll: Optional[Any]

