import datetime as dt
from operator import itemgetter
***REMOVED***
from typing import List

import pandas as pd
***REMOVED***
from rendaino_tombstone.toot import Toot, Visibility

***REMOVED***
SUMFILE = "sum_number_rotated.txt"
round_toots = pd.DataFrame({"username": [], "display_name": [], "created_at": []})
TIME29 = dt.time(17, 29, 0, 0)
TIME30 = dt.time(17, 30, 0, 0)
TIME31 = dt.time(17, 31, 0, 0)
TODAY = dt.date.today()  # 今日の日付
multi_turn = 0

***REMOVED***
    mastodon = Mastodon(
        client_id=PATH + "clientcred.secret",
        access_token=PATH + "usercred.secret",
        api_base_url="https://gensokyo.town",
***REMOVED***


def get_timeline(tl_type: str) -> List[Toot]:
    ***REMOVED***
    タイムラインから2:29分までのtootを集めてくる関数
    tl_typeには取得するタイムラインの種類を渡す。(home, local, public tag/hashtagのいずれか)
    返り値は取得したtootのlist
    ***REMOVED***
    toots = mastodon.timeline(timeline=tl_type, limit=40)
    while True:
        time = dt.time(
            toots[-1]["created_at"].hour,
            toots[-1]["created_at"].minute,
            toots[-1]["created_at"].second,
            toots[-1]["created_at"].microsecond,
    ***REMOVED***
        # 取得したget_toots全てのtootが29分より前の場合終了
        if time < TIME29:
            break
        m_id = toots[-1]["id"] - 1
        toots = toots + mastodon.timeline(timeline=tl_type, max_id=m_id, limit=40)
    toots = sorted(toots, key=itemgetter("created_at"))
    typed_toots = [Toot(**toot) for toot in toots]
    return typed_toots


def select_toots(toots: List[Toot]) -> pd.DataFrame:
    ***REMOVED***
    取得したtootのリストから必要なtootを抜き出し、
    必要な要素のラベルで構成されたDataFrameに落とし込む
    ***REMOVED***
    round_toots = pd.DataFrame({"username": [], "display_name": [], "created_at": []})
    for toot in toots:
        time = dt.time(
            toot.created_at.hour,
            toot.created_at.minute,
            toot.created_at.second,
            toot.created_at.microsecond,
    ***REMOVED***
        if TIME29 <= time and time < TIME31:
            if "ｽﾞｽﾞｽﾞ" in toot.content or "ズズズ" in toot.content or "ずずず" in toot.content:
                round_toots = round_toots.append(
                    pd.DataFrame(
                        {
                            "username": [toot.account["username"]],
                            "display_name": [toot.account["display_name"]],
                            "created_at": [time],
                        }
                ***REMOVED***
            ***REMOVED***
    return round_toots


def count_rotation(rotation_count: int) -> str:
    ***REMOVED***
    回転数についての文を作る。
    ***REMOVED***
    toot = ""
    if rotation_count >= 4:
        # 分数表記の判定
        if (rotation_count % 4) == 0:
            toot += str(int(rotation_count / 4)) + "回転です。"
        elif (rotation_count % 4) == 2:
            toot += str(int(rotation_count / 4)) + "と2分の1回転です。"
        else:
            toot += str(int(rotation_count / 4)) + "と4分の" + str(rotation_count % 4) + "回転です。"
    else:
        # 分数表記の判定
        if (rotation_count % 4) == 0:
            toot += "0回転です。"
        elif (rotation_count % 4) == 2:
            toot += "2分の1回転です。"
        else:
            toot += "4分の" + str(rotation_count % 4) + "回転です。"
    return toot


def sum_number_rotated(participation: int) -> str:
    ***REMOVED***
    合計の回転数
    ***REMOVED***
    # 今までの回転数に今回の回転数を足して保存
    with open(PATH + SUMFILE, "r") as f:
        sum_num_rotated = int(f.read()) + participation
    with open(PATH + SUMFILE, "w") as f:
        f.write(str(sum_num_rotated))

    toot = "\n今日までの回転の合計数は"
    toot += count_rotation(sum_num_rotated)
    return toot


def toot_number_rotated(participation: int, early_parti: int, multi_turn: int***REMOVED***
    # 回転の有無の判定
    if participation == 0:
        post = str(TODAY.month) + "月" + str(TODAY.day) + "日の墓石は回転しませんでした。"
    else:
        post = str(TODAY.month) + "月" + str(TODAY.day) + "日の墓石の回転は" + str(participation) + "人による"
        # 回転数を文章に書き起こす
        post += count_rotation(participation)
        # 早回し判定
        if early_parti > 0:
            post += "\nまた、2時30分になる前に回した人は" + str(early_parti) + "人"
            if multi_turn > 0:
                post += "、2度以上回した人は" + str(multi_turn) + "人"
            post += "です。"
        else:
            if multi_turn > 0:
                post += "2度以上回した人は" + str(multi_turn) + "人です。"

    # 合計回転数のカウント
    post += sum_number_rotated(participation)
    mastodon.status_post(status=post)


def toot_ranking(rotated_just: pd.DataFrame***REMOVED***
    ***REMOVED***
    tootのランキングを投稿する
    ***REMOVED***
    post = ""
    temp_time = dt.time(17, 27, 41, 0)
    temp_i = -1
    for i, rank in rotated_just.iterrows():
        # 一個前のtootと時刻が同じだったら順位を一個前のと同じにする
        if rank["created_at"] == temp_time:
            temp = "{}位: {} @{} [02{}]\n".format(
                int(str(temp_i)) + 1,
                rank["display_name"],
                rank["username"],
                str(rank["created_at"])[2:12],
        ***REMOVED***
        else:
            temp = "{}位: {} @{} [02{}]\n".format(
                int(str(i)) + 1,
                rank["display_name"],
                rank["username"],
                str(rank["created_at"])[2:12],
        ***REMOVED***
            temp_time = rank["created_at"]
            temp_i = i
        if len(post) + len(temp) >= 500:
            mastodon.status_post(status=post, visibility="unlisted")
            post = ""
        post += temp
    mastodon.status_post(status=post, visibility="unlisted")


***REMOVED***
    # LTL
    # tootの取得
    toots = get_timeline(tl_type="local")
    # データの整形とズズズだけ拾う
    round_toots = select_toots(toots=toots)

    # 複数回回した人を数える
    for i in round_toots["username"].value_counts():
        if i > 1:
            multi_turn += 1

    # 人数のダブりを削る
    round_toots = round_toots.drop_duplicates(["username"])
    round_toots = round_toots.reset_index(drop=True)

    # 30分よりまえ、以降で回した人に分ける
    rotated_early = round_toots[round_toots.created_at < TIME30]
    rotated_just = round_toots[round_toots.created_at >= TIME30]
    rotated_just = rotated_just.reset_index(drop=True)
    participation = int(len(round_toots.index))  # 参加者人数
    early_parti = int(len(rotated_early.index))

    # 回転数についてtootする
    toot_number_rotated(participation=participation, early_parti=early_parti, multi_turn=multi_turn)

    # ランキング表記
    if participation > 0:
        toot_ranking(rotated_just=rotated_just)

    # 早回し表記
    if early_parti > 0:
        post = "2時30分より前に回したtootです。\n"
        for rank in rotated_early.itertuples(index=False):
            temp = (
                rank.display_name
                + " @"
                + rank.username
                + " [02"
                + str(rank.created_at)[2:12]
                + "]\n"
        ***REMOVED***
            if len(post) + len(temp) >= 500:
                mastodon.status_post(status=post, visibility="unlisted")
                post = "2時30分より前に回したtoot、続き。\n"
            post += temp
        mastodon.status_post(status=post, visibility="unlisted")

    # HTL用
    round_toots = pd.DataFrame({"username": [], "display_name": [], "created_at": []})
    toots = get_timeline(tl_type="home")

    ***REMOVED***
    取得したtootのリストから必要なtootを抜き出し、
    必要な要素のラベルで構成されたDataFrameに落とし込む
    ***REMOVED***
    for toot in toots:
        time = dt.time(
            toot.created_at.hour,
            toot.created_at.minute,
            toot.created_at.second,
            toot.created_at.microsecond,
    ***REMOVED***
        if TIME29 <= time and time <= TIME31:
            if Visibility.public != toot.visibility:
                if "ｽﾞｽﾞｽﾞ" in toot.content or "ズズズ" in toot.content or "ずずず" in toot.content:
                    round_toots = round_toots.append(
                        pd.DataFrame(
                            {
                                "username": [toot.account.username],
                                "display_name": [toot.account.display_name],
                                "created_at": [time],
                            }
                    ***REMOVED***
                ***REMOVED***

    # 人数のダブりを削る
    round_toots = round_toots.drop_duplicates(["username"])
    round_toots = round_toots.reset_index(drop=True)
    participation = int(len(round_toots.index))  # 参加者人数

    # 時刻報告
    if participation > 0:
        post = ""
        for rank in round_toots.itertuples(index=False):
            post = (
                "@"
                + rank.username
                + " "
                + rank.display_name
                + " [02"
                + str(rank.created_at)[2:12]
                + "]\n"
        ***REMOVED***
            mastodon.status_post(status=post, visibility="direct")
            post = ""
