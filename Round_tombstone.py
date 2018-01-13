from operator import itemgetter
from mastodon import Mastodon
from os import path
import datetime as dt
import pandas as pd

PATH = path.dirname(path.abspath(__file__)) + "/"
SUMFILE = 'sum_number_rotated.txt'
round_toots = pd.DataFrame({"username":[],"display_name":[],"created_at":[]})
TIME29 = dt.time(17,29,0,0)
TIME30 = dt.time(17,30,0,0)
TIME31 = dt.time(17,31,0,0)
TODAY = dt.date.today() #今日の日付
multi_turn = 0

if __name__ == "__main__":
    mastodon = Mastodon(
            client_id = PATH + "clientcred.secret",
            access_token = PATH + "usercred.secret",
            api_base_url = "https://gensokyo.town")

def get_timeline(tl_type):
    """
    タイムラインから2:29分までのtootを集めてくる関数
    tl_typeには取得するタイムラインの種類を渡す。(home, local, public tag/hashtagのいずれか)
    返り値は取得したtootのlist
    """
    toots = mastodon.timeline(timeline = tl_type, limit = 40)
    while True:
        time = dt.time(toots[-1]["created_at"].hour, toots[-1]["created_at"].minute, toots[-1]["created_at"].second, toots[-1]["created_at"].microsecond)
        #取得したget_toots全てのtootが29分より前の場合終了
        if time < TIME29:
            break
        m_id = toots[-1]["id"] -1
        toots = toots + mastodon.timeline(timeline = tl_type, max_id = m_id, limit = 40)
    toots = sorted(toots, key=itemgetter("created_at"))
    return (toots)

def select_toots(toots):
    """
    取得したtootのリストから必要なtootを抜き出し、
    必要な要素のラベルで構成されたDataFrameに落とし込む
    """
    round_toots = pd.DataFrame({"username":[],"display_name":[],"created_at":[]})
    for toot in toots:
        time = dt.time(toot["created_at"].hour, toot["created_at"].minute, toot["created_at"].second, toot["created_at"].microsecond)
        if TIME29 <= time and time < TIME31:
            if "ｽﾞｽﾞｽﾞ" in toot["content"] or "ズズズ" in toot["content"] or "ずずず" in toot["content"]:
                round_toots = round_toots.append(pd.DataFrame({
                    "username":[toot["account"]["username"]],
                    "display_name":[toot["account"]["display_name"]],
                    "created_at":[time]}))
    return (round_toots)

def count_rotation(rotation_count):
    """
    回転数についての文を作る。
    """
    toot = ""
    if rotation_count >= 4:
        #分数表記の判定
        if (rotation_count % 4) == 0:
            toot += str(int(rotation_count / 4)) + "回転です。"
        elif (rotation_count % 4) == 2:
            toot += str(int(rotation_count / 4)) + "と2分の1回転です。"
        else:
            toot += str(int(rotation_count / 4)) + "と4分の" + str(rotation_count % 4) + "回転です。"
    else:
        #分数表記の判定
        if (rotation_count % 4) == 0:
            toot += "0回転です。"
        elif (rotation_count % 4) == 2:
            toot += "2分の1回転です。"
        else:
            toot += "4分の" + str(rotation_count % 4) + "回転です。"
    return(toot)

def sum_number_rotated(participation):
    """
    合計の回転数
    """
    #今までの回転数に今回の回転数を足して保存
    with open(PATH + SUMFILE, "r") as f:
        sum_num_rotated = int(f.read()) + participation
    with open(PATH + SUMFILE,"w") as f:
        f.write(str(sum_num_rotated))

    toot = "\n今日までの回転の合計数は"
    toot += count_rotation(sum_num_rotated)
    return(toot)

def toot_number_rotated(participation, early_parti, multi_turn):
    #回転の有無の判定
    if participation == 0:
        toot = (str(TODAY.month) + '月' + str(TODAY.day) + "日の墓石は回転しませんでした。")
    else:
        toot = (str(TODAY.month) + '月' + str(TODAY.day) + "日の墓石の回転は" + str(participation) + "人による")
        #回転数を文章に書き起こす
        toot += count_rotation(participation)
        #早回し判定
        if early_parti > 0:
            toot += "\nまた、2時30分になる前に回した人は" + str(early_parti) + "人"
            if multi_turn > 0:
                toot += "、2度以上回した人は" + str(multi_turn) + "人"
            toot += "です。"
        else:
            if multi_turn > 0:
                toot += "2度以上回した人は" + str(multi_turn) + "人です。"

    #合計回転数のカウント
    toot += sum_number_rotated(participation)
    mastodon.status_post(status = toot)

if __name__ == "__main__":
    #LTL
    #tootの取得
    toots = get_timeline(tl_type = "local")
    #データの整形とズズズだけ拾う
    round_toots = select_toots(toots = toots)

    #複数回回した人を数える
    for i in round_toots["username"].value_counts():
        if i > 1:
            multi_turn += 1

    #人数のダブりを削る
    round_toots = round_toots.drop_duplicates(["username"])
    round_toots = round_toots.reset_index(drop = True)

    #30分よりまえ、以降で回した人に分ける
    rotated_early = round_toots[round_toots.created_at < TIME30]
    rotated_just = round_toots[round_toots.created_at >= TIME30]
    rotated_just = rotated_just.reset_index(drop = True)
    participation = int(len(round_toots.index))    #参加者人数
    early_parti = int(len(rotated_early.index))

    #回転数についてtootする
    toot_number_rotated(participation = participation, early_parti = early_parti, multi_turn = multi_turn)

    #ランキング表記
    if participation > 0:
        toot = ""
        for i,rank in rotated_just.iterrows():
            temp = str(int(str(i))+1) + "位：" + rank["display_name"] + " @" + rank["username"] + " [02" + str(rank["created_at"])[2:12] +"]\n"
            if len(toot) + len(temp) >= 500:
                mastodon.status_post(status = toot, visibility = "unlisted")
                toot = ""
            toot += temp
        mastodon.status_post(status = toot, visibility = "unlisted")

    #早回し表記
    if early_parti > 0:
        toot = "2時30分より前に回したtootです。\n"
        for i,rank in rotated_early.iterrows():
            temp = rank["display_name"] + " @" + rank["username"] + " [02" + str(rank["created_at"])[2:12] +"]\n"
            if len(toot) + len(temp) >= 500:
                mastodon.status_post(status = toot, visibility = "unlisted")
                toot = "2時30分より前に回したtoot、続き。\n"
            toot += temp
        mastodon.status_post(status = toot, visibility = "unlisted")


    #HTL用
    round_toots = pd.DataFrame({"username":[],"display_name":[],"created_at":[]})
    toots = get_timeline(tl_type = "home")


    """
    取得したtootのリストから必要なtootを抜き出し、
    必要な要素のラベルで構成されたDataFrameに落とし込む
    """
    for toot in toots:
        time = dt.time(toot["created_at"].hour, toot["created_at"].minute, toot["created_at"].second, toot["created_at"].microsecond)
        if TIME29 <= time and time <= TIME31:
            if "public" != toot["visibility"]:
                if "ｽﾞｽﾞｽﾞ" in toot["content"] or "ズズズ" in toot["content"] or "ずずず" in toot["content"]:
                    round_toots = round_toots.append(pd.DataFrame({
                        "username":[toot["account"]["username"]],
                        "display_name":[toot["account"]["display_name"]],
                        "created_at":[time]}))


    #人数のダブりを削る
    round_toots = round_toots.drop_duplicates(["username"])
    round_toots = round_toots.reset_index(drop = True)
    participation = int(len(round_toots.index))    #参加者人数

    #時刻報告
    if participation > 0:
        toot = ""
        for i,rank in round_toots.iterrows():
            toot = "@" + rank["username"] + " " + rank["display_name"] + " [02" + str(rank["created_at"])[2:12] +"]\n"
            mastodon.status_post(status= toot, visibility = 'direct')
            toot = ""
