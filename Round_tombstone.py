# -*- coding: utf-8 -*-

***REMOVED***
import datetime as dt
import pandas as pd

#変数初期化
mastodon = Mastodon(
        client_id="clientcred.secret",
        access_token="usercred.secret",
        api_base_url = "https://gensokyo.cloud")
round_toots = pd.DataFrame({"username":[],"display_name":[],"created_at":[]})
time29 = dt.time(17,29,0,0)
time30 = dt.time(17,30,0,0)
time31 = dt.time(17,31,0,0)
today = dt.date.today() #今日の日付
multi_turn = 0
toots = []

#tootの取得
toots = mastodon.timeline_local(limit = 40)
while True:
    time = dt.time(
        int(toots[-1]["created_at"][11:13]), int(toots[-1]["created_at"][14:16]),
        int(toots[-1]["created_at"][17:19]), int(toots[-1]["created_at"][20:23])*1000,)
    #取得したget_toots全てのtootが29分より前の場合終了
    if time <= time29:
        break
    #取得するtootのidを指定
    m_id = toots[-1]["id"] - 1
    s_id = toots[-1]["id"] - 41
    toots = mastodon.timeline_local(max_id = m_id, since_id = s_id) + toots
    toots = sorted(toots, key=lambda x:x['id'])
    toots.reverse()
    #tootが取得できているか確認

#idでソート
toots = sorted(toots, key=lambda x:x['id'])

#tootをDataFrameに落とし込む
for toot in toots:
    time = dt.time(
        int(toot["created_at"][11:13]), int(toot["created_at"][14:16]),
        int(toot["created_at"][17:19]), int(toot["created_at"][20:23])*1000)
    if time29 <= time and time <= time31:
        if "ｽﾞｽﾞｽﾞ" in toot["content"] or "ズズズ" in toot["content"] or "ずずず" in toot["content"]:
            round_toots = round_toots.append(pd.DataFrame({
                "username":[toot["account"]["username"]],
                "display_name":[toot["account"]["display_name"]],
                "created_at":[time]}))

#複数回回した人を数える
for i in round_toots["username"].value_counts():
    if i > 1:
        multi_turn += 1

#人数のダブりを削る
round_toots = round_toots.drop_duplicates(["username"])
round_toots = round_toots.reset_index(drop = True)

#30分よりまえ、以降で回した人に分ける
rotated_early = round_toots[round_toots.created_at < time30]
rotated_just = round_toots[round_toots.created_at >= time30]
rotated_just = rotated_just.reset_index(drop = True)
participation = int(len(round_toots.index))    #参加者人数
early_parti = int(len(rotated_early.index))


#回転の有無の判定
if participation == 0:
    toot = (str(today.month) + '月' + str(today.day) + "日の墓石は回転しませんでした。")
else:
    toot = (str(today.month) + '月' + str(today.day) + "日の墓石の回転は" + str(participation) + "人による")
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

#print(toot)
mastodon.toot(toot)


#ランキング表記
if participation > 0:
    toot = ""
    for i,rank in rotated_just.iterrows():
        temp = str(int(str(i))+1) + "位：" + rank["display_name"] + " @" + rank["username"] + " [02" + str(rank["created_at"])[2:12] +"]\n"
        if len(toot) + len(temp) >= 500:
            #print(toot)
            mastodon.status_post(status = toot, visibility = "unlisted")
            toot = ""
        toot += temp
    #print(toot)
    mastodon.status_post(status = toot, visibility = "unlisted")


#早回し表記
if early_parti > 0:
    toot = "2時30分より前に回したtootです。\n"
    for i,rank in rotated_early.iterrows():
        temp = rank["display_name"] + " @" + rank["username"] + " [02" + str(rank["created_at"])[2:12] +"]\n"
        if len(toot) + len(temp) >= 500:
            #print(toot)
            mastodon.status_post(status = toot, visibility = "unlisted")
            toot = "2時30分より前に回したtoot、続き。\n"
        toot += temp
    #print(toot)
    mastodon.status_post(status = toot, visibility = "unlisted")
