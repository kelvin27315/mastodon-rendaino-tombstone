# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock
import Round_tombstone as rt
from datetime import date, datetime, timezone
import mastodon

TODAY_STR = '{dt.month}月{dt.day}日'.format(dt = date.today())
UTC = timezone.utc

class TestRoundTombstone(unittest.TestCase):
    def setUp(self):
# rt.mastodon をmockするので、元のが定義されていたら退避
        self.original_mastodon = rt.mastodon if hasattr(rt, 'mastodon') else None
        rt.mastodon = Mock(spec=mastodon.Mastodon)

    def tearDown(self):
        rt.mastodon = self.original_mastodon

    def test_get_timeline(self):
        rt.mastodon.timeline.side_effect = [
 # timeline取得 1回目
            [
                { 'id': 12, 'created_at': datetime(2017, 11, 4, 17, 30, 0, 0, UTC), 'content': 'コスズ', 'account': { 'username': 'kosuzu', 'display_name': '小鈴', } },
                { 'id': 11, 'created_at': datetime(2017, 11, 4, 17, 30, 0, 0, UTC), 'content': 'ｽﾞｽﾞｽﾞ', 'account': { 'username': 'marisa', 'display_name': '魔理沙', } },
                { 'id': 10, 'created_at': datetime(2017, 11, 4, 17, 29, 0, 0, UTC), 'content': 'ズズズ', 'account': { 'username': 'reimu', 'display_name': '霊夢', } }
            ],
# timeline取得 2回目
            [
                { 'id': 9, 'created_at': datetime(2017, 11, 4, 17, 29, 0, 0, UTC), 'content': 'ズズズ', 'account': { 'username': 'sanae', 'display_name': '早苗', } },
                { 'id': 8, 'created_at': datetime(2017, 11, 4, 17, 28, 0, 0, UTC), 'content': 'ズズズ', 'account': { 'username': 'sakuya', 'display_name': '咲夜', } },
            ],
# timeline取得 3回目。実際には呼ばれない
            [
                { 'id': 7, 'created_at': datetime(2017, 11, 4, 17, 28, 0, 0, UTC), 'content': 'ズズズ', 'account': { 'username': 'akyu', 'display_name': '阿求', } },
            ],
        ]
        results = rt.get_timeline('local')
# 取得したTLの検証。
        self.assertEqual(['咲夜', '霊夢', '早苗', '小鈴', '魔理沙'], [x['account']['display_name'] for x in results])
# mastodon APIの呼び出し回数検証
        self.assertEqual(2, len(rt.mastodon.timeline.mock_calls))

    def test_select_toots(self):
        toots = [
# positive
            { 'id': 10, 'created_at': datetime(2017, 11, 4, 17, 29, 0, 0, UTC), 'content': 'ズズズ', 'account': { 'username': 'reimu', 'display_name': '霊夢', } },
            { 'id': 11, 'created_at': datetime(2017, 11, 4, 17, 30, 0, 0, UTC), 'content': 'ｽﾞｽﾞｽﾞ', 'account': { 'username': 'marisa', 'display_name': '魔理沙', } },
# negative
            { 'id': 12, 'created_at': datetime(2017, 11, 4, 17, 31, 0, 0, UTC), 'content': 'コスズ', 'account': { 'username': 'kosuzu', 'display_name': '小鈴', } },
        ]
        results = rt.select_toots(toots)
        self.assertEqual(['reimu','marisa'], list(results['username']))
        self.assertEqual(['霊夢','魔理沙'], list(results['display_name']))

# toot_number_rotatedについて、細かいケースごとにテスト
    def test_toot_number_rotated_no_participation(self):
        rt.toot_number_rotated(0, 0, 0)
        rt.mastodon.status_post.assert_called_once_with(TODAY_STR + 'の墓石は回転しませんでした。')

    def test_toot_number_rotated_1_participation(self):
        rt.toot_number_rotated(1, 0, 0)
# BUG: 4人未満の場合に余計な0が付く
        rt.mastodon.status_post.assert_called_once_with(TODAY_STR + 'の墓石の回転は1人による4分の1回転でした。')

    def test_toot_number_rotated_2_participations(self):
        rt.toot_number_rotated(2, 0, 0)
# BUG: 4人未満の場合に余計な0が付く
        rt.mastodon.status_post.assert_called_once_with(TODAY_STR + 'の墓石の回転は2人による2分の1回転でした。')

    def test_toot_number_rotated_4_participations(self):
        rt.toot_number_rotated(4, 0, 0)
        rt.mastodon.status_post.assert_called_once_with(TODAY_STR + 'の墓石の回転は4人による1回転でした。')

    def test_toot_number_rotated_5_participations(self):
        rt.toot_number_rotated(5, 0, 0)
        rt.mastodon.status_post.assert_called_once_with(TODAY_STR + 'の墓石の回転は5人による1と4分の1回転でした。')

    def test_toot_number_rotated_6_participations(self):
        rt.toot_number_rotated(6, 0, 0)
        rt.mastodon.status_post.assert_called_once_with(TODAY_STR + 'の墓石の回転は6人による1と2分の1回転でした。')

    def test_toot_number_rotated_early_participation(self):
        rt.toot_number_rotated(6, 1, 0)
        rt.mastodon.status_post.assert_called_once_with(TODAY_STR + 'の墓石の回転は6人による1と2分の1回転でした。\nまた、2時30分になる前に回した人は1人です。')

    def test_toot_number_rotated_multi_turn(self):
        rt.toot_number_rotated(6, 0, 1)
        rt.mastodon.status_post.assert_called_once_with(TODAY_STR + 'の墓石の回転は6人による1と2分の1回転でした。2度以上回した人は1人です。')

    def test_toot_number_rotated_early_participation_and_multi_turn(self):
        rt.toot_number_rotated(6, 1, 1)
        rt.mastodon.status_post.assert_called_once_with(TODAY_STR + 'の墓石の回転は6人による1と2分の1回転でした。\nまた、2時30分になる前に回した人は1人、2度以上回した人は1人です。')

if __name__ == '__main__':
    unittest.main()
