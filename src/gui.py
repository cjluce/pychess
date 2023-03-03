"""."""
import dearpygui.dearpygui as dpg

# Piece images taken from:
# https://commons.wikimedia.org/wiki/Category:SVG_chess_pieces
# /home/lucec/code/python/pychess/assets/pieces/black_king.png

dpg.create_context()

imcolors = ["white", "black"]
impieces = ["bishop", "king", "knight", "pawn", "queen", "rook"]
imtags = []

for imcolor in imcolors:
    for impiece in impieces:
        imtag = f"{imcolor}_{impiece}"
        imtags.append(imtag)

        imdata = dpg.load_image(
            f"../assets/pieces/{imtag}.png"
        )  # 0:widths,1:heights,2:channels,3:data

        with dpg.texture_registry():
            dpg.add_dynamic_texture(width=imdata[0],
                                    height=imdata[1],
                                    default_value=imdata[3],
                                    tag=f"{imtag}")

size = 510
with dpg.window(label="PyChess"):
    with dpg.drawlist(width=size, height=size):
        # This is kind of a fun way to define the colors for now.
        light = (243, 205, 170)
        dark = tuple([255 - light[i] for i in range(3)])
        line = tuple([(light[i] - dark[i]) / 2 for i in range(3)])

        color, oppcolor = light, dark
        for xmin in range(0, 400, 50):
            for ymin in range(0, 400, 50):
                dpg.draw_rectangle((xmin, ymin),
                                   (xmin + 50, ymin + 50),
                                   fill=color,
                                   color=line,
                                   thickness=10)
                color, oppcolor = oppcolor, color
            color, oppcolor = oppcolor, color

            # dpg.draw_image("black_bishop", (0, 0), (45, 45))
        s = 0
        for p in impieces:
            dpg.draw_image(f"black_{p}", (s, 0), (s + 45, 45))
            s += 50

dpg.create_viewport(title='PyChess', width=size, height=size)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
