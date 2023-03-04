"""Define the structure and handling of each piece."""


from enum import Enum
from itertools import count


class EnumPiece(Enum):
    """."""

    PAWN = 1
    BISHOP = 2
    KNIGHT = 3
    ROOK = 4
    QUEEN = 5
    KING = 6


class EnumColor(Enum):
    """."""

    WHITE = 0
    BLACK = 1


class Piece:
    """."""

    id_iter = count()

    def __init__(self, piece: EnumPiece, color: EnumColor):
        """."""
        self.id = next(self.id_iter)
        self.piece = piece
        self.color = color
        self.moved = False
        self.can_enpassant = False
        self.tag = self.create_tag()

    def create_tag(self):
        """."""
        color_dict = {EnumColor.WHITE: "white",
                      EnumColor.BLACK: "black"}
        piece_dict = {EnumPiece.PAWN: "pawn",
                      EnumPiece.BISHOP: "bishop",
                      EnumPiece.KNIGHT: "knight",
                      EnumPiece.ROOK: "rook",
                      EnumPiece.QUEEN: "queen",
                      EnumPiece.KING: "king"}
        return f"{color_dict[self.color]}_{piece_dict[self.piece]}"

    def __str__(self):
        """."""
        color_dict = {EnumColor.WHITE: "W",
                      EnumColor.BLACK: "B"}
        piece_dict = {EnumPiece.PAWN: "P",
                      EnumPiece.BISHOP: "B",
                      EnumPiece.KNIGHT: "N",
                      EnumPiece.ROOK: "R",
                      EnumPiece.QUEEN: "Q",
                      EnumPiece.KING: "K"}

        return f"{color_dict[self.color]}{piece_dict[self.piece]}"

    def __repr__(self):
        """."""
        return self.__str__()
