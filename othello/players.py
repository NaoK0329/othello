"""プレイヤー。どのプレイヤーも choose_move(board, color) を持つ。

新しい AI を追加するときは、このファイルにクラスを1つ足すだけでよい。
"""

import random

from .board import SIZE

COLUMNS = "abcdefgh"


def parse_position(text):
    """'d3' のような文字列を (row, col) に変換する。不正なら None。"""
    text = text.strip().lower()
    if len(text) != 2 or text[0] not in COLUMNS or not text[1].isdigit():
        return None
    row, col = int(text[1]) - 1, COLUMNS.index(text[0])
    if not (0 <= row < SIZE):
        return None
    return row, col


def format_position(row, col):
    """(row, col) を 'd3' のような文字列に変換する。"""
    return f"{COLUMNS[col]}{row + 1}"


class QuitGame(Exception):
    """プレイヤーが終了を選んだ。"""


class HumanPlayer:
    """キーボードから手を入力する人間のプレイヤー。"""

    def __init__(self, name, input_func=input):
        self.name = name
        self.input_func = input_func  # テストで差し替えられるように

    def choose_move(self, board, color):
        """入力を受け取り、置ける場所が入力されるまで聞き直す。"""
        while True:
            text = self.input_func(f"{self.name} の番です (例: d3, q で終了) > ")
            if text.strip().lower() == "q":
                raise QuitGame
            pos = parse_position(text)
            if pos is None:
                print("  入力の形式が正しくありません。")
            elif not board.is_valid_move(*pos, color):
                print("  そこには置けません。")
            else:
                return pos


class RandomAI:
    """置ける場所からランダムに選ぶ AI。"""

    def __init__(self, name="ランダムAI", rng=None):
        self.name = name
        self.rng = rng or random.Random()

    def choose_move(self, board, color):
        """置ける場所からランダムに1つ選ぶ。"""
        return self.rng.choice(board.valid_moves(color))
