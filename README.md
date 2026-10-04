# オセロ (Othello)

共同開発の練習用に作った、ターミナルで遊べるオセロゲームです。
Python の標準ライブラリだけで動きます（追加インストール不要）。

## 遊び方

```bash
python3 -m othello          # 人 vs 人
python3 -m othello --ai     # 人(黒) vs ランダムAI(白)
```

`d3` のように「列(a-h)＋行(1-8)」で石を置く場所を入力します。`q` で終了。

## テスト

```bash
python3 -m unittest -v
```

## ファイル構成と担当範囲

役割ごとにファイルを分けているので、複数人が別々のファイルを触れば
コンフリクト（同じ行の同時編集）が起きにくくなっています。

| ファイル | 役割 | 依存 |
|---|---|---|
| `othello/board.py`  | 盤面とルール（石を置く・裏返す・勝敗判定） | なし |
| `othello/players.py`| プレイヤー（人間・AI） | board |
| `othello/cli.py`    | 画面表示とゲームの進行 | board, players |
| `tests/`            | 自動テスト | 各モジュール |

`board.py` は表示や入力を一切知らない「純粋なロジック」です。
こうしておくと、将来 GUI 版や Web 版を作る人も `board.py` をそのまま再利用できます。

## 開発に参加するには

[CONTRIBUTING.md](CONTRIBUTING.md) を読んでください。
