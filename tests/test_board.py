import unittest

from othello.board import BLACK, EMPTY, WHITE, Board


class TestInitialBoard(unittest.TestCase):
    def test_starts_with_two_stones_each(self):
        board = Board()
        self.assertEqual(board.count(BLACK), 2)
        self.assertEqual(board.count(WHITE), 2)

    def test_black_has_four_opening_moves(self):
        board = Board()
        self.assertCountEqual(
            board.valid_moves(BLACK),
            [(2, 3), (3, 2), (4, 5), (5, 4)],
        )


class TestPlace(unittest.TestCase):
    def test_place_flips_sandwiched_stone(self):
        board = Board()
        flipped = board.place(2, 3, BLACK)
        self.assertEqual(flipped, [(3, 3)])
        self.assertEqual(board.get(3, 3), BLACK)
        self.assertEqual(board.count(BLACK), 4)
        self.assertEqual(board.count(WHITE), 1)

    def test_cannot_place_where_nothing_flips(self):
        board = Board()
        with self.assertRaises(ValueError):
            board.place(0, 0, BLACK)

    def test_cannot_place_on_occupied_square(self):
        board = Board()
        self.assertFalse(board.is_valid_move(3, 3, BLACK))

    def test_flips_in_multiple_directions(self):
        board = Board()
        board.grid = [[EMPTY] * 8 for _ in range(8)]
        # 黒が (2,2) に置くと、右と下の白を同時に挟む
        board.grid[2][3] = WHITE
        board.grid[2][4] = BLACK
        board.grid[3][2] = WHITE
        board.grid[4][2] = BLACK
        flipped = board.place(2, 2, BLACK)
        self.assertCountEqual(flipped, [(2, 3), (3, 2)])


class TestGameEnd(unittest.TestCase):
    def test_full_board_is_game_over(self):
        board = Board()
        board.grid = [[BLACK] * 8 for _ in range(8)]
        self.assertTrue(board.is_game_over())
        self.assertEqual(board.winner(), BLACK)

    def test_draw(self):
        board = Board()
        board.grid = [[BLACK] * 8 for _ in range(4)] + [[WHITE] * 8 for _ in range(4)]
        self.assertEqual(board.winner(), EMPTY)


if __name__ == "__main__":
    unittest.main()
