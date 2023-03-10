"""Define the main board's structure."""


import piece as p
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

    default_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def __init__(self):
        """."""
        self.board = [None] * 64
        self.pieces = {}
        self.update_pieces()

    def init_board(self, fenstring=default_fen):
        """."""
        self.parse_fen(fenstring)
        self.update_pieces()

    def update_pieces(self):
        """."""
        self.pieces = {}
        i = 0
        for piece in self.board:
            if piece is None:
                i += 1
                continue
            self.pieces[i] = str(piece)
            i += 1

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
        if not isinstance(value, p.Piece) and value is not None:
            print(f"""You tried to set {move.index} to an invalid
            move: {value}""")
            return False

        self.board[move.index] = value
        self.update_pieces()
        return True

    def get(self, move: Move) -> p.Piece:
        """Return the value of the board at index `moveinput`."""
        return self.board[move.index]

    def parse_fen(self, fenstring):
        """Parse the FEN string.

        rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

        """
        # TODO: Implement the rest of the fen string, clean up the
        # board parsing.
        fen_chunks = fenstring.split(" ")

        fen_board = fen_chunks[0].split("/")

        fen_index = 56
        fen_dict = {'p': p.Pawn,
                    'b': p.Bishop,
                    'n': p.Knight,
                    'r': p.Rook,
                    'q': p.Queen,
                    'k': p.King}
        for row in fen_board:
            for f in row:
                if f.lower() in fen_dict:
                    color = p.EnumColor.WHITE if f.lower() != f else p.EnumColor.BLACK
                    self.set(Move(fen_index), fen_dict[f.lower()](color))
                    fen_index += 1
                else:
                    skip = int(f)
                    for s in range(skip):
                        self.set(Move(fen_index), None)
                        fen_index += 1
            fen_index -= 16
