import datetime as dt
from typing import Literal


def get_timeline(tl_type: Literal["home", "local", "public"]) -> list[Toot]:
    """
    タイムラインから2:29分までのtootを集めてくる関数
    tl_typeには取得するタイムラインの種類を渡す。(home, local, public tag/hashtagのいずれか)
    返り値は取得したtootのlist
    """
    toots: list[Toot] = []
    while True:
        get_toots = mastodon.timeline(timeline=tl_type, limit=40)
        time = dt.datetime(
            toots[-1]["created_at"].year,
            toots[-1]["created_at"].month,
            toots[-1]["created_at"].day,
            toots[-1]["created_at"].hour,
            toots[-1]["created_at"].minute,
            toots[-1]["created_at"].second,
            toots[-1]["created_at"].microsecond,
        )
        # 取得したget_toots全てのtootが29分より前の場合終了
        if time < TIME29:
            break
        m_id = toots[-1]["id"] - 1
        toots = toots + mastodon.timeline(timeline=tl_type, max_id=m_id, limit=40)
    toots = sorted(toots, key=itemgetter("created_at"))
    return toots


def select_toots(toots) -> pd.DataFrame:
    """
    取得したtootのリストから必要なtootを抜き出し、
    必要な要素のラベルで構成されたDataFrameに落とし込む
    """
    round_toots = pd.DataFrame({"username": [], "display_name": [], "created_at": []})
    for toot in toots:
        time = dt.time(
            toot["created_at"].hour,
            toot["created_at"].minute,
            toot["created_at"].second,
            toot["created_at"].microsecond,
        )
        if TIME29 <= time and time < TIME31:
            if "ｽﾞｽﾞｽﾞ" in toot["content"] or "ズズズ" in toot["content"] or "ずずず" in toot["content"]:
                round_toots = pd.concat(
                    [
                        round_toots,
                        pd.DataFrame(
                            {
                                "username": [toot["account"]["username"]],
                                "display_name": [toot["account"]["display_name"]],
                                "created_at": [time],
                            }
                        ),
                    ]
                )
    return round_toots
