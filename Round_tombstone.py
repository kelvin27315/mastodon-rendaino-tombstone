# -*- coding: utf-8 -*-

***REMOVED***
import datetime as dt
import pandas as pd

***REMOVED***
    #変数初期化
    mastodon = Mastodon(
            client_id="clientcred.secret",
            access_token="usercred.secret",
            api_base_url = "https://gensokyo.cloud")
round_toots = pd.DataFrame({"username":[],"display_name":[],"created_at":[]})
TIME29 = dt.time(17,29,0,0)
TIME30 = dt.time(17,30,0,0)
TIME31 = dt.time(17,31,0,0)
TODAY = dt.date.today() #今日の日付
multi_turn = 0


def get_timeline(tl_type):
    ***REMOVED***
    タイムラインから2:29分までのtootを集めてくる関数
    tl_typeには取得するタイムラインの種類を渡す。(home, local, public tag/hashtagのいずれか)
    返り値は取得したtootのlist
    ***REMOVED***
    toots = mastodon.timeline(timeline = tl_type, limit = 40)
    while True:
        time = dt.time(
            int(toots[-1]["created_at"][11:13]), int(toots[-1]["created_at"][14:16]),
            int(toots[-1]["created_at"][17:19]), int(toots[-1]["created_at"][20:23])*1000)
        #取得したget_toots全てのtootが29分より前の場合終了
        if time <= TIME29:
            break
        m_id = toots[-1]["id"] -1
        toots = toots + mastodon.timeline(timeline = tl_type, max_id = m_id, limit = 40)
    toots = sorted(toots, key=lambda x:x['id'])
    return (toots)

def select_toots(toots):
    ***REMOVED***
    取得したtootのリストから必要なtootを抜き出し、
    必要な要素のラベルで構成されたDataFrameに落とし込む
    ***REMOVED***
    round_toots = pd.DataFrame({"username":[],"display_name":[],"created_at":[]})
    for toot in toots:
        time = dt.time(
            int(toot["created_at"][11:13]), int(toot["created_at"][14:16]),
            int(toot["created_at"][17:19]), int(toot["created_at"][20:23])*1000)
        if TIME29 <= time and time <= TIME31:
            if "ｽﾞｽﾞｽﾞ" in toot["content"] or "ズズズ" in toot["content"] or "ずずず" in toot["content"]:
                round_toots = round_toots.append(pd.DataFrame({
                    "username":[toot["account"]["username"]],
                    "display_name":[toot["account"]["display_name"]],
                    "created_at":[time]}))
    return (round_toots)

def toot_number_rotated(participation, early_parti, multi_turn):
    #回転の有無の判定
    if participation == 0:
        toot = (str(TODAY.month) + '月' + str(TODAY.day) + "日の墓石は回転しませんでした。")
    else:
        toot = (str(TODAY.month) + '月' + str(TODAY.day) + "日の墓石の回転は" + str(participation) + "人による")
        #一回転以上したかの判定
        if participation >= 4:
            #分数表記の判定
            if (participation % 4) == 0:
                toot += str(int(participation / 4)) + "回転でした。"
            elif (participation % 4) == 2:
                toot += str(int(participation / 4)) + "と2分の" + str(int((participation % 4) / 2)) + "回転でした。"
            else:
                toot += str(int(participation / 4)) + "と4分の" + str(participation % 4) + "回転でした。"
        else:
            #分数表記の判定
            if (participation % 4) == 2:
                toot += str(int(participation / 4)) + "2分の" + str(int((participation % 4) / 2)) + "回転でした。"
            else:
                toot += str(int(participation / 4)) + "4分の" + str(participation % 4) + "回転でした。"
        #早回し判定
        if early_parti > 0:
            toot += "\nまた、2時30分になる前に回した人は" + str(early_parti) + "人"
            if multi_turn > 0:
                toot += "、2度以上回した人は" + str(multi_turn) + "人"
            toot += "です。"
        else:
            if multi_turn > 0:
                toot += "2度以上回した人は" + str(multi_turn) + "人です。"
    mastodon.toot(toot)

***REMOVED***
    #LTL
    #tootの取得
    toots = get_timeline(tl_type = "local")
    #データの整形
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
    #round_toots = select_toots(toots = toots)
    
    ***REMOVED***
    取得したtootのリストから必要なtootを抜き出し、
    必要な要素のラベルで構成されたDataFrameに落とし込む
    ***REMOVED***
    for toot in toots:
        time = dt.time(
            int(toot["created_at"][11:13]), int(toot["created_at"][14:16]),
            int(toot["created_at"][17:19]), int(toot["created_at"][20:23])*1000)
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
