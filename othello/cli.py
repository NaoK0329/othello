"""ターミナルでの表示とゲーム進行。"""

import argparse

from .board import BLACK, EMPTY, SIZE, WHITE, Board
from .players import COLUMNS, HumanPlayer, QuitGame, RandomAI, format_position

SYMBOLS = {BLACK: "●", WHITE: "○", EMPTY: "・"}
NAMES = {BLACK: "黒●", WHITE: "白○"}
HINT = "*"


def render(board, hints=()):
    """盤面を文字列にする。hints のマスには * を表示する。"""
    lines = ["   " + " ".join(COLUMNS)]
    for r in range(SIZE):
        cells = []
        for c in range(SIZE):
            cells.append(HINT if (r, c) in hints else SYMBOLS[board.get(r, c)])
        lines.append(f"{r + 1:>2} " + " ".join(cells))
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
    print("引き分け！" if winner == EMPTY else f"{NAMES[winner]} の勝ち！")
    return board


def main(argv=None):
    parser = argparse.ArgumentParser(description="ターミナルで遊ぶオセロ")
    parser.add_argument("--ai", action="store_true", help="白をランダムAIにする")
    args = parser.parse_args(argv)

    players = {
        BLACK: HumanPlayer(NAMES[BLACK]),
        WHITE: RandomAI() if args.ai else HumanPlayer(NAMES[WHITE]),
    }
    try:
        play(players)
    except (QuitGame, KeyboardInterrupt, EOFError):
        print("\nゲームを終了しました。")
