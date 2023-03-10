"""."""

from board import Board
from move import Move
import piece as p


class ChessEngine:
    """."""

    _north = 8
    _south = -8
    _east = 1
    _west = -1
    _northeast = 9
    _northwest = 7
    _southeast = -7
    _southwest = 9

    def __init__(self, board: Board):
        """."""
        self.board = board
        self._dispatch_piecetype_validation = {
            p.Pawn: self._get_valid_moves_pawn,
            p.Knight: self._get_valid_moves_knight,
            p.Bishop: self._get_valid_moves_bishop,
            p.Rook: self._get_valid_moves_rook,
            p.Queen: self._get_valid_moves_queen,
            p.King: self._get_valid_moves_king
        }

    # TODO: I think I'll need to add a color here.
    def is_board_check(self, board: Board):
        """Check whether the board is currently in check."""
        pass

    def _valid_square_test(self, testindex, color: p.EnumColor):
        """."""
        if not self.valid_index(testindex):
            return False
        testpiece = self.board.get(testindex)
        if testpiece is None:
            return True
        if testpiece.oppositecolor == color:
            return True
        return False

    def _valid_square_linear_path(self,
                                  move: Move,
                                  piece: p.Piece,
                                  direction):
        """."""
        target_moves = []

        for i in range(move.index, 63, direction):
            if self._valid_square_test(i, piece.color):
                target_moves.append(i)
        return target_moves

    # TODO: It might be nice to have a way of referring to relative
    # indices. Like using a vector notation to refer to up, down,
    # left, right, diag (1,0), (1,1), ... Kind of what I had in the
    # previous version. It could also be nice to have a
    # "validate_X_path" which would return the list of valid empty
    # spaces along that path.

    # TODO: I'll need to make sure a move doesn't put me into
    # check. Perhaps after I get my list of "target_moves" I can
    # iterate through and check whether any of these moves will leave
    # me in check.
    def get_valid_moves(self, moveinput):
        """Given a move input, return a list of possible moves.

        I do move validation based on the relative position of
        moves. Here is an example of a relative grid:

         +14 +15 +16 +17 +18
         +06 +07 +08 +09 +10
         -02 -01 000 +01 +02
         -10 -09 -08 -07 -06
         -18 -17 -16 -15 -14

        """
        move = Move(moveinput)
        piece = self.board.get(move)

        target_moves = []
        if piece is None:
            return target_moves

        piecetype = type(piece)
        target_moves = self._dispatch_piecetype_validation[piecetype](move,
                                                                      piece)

    def _get_valid_moves_pawn(self, move: Move, piece: p.Piece):
        """."""
        # TODO: Include en passant and promotion. For promotion, I can
        # probably just set the promotion flag and then elsewhere will
        # be a check for promotion. Lol nvm, this will happen
        # elsewhere bc i'm just appending to a list of valid moves.
        target_moves = []

        relative_indices = [8]
        if not piece.has_moved:
            relative_indices += [16]
        for d_i in relative_indices:
            testindex = move.index + d_i
            if self._valid_square_test(testindex, piece):
                target_moves.append(testindex)
        return target_moves

    def _get_valid_moves_knight(self, move: Move, piece: p.Piece):
        """."""
        target_moves = []

        relative_indices = [-6, 10, 17, 15, 6, -10, -17, -15]
        for d_i in relative_indices:
            testindex = move.index + d_i
            if self._valid_square_test(testindex, piece):
                target_moves.append(testindex)
        return target_moves

    def _get_valid_moves_bishop(self, move: Move, piece: p.Piece):
        """."""
        target_moves = []

        for direction in [self._northeast,
                          self._northwest,
                          self._southeast,
                          self._southwest]:
            target_moves += self._valid_square_linear_path(move,
                                                           piece,
                                                           direction)

        return target_moves

    def _get_valid_moves_rook(self, move: Move, piece: p.Piece):
        """."""
        target_moves = []

        for direction in [self._north,
                          self._west,
                          self._east,
                          self._south]:
            target_moves += self._valid_square_linear_path(move,
                                                           piece,
                                                           direction)

        return target_moves

    def _get_valid_moves_queen(self, move: Move, piece: p.Piece):
        """."""
        target_moves = []

        for direction in [self._northeast,
                          self._northwest,
                          self._southeast,
                          self._southwest,
                          self._north,
                          self._west,
                          self._east,
                          self._west]:
            target_moves += self._valid_square_linear_path(move,
                                                           piece,
                                                           direction)

        return target_moves

    def _get_valid_moves_king(self, move: Move, piece: p.Piece):
        """."""
        target_moves = []
        relative_indices = [7, 8, 9, -1, 1, -9, -8, -7]

        for d_i in relative_indices:
            testindex = move.index + d_i
            if self._valid_square_test(testindex,
                                       piece.color):
                target_moves.append(testindex)
        return target_moves

    def valid_index(self, index):
        """."""
        if index < 0 or index > 63:
            return False
        return True
