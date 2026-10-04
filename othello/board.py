"""盤面とルール。表示や入力のコードはここに書かないこと。"""

SIZE = 8
EMPTY = 0
BLACK = 1
WHITE = -1  # 相手の色は -color で求められる

# 8方向 (行の増分, 列の増分)
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
]


def opponent(color):
    """相手の色を返す。"""
    return -color


class Board:
    """8x8 のオセロ盤。座標は (row, col)、どちらも 0〜7。"""

    def __init__(self):
        self.grid = [[EMPTY] * SIZE for _ in range(SIZE)]
        mid = SIZE // 2
        self.grid[mid - 1][mid - 1] = WHITE
        self.grid[mid][mid] = WHITE
        self.grid[mid - 1][mid] = BLACK
        self.grid[mid][mid - 1] = BLACK

    def copy(self):
        """盤面の複製を返す（AI の先読みなどに使う）。"""
        new = Board.__new__(Board)
        new.grid = [row[:] for row in self.grid]
        return new

    def get(self, row, col):
        """指定マスの石を返す。"""
        return self.grid[row][col]

    @staticmethod
    def in_bounds(row, col):
        """盤の内側かどうか。"""
        return 0 <= row < SIZE and 0 <= col < SIZE

    def flips_for(self, row, col, color):
        """(row, col) に color を置いたときに裏返る石の座標リストを返す。"""
        if not self.in_bounds(row, col) or self.grid[row][col] != EMPTY:
            return []
        flips = []
        for dr, dc in DIRECTIONS:
            line = []
            r, c = row + dr, col + dc
            while self.in_bounds(r, c) and self.grid[r][c] == opponent(color):
                line.append((r, c))
                r, c = r + dr, c + dc
            # 相手の石が1つ以上続き、その先に自分の石があれば挟める
            if line and self.in_bounds(r, c) and self.grid[r][c] == color:
                flips.extend(line)
        return flips

    def is_valid_move(self, row, col, color):
        """そこに置けるかどうか。"""
        return bool(self.flips_for(row, col, color))

    def valid_moves(self, color):
        """color が置ける全マスのリストを返す。"""
        return [
            (r, c)
            for r in range(SIZE)
            for c in range(SIZE)
            if self.is_valid_move(r, c, color)
        ]

    def place(self, row, col, color):
        """石を置いて挟んだ石を裏返す。裏返した石のリストを返す。

        置けない場所なら ValueError。
        """
        flips = self.flips_for(row, col, color)
        if not flips:
            raise ValueError(f"({row}, {col}) には置けません")
        self.grid[row][col] = color
        for r, c in flips:
            self.grid[r][c] = color
        return flips

    def count(self, color):
        """color の石の数を返す。"""
        return sum(row.count(color) for row in self.grid)

    def is_game_over(self):
        """両者とも置ける場所がなければ終局。"""
        return not self.valid_moves(BLACK) and not self.valid_moves(WHITE)

    def winner(self):
        """勝者の色を返す。引き分けなら EMPTY。"""
        black, white = self.count(BLACK), self.count(WHITE)
        if black > white:
            return BLACK
        if white > black:
            return WHITE
        return EMPTY
