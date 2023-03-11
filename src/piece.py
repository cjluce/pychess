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

    def __init__(self, color: EnumColor):
        """."""
        self.id = next(self.id_iter)
        self.color = color
        self.has_moved = False
        self.oppositecolor = self.get_oppositecolor()

    def __str__(self):
        """."""
        return f"{self.get_color_str()}{self.get_piece_str()}"

    def __repr__(self):
        """."""
        return self.__str__()

    def get_oppositecolor(self):
        """Return the opposite of `self.color`."""
        if self.color == EnumColor.WHITE:
            return EnumColor.BLACK
        else:
            return EnumColor.WHITE

    def get_piece_str(self):
        """Short, identifiable string for console output."""
        raise NotImplementedError

    def get_color_str(self):
        """Get a short string representing color for console output."""
        if self.color == EnumColor.WHITE:
            return "W"
        return "B"


# TODO: Add promotion.
class Pawn(Piece):
    """."""

    def __init__(self, color: EnumColor):
        """."""
        super().__init__(color)
        self.can_enpassant = False
        # This value will be attached to an attacking pawn, and will
        # equal the piece that the said pawn can attack via en passant
        self.en_passant_attacked = None
        # This value is equal to the index of the piece that the
        # attacking pawn can attack
        self.en_passant_piece = None

    def get_piece_str(self):
        """."""
        return "P"

    def get_enpassant_status(self):
        """."""
        return self.can_enpassant

    def set_enpassant_status(self, can_enpassant):
        """."""
        self.can_enpassant = can_enpassant


class Bishop(Piece):
    """."""

    def __init__(self, color: EnumColor):
        """."""
        super().__init__(color)

    def get_piece_str(self):
        """."""
        return "B"


class Knight(Piece):
    """."""

    def __init__(self, color: EnumColor):
        """."""
        super().__init__(color)

    def get_piece_str(self):
        """."""
        return "N"


class Rook(Piece):
    """."""

    def __init__(self, color: EnumColor):
        """."""
        super().__init__(color)
        self.can_castle = False

    def get_piece_str(self):
        """."""
        return "R"


class Queen(Piece):
    """."""

    def __init__(self, color: EnumColor):
        """."""
        super().__init__(color)

    def get_piece_str(self):
        """."""
        return "Q"


class King(Piece):
    """."""

    def __init__(self, color: EnumColor):
        """."""
        super().__init__(color)
        self.can_castle = False
        self.can_castle_kings = False
        self.can_castle_queens = False

    def get_piece_str(self):
        """."""
        return "K"
