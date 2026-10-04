"""ターミナルでの表示とゲーム進行。"""

import argparse
import unicodedata

from .board import BLACK, EMPTY, SIZE, WHITE, Board
from .players import COLUMNS, GreedyAI, HumanPlayer, QuitGame, RandomAI, format_position

AI_TYPES = {"random": RandomAI, "greedy": GreedyAI}

SYMBOLS = {BLACK: "●", WHITE: "○", EMPTY: "・"}
NAMES = {BLACK: "黒●", WHITE: "白○"}
HINT = "*"
CELL_WIDTH = 2  # 1マスの表示幅（全角1文字分）


def display_width(text):
    """ターミナルでの表示幅を返す。全角は2、それ以外は1として数える。"""
    return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in text)


def pad_cell(text):
    """表示幅が CELL_WIDTH になるよう右を空白で埋める。

    「・」(全角) と「●」「a」(半角扱い) が混ざっても列がそろうようにするため。
    """
    return text + " " * (CELL_WIDTH - display_width(text))


def render(board, hints=()):
    """盤面を文字列にする。hints のマスには * を表示する。"""
    lines = ["   " + "".join(pad_cell(col) for col in COLUMNS)]
    for r in range(SIZE):
        cells = []
        for c in range(SIZE):
            symbol = HINT if (r, c) in hints else SYMBOLS[board.get(r, c)]
            cells.append(pad_cell(symbol))
        lines.append(f"{r + 1:>2} " + "".join(cells))
    lines.append(f"   {NAMES[BLACK]} {board.count(BLACK)}  {NAMES[WHITE]} {board.count(WHITE)}")
    return "\n".join(lines)


def play(players, board=None):
    """ゲームを最後まで進めて、終了時の盤面を返す。

    players は {BLACK: プレイヤー, WHITE: プレイヤー} の辞書。
    """
    board = board or Board()
    color = BLACK
    while not board.is_game_over():
        moves = board.valid_moves(color)
        print()
        print(render(board, hints=moves))
        if not moves:
            print(f"{NAMES[color]} は置ける場所がないのでパスします。")
        else:
            row, col = players[color].choose_move(board, color)
            board.place(row, col, color)
            print(f"{NAMES[color]} → {format_position(row, col)}")
        color = -color

    print()
    print(render(board))
    winner = board.winner()
    diff = abs(board.count(BLACK) - board.count(WHITE))
    print("引き分け！" if winner == EMPTY 
        else f"{NAMES[winner]}の勝ち！ ({diff}石差)")
    return board


def main(argv=None):
    parser = argparse.ArgumentParser(description="ターミナルで遊ぶオセロ")
    parser.add_argument(
        "--ai",
        nargs="?",
        const="random",
        choices=AI_TYPES,
        help="白をAIにする (random: ランダム / greedy: 欲張り。省略時は random)",
    )
    args = parser.parse_args(argv)

    players = {
        BLACK: HumanPlayer(NAMES[BLACK]),
        WHITE: AI_TYPES[args.ai]() if args.ai else HumanPlayer(NAMES[WHITE]),
    }
    try:
        play(players)
    except (QuitGame, KeyboardInterrupt, EOFError):
        print("\nゲームを終了しました。")
