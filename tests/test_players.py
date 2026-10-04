import random
import unittest

from othello.board import BLACK, EMPTY, WHITE, Board
from othello.players import (
    GreedyAI,
    HumanPlayer,
    QuitGame,
    RandomAI,
    format_position,
    parse_position,
)


class TestPosition(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(parse_position("a1"), (0, 0))
        self.assertEqual(parse_position(" H8 "), (7, 7))

    def test_parse_invalid(self):
        for text in ["", "z1", "a9", "a0", "11", "abc"]:
            self.assertIsNone(parse_position(text), text)

    def test_format_is_inverse_of_parse(self):
        self.assertEqual(format_position(*parse_position("d3")), "d3")


class TestHumanPlayer(unittest.TestCase):
    def test_retries_until_valid_move(self):
        answers = iter(["xx", "a1", "d3"])  # 形式エラー → 置けない → OK
        player = HumanPlayer("テスト", input_func=lambda _: next(answers))
        self.assertEqual(player.choose_move(Board(), BLACK), (2, 3))

    def test_quit(self):
        player = HumanPlayer("テスト", input_func=lambda _: "q")
        with self.assertRaises(QuitGame):
            player.choose_move(Board(), BLACK)


class TestRandomAI(unittest.TestCase):
    def test_always_chooses_valid_move(self):
        board = Board()
        ai = RandomAI(rng=random.Random(0))
        for _ in range(20):
            self.assertIn(ai.choose_move(board, BLACK), board.valid_moves(BLACK))


class TestGreedyAI(unittest.TestCase):
    def test_chooses_move_that_flips_most(self):
        board = Board()
        board.grid = [[EMPTY] * 8 for _ in range(8)]
        # (0,3) なら白2つ、(4,7) なら白1つ裏返せる
        board.grid[0][0] = BLACK
        board.grid[0][1] = WHITE
        board.grid[0][2] = WHITE
        board.grid[2][7] = BLACK
        board.grid[3][7] = WHITE
        self.assertCountEqual(board.valid_moves(BLACK), [(0, 3), (4, 7)])
        ai = GreedyAI(rng=random.Random(0))
        self.assertEqual(ai.choose_move(board, BLACK), (0, 3))


if __name__ == "__main__":
    unittest.main()
