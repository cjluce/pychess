"""."""

from board import Board
from move import Move
import piece as p


class ChessEngine:
    """."""

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
        target_moves = self._dispatch_piecetype_validation[piecetype](move, piece)

    def _get_valid_moves_pawn(self, move: Move, piece: p.Piece):
        """."""
        pass

    def _get_valid_moves_knight(self, move: Move, piece: p.Piece):
        """."""
        target_moves = []

        relative_indices = [-6, 10, 17, 15, 6, -10, -17, -15]
        for d_i in relative_indices:
            testindex = move.index + d_i
            if not self.valid_index(testindex):
                continue
            testpiece = self.board.get(testindex)
            if testpiece is None:
                target_moves.append(testindex)
            elif piece.color == testpiece.oppositecolor:
                target_moves.append(testindex)

    def _get_valid_moves_bishop(self, move: Move, piece: p.Piece):
        """."""
        pass

    def _get_valid_moves_rook(self, move: Move, piece: p.Piece):
        """."""
        pass

    def _get_valid_moves_queen(self, move: Move, piece: p.Piece):
        """."""
        pass

    def _get_valid_moves_king(self, move: Move, piece: p.Piece):
        """."""
        pass

    def valid_index(self, index):
        """."""
        if index < 0 or index > 63:
            return False
        return True
