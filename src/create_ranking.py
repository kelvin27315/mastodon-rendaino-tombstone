def toot_ranking(rotated_just) -> None:
    """
    tootのランキングを投稿する
    """
    toot = ""
    temp_time = dt.time(17, 27, 41, 0)
    temp_i = -1
    for i, rank in rotated_just.iterrows():
        # 一個前のtootと時刻が同じだったら順位を一個前のと同じにする
        if rank["created_at"] == temp_time:
            temp = (
                str(int(str(temp_i)) + 1)
                + "位: "
                + rank["display_name"]
                + " @"
                + rank["username"]
                + " [02"
                + str(rank["created_at"])[2:12]
                + "]\n"
            )
        else:
            temp = (
                str(int(str(i)) + 1)
                + "位: "
                + rank["display_name"]
                + " @"
                + rank["username"]
                + " [02"
                + str(rank["created_at"])[2:12]
                + "]\n"
            )
            temp_time = rank["created_at"]
            temp_i = i
        if len(toot) + len(temp) >= 500:
            mastodon.status_post(status=toot, visibility="unlisted")
            toot = ""
        toot += temp
    mastodon.status_post(status=toot, visibility="unlisted")
