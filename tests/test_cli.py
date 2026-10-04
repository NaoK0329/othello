import contextlib
import io
import random
import unittest

from othello.board import BLACK, WHITE, Board
from othello.cli import display_width, play, render
from othello.players import RandomAI


class TestPlay(unittest.TestCase):
    def test_ai_vs_ai_finishes(self):
        players = {
            BLACK: RandomAI(rng=random.Random(1)),
            WHITE: RandomAI(rng=random.Random(2)),
        }
        with contextlib.redirect_stdout(io.StringIO()):
            board = play(players)
        self.assertTrue(board.is_game_over())


class TestRender(unittest.TestCase):
    def test_display_width(self):
        self.assertEqual(display_width("a"), 1)
        self.assertEqual(display_width("・"), 2)

    def test_rows_line_up_with_column_labels(self):
        board = Board()
        lines = render(board, hints=board.valid_moves(BLACK)).splitlines()
        header, rows = lines[0], lines[1:9]
        # 全角の「・」と半角の「●」「*」が混ざっても、行の表示幅がそろう (#4)
        for row in rows:
            self.assertEqual(display_width(row), display_width(header), row)


if __name__ == "__main__":
    unittest.main()
