# 開発ルール（共同開発ガイド）

チームで同じコードを触るときの約束ごとです。

## 1. 作業の流れ（GitHub Flow）

```
main ──●────────────●──────────●──→   いつでも動く状態を保つ
        \          /          /
         ●──●──●──┘          /        feature/xxx  …自分の作業用ブランチ
                \           /
                 ●──●──●───┘          fix/yyy
```

1. **Issue を立てる / 選ぶ** — 何をやるかを先に共有する（作業の重複を防ぐ）
2. **main を最新にする**
   ```bash
   git switch main
   git pull
   ```
3. **ブランチを切る**
   ```bash
   git switch -c feature/undo-move
   ```
4. **小さくコミットする**（1コミット = 1つの意味のある変更）
5. **テストを通す**
   ```bash
   python3 -m unittest
   ```
6. **push して Pull Request (PR) を出す**
   ```bash
   git push -u origin feature/undo-move
   ```
7. **レビューを受ける** — 最低1人の Approve をもらう
8. **main にマージ** → ブランチを削除

> ⚠️ main に直接 push しない。必ず PR を通す。

## 2. ブランチ名

| 種類 | 例 |
|---|---|
| 新機能 | `feature/ai-greedy` |
| バグ修正 | `fix/pass-detection` |
| ドキュメント | `docs/readme-usage` |
| リファクタリング | `refactor/board-directions` |

## 3. コミットメッセージ

```
<種類>: <何をしたか（短く）>

<なぜしたか（必要なら）>
```

種類: `feat`（機能追加） / `fix`（バグ修正） / `docs` / `test` / `refactor` / `chore`

例:
```
feat: 置ける場所がないときに自動でパスする

今まではプレイヤーが入力待ちで止まってしまっていた。
Closes #12
```

PR やコミットに `Closes #12` と書くと、マージ時に Issue #12 が自動で閉じます。

## 4. コンフリクトが起きたら

他の人が先に main を更新して、同じ箇所を変えていた場合に起きます。

```bash
git switch feature/自分のブランチ
git fetch origin
git merge origin/main        # ここでコンフリクトが表示される
# ファイル内の <<<<<<< ======= >>>>>>> を手で直す
python3 -m unittest          # 直したら必ずテスト
git add .
git commit
```

迷ったら、その箇所を書いた人に相談するのが一番早いです。

## 5. レビューのポイント

レビューする人:
- 動くか？（手元でブランチを checkout して実行してみる）
- テストはあるか？
- 名前は分かりやすいか？
- 責任の分離は守られているか？（`board.py` に `print` が入っていないか 等）
- 指摘は「人」ではなく「コード」に対して、理由を添えて

レビューされる人:
- PR は小さく（目安: 差分 200 行以内）
- PR の説明に「何を・なぜ・どう確認したか」を書く

## 6. コードスタイル

- Python は [PEP 8](https://peps.python.org/pep-0008/) に従う
- 関数には何をするかが分かる docstring を1行書く
- `board.py` には表示・入力のコードを入れない
