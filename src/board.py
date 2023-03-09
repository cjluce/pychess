"""Define the main board's structure."""


from piece import Piece
from move import Move


class Board:
    """Handle the internal storing of pieces.

    In addition, I might have the board handle the parsing of FEN
    strings. This might be better off as a separate class.

    -----------------------------
    |  A  B  C  D  E  F  G  H |
    | ---------------------------
    | 56 57 58 59 60 61 62 63 | 8
    | 48 49 50 51 52 53 54 55 | 7
    | 40 41 42 43 44 45 46 47 | 6
    | 32 33 34 35 36 37 38 39 | 5
    | 24 25 26 27 28 29 30 31 | 4
    | 16 17 18 19 20 21 22 23 | 3
    | 08 09 10 11 12 13 14 15 | 2
    | 00 01 02 03 04 05 06 07 | 1
    -----------------------------

    The board is represented by a python list of Piece objects with
    length 64.

    """

    def __init__(self):
        """."""
        self.board = [None] * 64

    def __str__(self):
        """."""
        printstring = [" A  B  C  D  E  F  G  H |  ",
                       "---------------------------",
                       ""]
        j = len(printstring) - 1
        for i in range(len(self.board)):
            p = self.board[i]
            if p is None:
                printstring[j] += "[]"
            else:
                printstring[j] += str(p)
            if i % 8 == 7:
                printstring[j] += f" | {(i+1)/8}"
                printstring.append("")
                j += 1
            else:
                printstring[j] += " "
        return "\n".join(printstring[::-1])

    def __repr__(self):
        """."""
        return self.__str__()

    def set(self, move: Move, value):
        """Set the board at index `move.index` to value.

        Return True if a value was correctly set at the index,
        otherwise False.

        """
        if not isinstance(value, Piece) and value is not None:
            print(f"""You tried to set {move.index} to an invalid
            move: {value}""")
            return False

        self.board[move.index] = value
        return True

    def get(self, move: Move) -> Piece:
        """Return the value of the board at index `moveinput`."""
        return self.board[move.index]

    # TODO: I'm probably not going to have the board implement the
    # "move" method and am considering moving this to the ChessEngine
    # class. We will see how well that works later.
    def move(self, movefrom, moveto):
        """Handle the moving of pieces on the internal board.

        This is a little more nuanced than just moving the piece at
        `movefrom` to the square at `moveto`. Let's assume that there
        is a piece located at `movefrom`. There are a few cases:

        0) Either the requested move is valid or not. I'm not sure
        whether I only want to handle valid moves, here, or if I will
        allow invalid moves on the internal board. Let's assume for
        the following cases that the move is valid.

        1) There is not a piece at `moveto`, and we simply shift the
        piece from `movefrom` to `moveto`.

        2) There is an enemy piece at `moveto`, and we must remove
        that piece from the board, and then move the friendly piece to
        the respective square.

        3) The move requested is identified as a castle (will need to
        be cross-verified by the ChessEngine class).

        4) The move requested is identified as an en passant (will
        need to be cross-verified by the ChessEngine class).

        """
        # try:
        #     movefrom_index = self.parse_moveinput(movefrom)
        #     moveto_index = self.parse_moveinput(moveto)
        # except (ValueError, KeyError) as e:
        #     print(f"Failed to parse move: {e}")
        pass
