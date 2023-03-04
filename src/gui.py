"""."""
import pyglet
from pyglet.window import mouse
from pyglet.sprite import Sprite
from pyglet.resource import image
from pyglet import shapes


pyglet.resource.path = ['../assets']
pyglet.resource.reindex()

window = pyglet.window.Window()
boardbatch = pyglet.graphics.Batch()
piecebatch = pyglet.graphics.Batch()

# image = image("pieces/white_queen.png")

tags = [f"{imc}_{imp}"
        for imc in ["white", "black"]
        for imp in ["bishop", "king", "knight", "pawn", "queen", "rook"]]
images = {}
for tag in tags:
    images[tag] = image(f"pieces/{tag}.png", )

# sprites = [
#     Sprite(
#         image(f"pieces/{tag}.png"),
#         batch=piecebatch)
#     for tag in tags]

squares = []
lightcolor = (249, 208, 170)
darkcolor = tuple([255 - c for c in lightcolor])
curcolor, oppcolor = darkcolor, lightcolor
boardtopixel = []
for y in range(0, 400, 50):
    for x in range(0, 400, 50):
        squares.append(shapes.Rectangle(x=x,
                                        y=y,
                                        width=50,
                                        height=50,
                                        color=curcolor,
                                        batch=boardbatch))
        curcolor, oppcolor = oppcolor, curcolor
        boardtopixel.append((x, y))
    curcolor, oppcolor = oppcolor, curcolor

pixeltoboard = {}
for pixel_index in range(len(boardtopixel)):
    pixel = boardtopixel[pixel_index]
    pixeltoboard[pixel] = pixel_index

import board
b = board.Board()
sprites = []
for piece_index in range(len(b.board)):
    piece = b.board[piece_index]
    if piece is None:
        continue
    print(piece.tag)
    sprites.append(
        Sprite(
            image(f"pieces/{piece.tag}.png"),
            x=boardtopixel[piece_index][0],
            y=boardtopixel[piece_index][1],
            batch=piecebatch)
    )


@window.event
def on_mouse_press(x, y, button, modifiers):
    """."""
    if button == mouse.LEFT:
        print('The left mouse button was pressed.')


def between(testval, val1, val2):
    """."""
    if val1 <= testval and testval <= val2:
        return True
    return False


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    """."""
    if buttons & mouse.LEFT:
        sprite = None
        for sp in sprites:
            if not between(x, sp.x, sp.x + 50):
                continue
            if not between(y, sp.y, sp.y + 50):
                continue
            sprite = sp
            break
        if sprite is None:
            return False
        sprite.x += dx
        sprite.y += dy


@window.event
def on_draw():
    """."""
    window.clear()
    # image.blit(window.width//2, window.height//2)
    boardbatch.draw()
    piecebatch.draw()


pyglet.app.run()
