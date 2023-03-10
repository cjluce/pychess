"""."""
import pyglet
from pyglet.window import mouse
from pyglet.sprite import Sprite
from pyglet.resource import image
from pyglet import shapes
import board
from move import Move
from chessengine import ChessEngine


class ChessGUI(pyglet.window.Window):
    """."""

    def __init__(self):
        """."""
        super(ChessGUI, self).__init__(600,
                                       600,
                                       resizable=False,
                                       caption='Chess',
                                       config=pyglet.gl.Config(
                                        double_buffer=True
                                       ))
        self.moving_piece = False
        self.move_from = -1

        self.boardbatch = pyglet.graphics.Batch()
        self.piecebatch = pyglet.graphics.Batch()
        self.movesbatch = pyglet.graphics.Batch()

        # TODO: All of this should be in initialization functions....
        self.tags = [f"{imc}_{imp}"
                     for imc in ["white", "black"]
                     for imp in ["bishop", "king",
                                 "knight", "pawn",
                                 "queen", "rook"]]
        self.images = {}
        for tag in self.tags:
            self.images[tag] = image(f"pieces/{tag}.png", )

        self.squares = []
        lightcolor = (249, 208, 170)
        darkcolor = tuple([255 - c for c in lightcolor])
        curcolor, oppcolor = darkcolor, lightcolor
        self.boardtopixel = []
        for y in range(0, 400, 50):
            for x in range(0, 400, 50):
                self.squares.append(
                    shapes.Rectangle(x=x,
                                     y=y,
                                     width=50,
                                     height=50,
                                     color=curcolor,
                                     batch=self.boardbatch))
                curcolor, oppcolor = oppcolor, curcolor
                self.boardtopixel.append((x, y))
            curcolor, oppcolor = oppcolor, curcolor

        self.pixeltoboard = {}
        for pixel_index in range(len(self.boardtopixel)):
            pixel = self.boardtopixel[pixel_index]
            self.pixeltoboard[pixel] = pixel_index

        self.b = board.Board()
        self.engine = ChessEngine(self.b)
        self.b.init_board()
        self.render_pieces()

    def piecestr_to_tag(self, piecestr):
        """."""
        colorstr = piecestr[0]
        chessstr = piecestr[1]
        color = ""
        if colorstr == "W":
            color = "white"
        else:
            color = "black"
        piecestr_to_tag = {"P": "pawn",
                           "B": "bishop",
                           "N": "knight",
                           "R": "rook",
                           "Q": "queen",
                           "K": "king"}
        return f"{color}_{piecestr_to_tag[chessstr]}"

    def render_pieces(self):
        """."""
        self.sprites = []
        # print(self.b.pieces.items())
        for loc, piece in self.b.pieces.items():
            if piece is None:
                continue
            # print(piece.tag)
            self.sprites.append(
                Sprite(
                    image(f"pieces/{self.piecestr_to_tag(str(piece))}.png"),
                    x=self.boardtopixel[loc][0],
                    y=self.boardtopixel[loc][1],
                    batch=self.piecebatch)
            )

    def render_moves(self, moves):
        """."""
        self.validmoves = []
        for loc in moves:
            boarderpix = self.boardtopixel[loc]
            self.validmoves.append(
                shapes.Rectangle(
                    x=boarderpix[0],
                    y=boarderpix[1],
                    width=50,
                    height=50,
                    color=(0, 255, 0),
                    batch=self.movesbatch)
            )

    # @window.event
    def on_draw(self):
        """."""
        window.clear()
        # image.blit(window.width//2, window.height//2)
        self.render_pieces()
        self.boardbatch.draw()
        self.movesbatch.draw()
        self.piecebatch.draw()

    # @window.event
    def on_mouse_release(self, x, y, button, modifiers):
        """."""
        # TODO: Right click should probably unset the "moving_piece"
        # flag
        if button == mouse.LEFT:
            print('The left mouse button was release.')
            self.handle_click(x, y)

    def handle_click(self, x, y):
        """."""
        if self.moving_piece:
            self.validmoves = []
            square = self.get_square(x, y)
            if square is None:
                self.moving_piece, self.move_from = False, -1
                return
            if square not in self.moves:
                self.moving_piece, self.move_from = False, -1
                return
            self.engine.move(self.movingpiece,
                             Move(self.move_from),
                             Move(square),
                             self.moves,
                             self.b)
            # self.b.move(self.move_from, square)
            self.moving_piece, self.move_from = False, -1
            return
        square = self.get_square(x, y)
        if square is None:
            pass
        piece = self.b.get(Move(square))
        if piece is None:
            return
        print("Moving: ", piece)
        self.movingpiece = piece
        self.moves = self.engine.get_valid_moves(square)
        self.render_moves(self.moves)
        self.moving_piece = True
        self.move_from = square
        print(self.b)

    def get_square(self, x, y):
        """Get the internal board square from a square region."""
        point = (50 * (x // 50), 50 * (y // 50))
        if point in self.pixeltoboard:
            return self.pixeltoboard[point]
        return None

    def between(testval, val1, val2):
        """."""
        if val1 <= testval and testval <= val2:
            return True
        return False

    def update(self, dt):
        """."""
        self.on_draw()


if __name__ == "__main__":
    pyglet.resource.path = ['../assets']
    pyglet.resource.reindex()
    window = ChessGUI()
    # pyglet.clock.schedule_interval(window.update, 1000.)
    pyglet.app.run()
