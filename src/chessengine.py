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
    _southwest = -9

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

    def _get_board(self, board: Board) -> Board:
        """."""
        if board is None:
            return self.board
        return board

    # TODO: I think I'll need to add a color here.
    def is_board_check(self, board: Board, color: p.EnumColor):
        """Check whether the board is currently in check."""
        board = self._get_board(board)

        return False

    # TODO: This method is preliminary as I debate the best way to set
    # it up.
    def move(self, piece: p.Piece, movefrom: Move, moveto: Move, validmoves,
             board: Board = None):
        """."""
        if moveto.index not in validmoves:
            "You tried to make an invalid move."
            return False

        # Pawn requires en passant checking, king and rook require
        # castle checking. Everything else just moves and takes.
        if isinstance(piece, p.Pawn):
            enpassant = False
            piece.has_moved = True
            if enpassant:
                return True
        if isinstance(piece, p.Rook):
            castlecondition = False
            piece.has_moved = True
            if castlecondition:
                return True
        if isinstance(piece, p.King):
            castlecondition = False
            piece.has_moved = True
            if castlecondition:
                return True

        board.set(movefrom, None)
        board.set(moveto, piece)

        return True

    def _valid_square_test(self, testindex, color: p.EnumColor,
                           board: Board = None):
        """."""
        board = self._get_board(board)

        if not self.valid_index(testindex):
            return 0
        testpiece = board.get(Move(testindex))
        if testpiece is None:
            return 1
        elif testpiece.oppositecolor == color:
            return 2
        return 0

    def _valid_lag_distance(self, ind0, ind1):
        file0, rank0 = divmod(ind0, 8)
        file1, rank1 = divmod(ind1, 8)

        if abs(file1 - file0) > 1:
            return False
        if abs(rank1 - rank0) > 1:
            return False
        return True

    def _valid_square_linear_path(self,
                                  move: Move,
                                  piece: p.Piece,
                                  direction):
        """."""
        target_moves = []

        ind0, ind1 = move.index, move.index
        i = move.index

        while i >= 0 and i <= 63:
            i += direction
            ind1 = i
            if not self._valid_lag_distance(ind0, ind1):
                break
            ind0, ind1 = ind1, ind0
            status = self._valid_square_test(i, piece.color)
            if status:
                target_moves.append(i)
                if status == 2:
                    break
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

    def _get_valid_moves_pawn(self, move: Move, piece: p.Piece,
                              board: Board = None):
        """."""
        # TODO: Include en passant and promotion. For promotion, I can
        # probably just set the promotion flag and then elsewhere will
        # be a check for promotion. Lol nvm, this will happen
        # elsewhere bc i'm just appending to a list of valid moves.

        board = self._get_board(board)

        target_moves = []

        direction = 1 if piece.color == p.EnumColor.WHITE else -1

        relative_indices = [8]
        if not piece.has_moved:
            relative_indices += [16]
        relative_indices = [i * direction for i in relative_indices]
        for d_i in relative_indices:
            testindex = move.index + d_i
            if not self.valid_index(testindex):
                break
            testpiece = board.get(Move(testindex))
            if testpiece is None:
                target_moves.append(testindex)
            else:
                break
        possible_attacks = [self._northeast, self._northwest]
        possible_attacks = [i * direction for i in possible_attacks]
        for d_i in possible_attacks:
            testindex = move.index + d_i
            if not self._valid_lag_distance(move.index, testindex):
                continue
            if not self.valid_index(testindex):
                continue
            testpiece = board.get(Move(testindex))
            if testpiece is None:
                continue
            if testpiece.oppositecolor == piece.color:
                target_moves.append(testindex)
        # TODO: Add in en passant logic
        return target_moves

    def _get_valid_moves_knight(self, move: Move, piece: p.Piece,
                                board: Board = None):
        """."""
        board = self._get_board(board)

        target_moves = []

        # Knights require some extra move validation in the case of
        # edge wrapping.
        # As it turns out, divmod(index, 8) will produce a tuple with
        # (. // 8, . % 8).
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
            if self._valid_square_test(testindex, piece.color):
                target_moves.append(testindex)
        return target_moves

    def _get_valid_moves_bishop(self, move: Move, piece: p.Piece,
                                board: Board = None):
        """."""
        board = self._get_board(board)

        target_moves = []

        for direction in [self._northeast,
                          self._northwest,
                          self._southeast,
                          self._southwest]:
            target_moves += self._valid_square_linear_path(move,
                                                           piece,
                                                           direction)
        return target_moves

    def _get_valid_moves_rook(self, move: Move, piece: p.Piece,
                              board: Board = None):
        """."""
        board = self._get_board(board)

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
                          self._south]:
            target_moves += self._valid_square_linear_path(move,
                                                           piece,
                                                           direction)
        return target_moves

    def _get_valid_moves_king(self, move: Move, piece: p.Piece,
                              board: Board = None):
        """."""
        board = self._get_board(board)

        target_moves = []
        relative_indices = [self._northeast,
                            self._northwest,
                            self._southeast,
                            self._southwest,
                            self._north,
                            self._west,
                            self._east,
                            self._south]

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
