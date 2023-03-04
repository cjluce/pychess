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


def change_text(sender, app_data):
    """."""
    dpg.set_value("mouseloc", f"Mouse Location: {app_data}")


# with dpg.handler_registry():
    # dpg.add_mouse_move_handler(callback=change_text)
#     dpg.add_mouse_drag_handler(callback=change_text)

with dpg.item_handler_registry(tag="widget handler") as handler:
    dpg.add_item_clicked_handler(callback=change_text)

size = 510
with dpg.window(label="PyChess"):
    dpg.add_text("Mouse Location", tag="mouseloc")
    with dpg.drawlist(width=size, height=size):
        # This is kind of a fun way to define the colors for now.
        with dpg.draw_layer(tag="board_layer"):

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
        s = 0
        for p in impieces:
            t = f"black_{p}"
            dpg.draw_image(t, (s, 0), (s + 45, 45), tag=f"_{t}")
            s += 50


# TODO: Map each square to a coordinate root

dpg.bind_item_handler_registry("mouseloc", "widget handler")

dpg.create_viewport(title='PyChess', width=size, height=size)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
