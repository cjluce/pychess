"""Define the main board's structure."""


from piece import Piece, EnumPiece, EnumColor


FileDict = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}
RankDict = {"1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7}


class Board:
    """Handle the board logic."""

    def __init__(self):
        """Initialize the board.

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
        """
        # Initialize a 64 element list of empty pieces.
        self.board = [None] * 64
        self.state_board = [0] * 64

        self.init_board()

    def __str__(self):
        """."""
        s = ""
        for i in range(0, len(self.board)):
            p = self.board[i]
            if p is None:
                s += "[]"
            else:
                s += str(p)
            if i % 8 == 7:
                s += "\n"
            else:
                s += " "

        return s

    def __rep__(self):
        """."""
        return self.__str__()

    def init_board(self):
        """Initialize a chess board w/ the default configuration."""
        piece_order = [EnumPiece.ROOK, EnumPiece.KNIGHT, EnumPiece.BISHOP,
                       EnumPiece.QUEEN, EnumPiece.KING,
                       EnumPiece.BISHOP, EnumPiece.KNIGHT, EnumPiece.ROOK]

        for board_index in range(self.parse_movestring("A1"),
                                 self.parse_movestring("H1")):
            for piece in piece_order:
                self.board[board_index] = Piece(piece,
                                                EnumColor.WHITE)

        # init white pieces
        # init non-pawns
        self.board[self.parse_movestring("A1"):
                   self.parse_movestring("H1") + 1] = [Piece(p,
                                                             EnumColor.WHITE)
                                                       for p in piece_order]
        # init pawns
        self.board[self.parse_movestring("A2"):
                   self.parse_movestring("H2") + 1] = [
                       Piece(EnumPiece.PAWN,
                             EnumColor.WHITE)
                   ] * 8

        # init black pieces
        # init non-pawns
        self.board[self.parse_movestring("A8"):
                   self.parse_movestring("H8") + 1] = [Piece(p,
                                                             EnumColor.BLACK)
                                                       for p in piece_order]
        # init pawns
        self.board[self.parse_movestring("A7"):
                   self.parse_movestring("H7") + 1] = [
                       Piece(EnumPiece.PAWN,
                             EnumColor.BLACK)
                   ] * 8

    def parse_movestring(self, movestring):
        """Parse a move string from File-Rank notation to an index."""
        # Check if movestring is a valid movestring
        movefile = movestring[0]
        moverank = movestring[1]

        moveindex = (RankDict[moverank] * 8) + FileDict[movefile]

        return moveindex

    def get(self, location):
        """Handle the getting of a piece from the board."""
        # I'm thinking that I might allow location to be either the
        # direct index, or a movestring.
        parsed_location = None
        if isinstance(location, int):
            parsed_location = location
        if isinstance(location, str):
            parsed_location = self.parse_movestring(location)

        return self.board[parsed_location]

    def set(self, location, piece: Piece):
        """Handle the setting of a piece from the board."""
        parsed_location = None
        if isinstance(location, int):
            parsed_location = location
        if isinstance(location, str):
            parsed_location = self.parse_movestring(location)

        self.board[parsed_location] = piece

    def valid_move(self, movefromi, movetoi):
        """."""
        if movefromi < 0 or movefromi > 63:
            return False
        if movetoi < 0 or movetoi > 63:
            return False

        # I need to increment the state_board in the case of a valid move

        return True

    def move(self, movefrom, moveto):
        """Evaluate the move given in the form of, e.g., ("A1", "B3")."""
        # Handle the case where the move strings are invalid.
        movefromi = self.parse_movestring(movefrom)
        movetoi = self.parse_movestring(moveto)

        moving_piece = self.get(movefromi)

        if self.valid_move(movefromi, movetoi):
            self.set(movetoi, self.get(movefromi))
            moving_piece.moved = True

            # I might want to include my en passant logic here. I will
            # probably do htis with a state board tracking whether a
            # move has happened, and by tagging pawns that are able to
            # en passant on the next turn? Not sure. Perhaps instead
            # of a state board, each piece should check their own
            # counts?

            if self.state_board[movefromi] == 0:
                self.state_board[movefromi] = 1
