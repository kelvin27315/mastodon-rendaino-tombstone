# -*- coding: utf-8 -*-
import unittest
from datetime import date, datetime, time, timezone
from unittest.mock import Mock

import mastodon
import pandas as pd
from rendaino_tombstone import Round_tombstone as rt

TODAY_STR = "{dt.month}月{dt.day}日".format(dt=date.today())
UTC = timezone.utc


class TestRoundTombstone(unittest.TestCase):
    def setUp(self):
        # rt.mastodon をmockするので、元のが定義されていたら退避
        self.original_mastodon = rt.mastodon if hasattr(rt, "mastodon") else None
        rt.mastodon = Mock(spec=mastodon.Mastodon)
        # sum_num_rotatedのためのファイル作成。本番のファイルを書き換えないようにテスト用のファイル名に差し替える
        rt.SUMFILE = "sum_number_rotated_test.txt"
        with open(rt.PATH + rt.SUMFILE, "w") as f:
            f.write("42")

    def tearDown(self):
        rt.mastodon = self.original_mastodon

    def test_get_timeline(self):
        rt.mastodon.timeline.side_effect = [
            # timeline取得 1回目
            [
                {
                    "id": 12,
                    "created_at": datetime(2017, 11, 4, 17, 30, 0, 0, UTC),
                    "content": "コスズ",
                    "account": {
                        "username": "kosuzu",
                        "display_name": "小鈴",
                    },
                },
                {
                    "id": 11,
                    "created_at": datetime(2017, 11, 4, 17, 30, 0, 0, UTC),
                    "content": "ｽﾞｽﾞｽﾞ",
                    "account": {
                        "username": "marisa",
                        "display_name": "魔理沙",
                    },
                },
                {
                    "id": 10,
                    "created_at": datetime(2017, 11, 4, 17, 29, 0, 0, UTC),
                    "content": "ズズズ",
                    "account": {
                        "username": "reimu",
                        "display_name": "霊夢",
                    },
                },
            ],
            # timeline取得 2回目
            [
                {
                    "id": 9,
                    "created_at": datetime(2017, 11, 4, 17, 29, 0, 0, UTC),
                    "content": "ズズズ",
                    "account": {
                        "username": "sanae",
                        "display_name": "早苗",
                    },
                },
                {
                    "id": 8,
                    "created_at": datetime(2017, 11, 4, 17, 28, 0, 0, UTC),
                    "content": "ズズズ",
                    "account": {
                        "username": "sakuya",
                        "display_name": "咲夜",
                    },
                },
            ],
            # timeline取得 3回目。実際には呼ばれない
            [
                {
                    "id": 7,
                    "created_at": datetime(2017, 11, 4, 17, 28, 0, 0, UTC),
                    "content": "ズズズ",
                    "account": {
                        "username": "akyu",
                        "display_name": "阿求",
                    },
                },
            ],
        ]
        results = rt.get_timeline("local")
        # 取得したTLの検証。
        self.assertEqual(
            ["咲夜", "霊夢", "早苗", "小鈴", "魔理沙"], [x["account"]["display_name"] for x in results]
    ***REMOVED***
        # mastodon APIの呼び出し回数検証
        self.assertEqual(2, len(rt.mastodon.timeline.mock_calls))

    def test_select_toots(self):
        toots = [
            # positive
            {
                "id": 10,
                "created_at": datetime(2017, 11, 4, 17, 29, 0, 0, UTC),
                "content": "ズズズ",
                "account": {
                    "username": "reimu",
                    "display_name": "霊夢",
                },
            },
            {
                "id": 11,
                "created_at": datetime(2017, 11, 4, 17, 30, 0, 0, UTC),
                "content": "ｽﾞｽﾞｽﾞ",
                "account": {
                    "username": "marisa",
                    "display_name": "魔理沙",
                },
            },
            # negative
            {
                "id": 12,
                "created_at": datetime(2017, 11, 4, 17, 31, 0, 0, UTC),
                "content": "コスズ",
                "account": {
                    "username": "kosuzu",
                    "display_name": "小鈴",
                },
            },
        ]
        results = rt.select_toots(toots)
        self.assertEqual(["reimu", "marisa"], list(results["username"]))
        self.assertEqual(["霊夢", "魔理沙"], list(results["display_name"]))

    # count_rotationのテスト
    def test_count_rotation_no_participation(self):
        toot = rt.count_rotation(0)
        self.assertEqual("0回転です。", toot)

    def test_count_rotation_1_participation(self):
        toot = rt.count_rotation(1)
        self.assertEqual("4分の1回転です。", toot)

    def test_count_rotation_2_participations(self):
        toot = rt.count_rotation(2)
        self.assertEqual("2分の1回転です。", toot)

    def test_count_rotation_4_participations(self):
        toot = rt.count_rotation(4)
        self.assertEqual("1回転です。", toot)

    def test_count_rotation_5_participations(self):
        toot = rt.count_rotation(5)
        self.assertEqual("1と4分の1回転です。", toot)

    def test_count_rotation_6_participations(self):
        toot = rt.count_rotation(6)
        self.assertEqual("1と2分の1回転です。", toot)

    # toot_number_rotatedのテスト。細かい回転数ごとのテストはcount_rotationでカバーしている。
    def test_toot_number_rotated_no_participation(self):
        rt.toot_number_rotated(0, 0, 0)
        rt.mastodon.status_post.assert_called_once_with(
            status=TODAY_STR + "の墓石は回転しませんでした。\n" + "今日までの回転の合計数は10と2分の1回転です。"
    ***REMOVED***

    def test_toot_number_rotated_1_participation(self):
        rt.toot_number_rotated(1, 0, 0)
        rt.mastodon.status_post.assert_called_once_with(
            status=TODAY_STR + "の墓石の回転は1人による4分の1回転です。\n" + "今日までの回転の合計数は10と4分の3回転です。"
    ***REMOVED***

    def test_toot_number_rotated_early_participation(self):
        rt.toot_number_rotated(6, 1, 0)
        rt.mastodon.status_post.assert_called_once_with(
            status=TODAY_STR
            + "の墓石の回転は6人による1と2分の1回転です。\n"
            + "また、2時30分になる前に回した人は1人です。\n"
            + "今日までの回転の合計数は12回転です。"
    ***REMOVED***

    def test_toot_number_rotated_multi_turn(self):
        rt.toot_number_rotated(6, 0, 1)
        rt.mastodon.status_post.assert_called_once_with(
            status=TODAY_STR + "の墓石の回転は6人による1と2分の1回転です。2度以上回した人は1人です。\n" + "今日までの回転の合計数は12回転です。"
    ***REMOVED***

    def test_toot_number_rotated_early_participation_and_multi_turn(self):
        rt.toot_number_rotated(6, 1, 1)
        rt.mastodon.status_post.assert_called_once_with(
            status=TODAY_STR
            + "の墓石の回転は6人による1と2分の1回転です。\n"
            + "また、2時30分になる前に回した人は1人、2度以上回した人は1人です。\n"
            + "今日までの回転の合計数は12回転です。"
    ***REMOVED***

    def test_toot_ranking(self):
        rt.toot_ranking(
            rotated_just=pd.DataFrame(
                {
                    "username": ["akyu", "kosuzu", "reimu", "marisa"],
                    "display_name": ["阿求", "小鈴", "霊夢", "魔理沙"],
                    "created_at": [
                        time(17, 30, 0, 0),
                        time(17, 30, 1, 0),
                        time(17, 30, 1, 0),
                        time(17, 30, 2, 0),
                    ],
                }
        ***REMOVED***
    ***REMOVED***
        rt.mastodon.status_post.assert_called_once_with(
            status="1位: 阿求 @akyu [02:30:00]\n2位: 小鈴 @kosuzu [02:30:01]\n2位: 霊夢 @reimu [02:30:01]\n4位: 魔理沙 @marisa [02:30:02]\n",
            visibility="unlisted",
    ***REMOVED***
