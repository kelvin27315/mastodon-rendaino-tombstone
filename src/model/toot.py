from mastodon.types import Status
from datetime import datetime

@dataclass
class Toot:
    created_at: datetime
    content: str
    username: str
    display_name: str


def to_toot(toot: Status) -> Toot:
    return Toot(
        created_at = toot["created_at"],
        content = toot["content"],
        username = toot["account"]["username"],
        display_name = toot["account"]["display_name"]
    )
