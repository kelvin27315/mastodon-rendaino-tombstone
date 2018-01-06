# mastodon-rendaino-tombstone

Mastodonの東方インスタンス[gensokyo.cloud](https://gensokyo.cloud)で動いているbot,蓮台野の墓石([@Rendaino_tombstone](https://gensokyo.cloud/@Rendaino_tombstone))のプログラムです。

### 競技について

2:30丁度に墓石を回す事を目指す競技です。</br>

### 競技ルールについて

対象のtootは、gensokyo.cloudのローカルタイムラインにJSTで2:29から2:31(UTCで17:29から17:31)の間に["ずずず", "ズズズ", "ｽﾞｽﾞｽﾞ"]の何れかを含めたtootです。</br>
順位は2:30に近いものほど良い順位となりますが、2:30より前にtootされたものは失格となります。(失格でも順位が割り当てられないだけで、順位があるものと同様に掲載されます)</br>
対象の時刻内に複数回回した人は掲載されはしませんが、人数がカウントされるようになっています。また、ランキングに掲載されるものは一番最初のtootのみとなっています。</br>

### 更新記録

2018-01-06
- gensokyo.townのみに対応

2017-12-27
- 回転数が1回転未満の場合に不要な0が表示されるバグを修正しました。

2017-12-11
- add travis supportをmergeしました。
- .travis.ymlで指定するpythonのversionを3.6にしました。

2017-12-04
- Mastodon.py 1.1.2 に対応しました。
- requirements.txt を追加しました。

2017-11-11
- Add unittest をmergeしました。

2017-09-09
- コードの修正

2017-09-07
- 未収歳・非公開・@Rendaino_tombstoneへのダイレクトのtootに対応しました。</br>現状では時刻を返すだけで順位は返しません。
