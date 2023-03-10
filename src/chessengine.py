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
            "<class 'piece.Pawn'>": self._get_valid_moves_pawn,
            "<class 'piece.Knight'>": self._get_valid_moves_knight,
            "<class 'piece.Bishop'>": self._get_valid_moves_bishop,
            "<class 'piece.Rook'>": self._get_valid_moves_rook,
            "<class 'piece.Queen'>": self._get_valid_moves_queen,
            "<class 'piece.King'>": self._get_valid_moves_king
        }

    # TODO: I think I'll need to add a color here.
    def is_board_check(self, board: Board):
        """Check whether the board is currently in check."""
        pass

    def _valid_square_test(self, testindex, color: p.EnumColor):
        """."""
        if not self.valid_index(testindex):
            return False
        testpiece = self.board.get(Move(testindex))
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

        i = move.index
        while i > 0 and i < 63:
        # for i in range(move.index, 63, direction):
            i += direction
            if self._valid_square_test(i, piece.color):
                target_moves.append(i)
            else:
                break
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

        # TODO: I want to use my dispatcher, but it is currently broken.
        if isinstance(piece, p.Pawn):
            print("Pawn")
            target_moves = self._get_valid_moves_pawn(move, piece)
        if isinstance(piece, p.Bishop):
            print("Bishop")
            target_moves = self._get_valid_moves_bishop(move, piece)
        elif isinstance(piece, p.Knight):
            print("Knight")
            target_moves = self._get_valid_moves_knight(move, piece)
        elif isinstance(piece, p.Rook):
            print("Rook")
            target_moves = self._get_valid_moves_rook(move, piece)
        elif isinstance(piece, p.Queen):
            print("Queen")
            target_moves = self._get_valid_moves_queen(move, piece)
        elif isinstance(piece, p.King):
            print("King")
            target_moves = self._get_valid_moves_king(move, piece)
        # piecetype = str(type(piece))
        # print(piecetype in self._dispatch_piecetype_validation, piecetype)
        # print(self._dispatch_piecetype_validation.keys())
        # target_moves = self._dispatch_piecetype_validation[piecetype](move,
        #                                                               piece)
        return target_moves

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

        # Knights require some extra move validation in the case of
        # edge wrapping.
        piecerank = (move.index % 8) + 1
        piecefile = (move.index // 8) + 1
        relative_indices = [-6, 10, 17, 15, 6, -10, -17, -15]
        for d_i in relative_indices:
            testindex = move.index + d_i
            testrank = (testindex % 8) + 1
            testfile = (testindex // 8) + 1
            if abs(testrank - piecerank) > 2:
                continue
            if abs(testfile - piecefile) > 2:
                continue
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
