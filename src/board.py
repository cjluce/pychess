"""Define the main board's structure."""


from piece import Piece, EnumPiece, EnumColor
from math import copysign


FileDict = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}
RankDict = {"1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7}

# TODO: I'm thinking that the board should store a "pieces" object
# which will just be a linked list of the pieces... perhaps along with
# their location? Maybe a dictionary would do better. Yeah, and
# perhaps there should be a piece id that gets stored?


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
        sa = [" A  B  C  D  E  F  G  H |  ",
              "---------------------------",
              ""]
        j = len(sa) - 1
        for i in range(len(self.board)):
            p = self.board[i]
            if p is None:
                sa[j] += "[]"
            else:
                sa[j] += str(p)
            if i % 8 == 7:
                sa[j] += f" | {(i+1)/8}"
                sa.append("")
                j += 1
            else:
                sa[j] += " "
        return "\n".join(sa[::-1])

    def __repr__(self):
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

    def parse_location(self, location) -> int:
        """Take a location as str or int and return index."""
        parsed_location = None
        if isinstance(location, int):
            return location
        if isinstance(location, str):
            return self.parse_movestring(location)
        return parsed_location

    # TODO: I think it would be helpful to include a rank and file
    # offset from the initial location.
    def get(self, location, rankoffset=0, fileoffset=0) -> Piece:
        """Handle the getting of a piece from the board."""
        # I'm thinking that I might allow location to be either the
        # direct index, or a movestring.
        return self.board[
            self.parse_location(location) + fileoffset + (8*rankoffset)
        ]

    def set(self, location, piece: Piece):
        """Handle the setting of a piece from the board."""
        self.board[self.parse_location(location)] = piece

    def get_rank(self, location):
        """."""
        return (self.parse_location(location) // 8) + 1

    def get_file(self, location):
        """."""
        return (self.parse_location(location) % 8) + 1

    def rank_dist(self, movefrom, moveto):
        """."""
        return abs(
            self.get_rank(movefrom) - self.get_rank(moveto)
        )

    def rank_diff(self, movefrom, moveto):
        """."""
        return self.get_rank(moveto) - self.get_rank(movefrom)

    def file_diff(self, movefrom, moveto):
        """."""
        return self.get_file(moveto) - self.get_file(movefrom)

    def rank_dir(self, movefrom, moveto):
        """
        Determine the rank direction of movement.

         0: no movement
         1: white to black
        -1: black to white
        """
        diff = self.rank_diff(movefrom, moveto)
        direction = int(copysign(1, diff))
        if diff == 0:
            direction = 0
        return direction

    def file_dir(self, movefrom, moveto):
        """
        Determine the rank direction of movement.

         0: no movement
         1: white to black
        -1: black to white
        """
        diff = self.file_diff(movefrom, moveto)
        direction = int(copysign(1, diff))
        if diff == 0:
            direction = 0
        return direction

    def file_dist(self, movefrom, moveto):
        """."""
        return abs(
            self.get_file(movefrom) - self.get_file(moveto)
        )

    def valid_bounds(self, location):
        """."""
        location = self.parse_location(location)
        if location < 0 or location > 63:
            return False
        return True

    def validate_pos_diff(self, movefrom, moveto):
        """Naive validation based on relative distances."""
        rank_dist = self.rank_dist(movefrom, moveto)
        file_dist = self.file_dist(movefrom, moveto)

        piece = self.get(movefrom)
        if piece.piece == EnumPiece.PAWN:
            # TODO: I might need to include en passant logic here.
            rank_dir = self.rank_dir(movefrom, moveto)
            if file_dist != 0:
                return False
            if rank_dist > 2:
                return False
            if rank_dist > 1 and piece.moved:
                return False
            if rank_dir > 0:
                return piece.color == EnumColor.WHITE
            if rank_dir < 0:
                return piece.color == EnumColor.BLACK
            return False
        if piece.piece == EnumPiece.BISHOP:
            return rank_dist == file_dist
        if piece.piece == EnumPiece.KNIGHT:
            # Moving by 2 in one direction and 1 in direction means
            # that the distances should multiply to 2
            return rank_dist * file_dist == 2
        if piece.piece == EnumPiece.ROOK:
            # We need to ensure that a piece is moving in exactly one
            # direction.
            return 0 in [rank_dist, file_dist]
        if piece.piece == EnumPiece.QUEEN:
            return (0 in [rank_dist, file_dist] or
                    rank_dist == file_dist)
        # TODO: Might need to add validation for castling as early as
        # here... or before this function gets called?
        if piece.piece == EnumPiece.KING:
            return (rank_dist <= 1 and
                    file_dist <= 1)

        return None

    def validate_path(self, movefrom, moveto):
        """Naive validation based on path."""
        rank_dist = self.rank_dist(movefrom, moveto)
        file_dist = self.file_dist(movefrom, moveto)
        rank_dir = self.rank_dir(movefrom, moveto)
        file_dir = self.file_dir(movefrom, moveto)

        piece = self.get(movefrom)
        if piece.piece == EnumPiece.PAWN:
            # TODO: I might need to include en passant logic here.
            # TODO: I'll also need logic for attacking an opponent on
            # the diagonal
            for d_rank in range(1, rank_dist + 1):
                pathpiece = self.get(movefrom, rankoffset=d_rank*rank_dir)
                if pathpiece is not None:
                    return False
            return True
        # if piece.piece == EnumPiece.BISHOP:
        #     for d_diag in range(1, rank_dist + 1):
        #         pathpiece = self.get(movefrom,
        #                              rankoffset=copysign(d_diag,
        #                                                  rank_dir),
        #                              fileoffset=copysign(d_diag,
        #                                                  file_dir))
        #         if pathpiece is None:
        #             continue
        #         if pathpiece.color == piece.color:
        #             return False
        #         # We now know that there is a piece, and that the
        #         # piece is of the opposite color
        #         # if d_diag != rank_dist:
        #         if pathpiece is not None:
        #             return False
        #     return True
        if piece.piece == EnumPiece.KNIGHT:
            topiece = self.get(moveto)
            return (topiece is None or
                    topiece.color != piece.color)
        if piece.piece in [EnumPiece.ROOK,
                           EnumPiece.BISHOP,
                           EnumPiece.QUEEN]:
            for offset in range(1,
                                max(rank_dist,
                                    file_dist) + 1):
                topiece = self.get(movefrom,
                                   fileoffset=offset*file_dir,
                                   rankoffset=offset*rank_dir)
                if topiece is None:
                    continue
                if topiece.color == piece.color:
                    return False
                # We now know that there is a piece, and that the
                # piece is of the opposite color
                # if d_diag != rank_dist:
                if topiece is not None:
                    return False
            return True
        if piece.piece == EnumPiece.QUEEN:
            pass
        # TODO: Might need to add validation for castling as early as
        # here... or before this function gets called?
        if piece.piece == EnumPiece.KING:
            topiece = self.get(moveto)
            return (topiece is None or
                    topiece.color != piece.color)

    # TODO: Some of these functions will have to be able to take in an
    # alternate board to determine, e.g., whether a move will result
    # with the user in check.
    def valid_move(self, movefrom, moveto):
        """."""
        movefromi = self.parse_location(movefrom)
        movetoi = self.parse_location(moveto)
        # Ensure both to and from are on the board
        if not self.valid_bounds(movefromi):
            return False
        if not self.valid_bounds(movetoi):
            return False
        # Ensure that you are actually moving a piece
        if self.get(movefromi) is None:
            return False
        # You shoudn't be able to move to where you currently are
        if movefromi == movetoi:
            return False
        # Validate the positional differences naively. This will check
        # that you are moving the piece "correctly," e.g., that
        # bishops move on the diagonal, rooks only move in a single
        # direction, ignoring checking whether the move is
        # valid.
        if not self.validate_pos_diff(movefromi, movetoi):
            print("Validating position differences failed...")
            return False
        # Validate whether the move the player is trying to make is
        # possible w.r.t. the paths between the to and from move. That
        # is to say, ensure that there isn't a piece blocking the move
        # from happening by being in the path between to and from
        if not self.validate_path(movefromi, movetoi):
            print("Validating path failed...")
            return False

        # TODO: I need validation based on en passant and castling

        # TODO: I need to increment the state_board in the case of a valid move

        return True

    def move(self, movefrom, moveto):
        """Evaluate the move given in the form of, e.g., ("A1", "B3")."""
        # TODO: Handle the case where the move strings are invalid.
        movefromi = self.parse_movestring(movefrom)
        movetoi = self.parse_movestring(moveto)

        moving_piece = self.get(movefromi)

        if self.valid_move(movefromi, movetoi):
            self.set(movetoi, self.get(movefromi))
            # TODO: It's not safe to assume that the movefrom location
            # will be pieceless as in the case of, e.g., castling.
            self.set(movefromi, None)
            moving_piece.moved = True

            return True

            # TODO: I might want to include my en passant/castling
            # logic here. I will probably do htis with a state board
            # tracking whether a move has happened, and by tagging
            # pawns that are able to en passant on the next turn? Not
            # sure. Perhaps instead of a state board, each piece
            # should check their own counts?
        return False
