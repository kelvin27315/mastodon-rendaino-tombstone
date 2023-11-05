# mastodon-rendaino-tombstone

Mastodonの東方インスタンス[gensokyo.town](https://gensokyo.town)で動いているbot,蓮台野の墓石([@Rendaino_tombstone@gensokyo.town](https://gensokyo.town/@Rendaino_tombstone))のプログラムです。

動いてた（インスタンス: [gensokyo.cloud](https://gensokyo.cloud), アカウント: [@Rendaino_tombstone@gensokyo.cloud](https://gensokyo.cloud/@Rendaino_tombstone)）

## 競技について

2:30丁度に墓石を回す事を目指す競技です。</br>

## 競技ルールについて

対象のtootは、gensokyo.cloudのローカルタイムラインにJSTで2:29から2:31(UTCで17:29から17:31)の間に["ずずず", "ズズズ", "ｽﾞｽﾞｽﾞ"]の何れかを含めたtootです。</br>
順位は2:30に近いものほど良い順位となりますが、2:30より前にtootされたものは失格となります。(失格でも順位が割り当てられないだけで、順位があるものと同様に掲載されます)</br>
対象の時刻内に複数回回した人は掲載されはしませんが、人数がカウントされるようになっています。また、ランキングに掲載されるものは一番最初のtootのみとなっています。</br>

## Install
```
poetry install --no-root
```

## Lint/Format
```
make lint
```

```
make format
```

## Test
```
make test
```
