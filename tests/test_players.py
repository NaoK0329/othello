import random
import unittest

from othello.board import BLACK, Board
from othello.players import (
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


if __name__ == "__main__":
    unittest.main()
