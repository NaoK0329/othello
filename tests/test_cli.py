import contextlib
import io
import random
import unittest

from othello.board import BLACK, WHITE
from othello.cli import play
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


if __name__ == "__main__":
    unittest.main()
