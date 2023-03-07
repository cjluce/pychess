"""."""
import pyglet
from pyglet.window import mouse
from pyglet.sprite import Sprite
from pyglet.resource import image
from pyglet import shapes
import board


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
        self.render_pieces()

    def render_pieces(self):
        """."""
        self.sprites = []
        # print(self.b.pieces.items())
        for piece, loc in self.b.pieces.items():
            if piece is None:
                continue
            # print(piece.tag)
            self.sprites.append(
                Sprite(
                    image(f"pieces/{piece.tag}.png"),
                    x=self.boardtopixel[loc][0],
                    y=self.boardtopixel[loc][1],
                    batch=self.piecebatch)
            )

    # @window.event
    def on_draw(self):
        """."""
        window.clear()
        # image.blit(window.width//2, window.height//2)
        self.render_pieces()
        self.boardbatch.draw()
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
            square = self.get_square(x, y)
            if square is None:
                pass
            self.b.move(self.move_from, square)
            self.moving_piece, self.move_from = False, -1
            return
        square = self.get_square(x, y)
        if square is None:
            pass
        piece = self.b.get(square)
        if piece is None:
            return
        print("Moving: ", piece.tag)
        self.moving_piece = True
        self.move_from = square

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
