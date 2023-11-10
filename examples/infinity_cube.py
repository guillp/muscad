from muscad import TT, Part, Volume


class Frame(Part):
    mirror_x = ~Volume(width=300 + TT, height=300 + TT, depth=3 + TT, left=5)
    mirror_y = ~Volume(depth=300 + TT, height=300 + TT, width=3 + TT, back=5)

    outer_shell = (
        Volume(width=20, depth=20, height=300)
        .chamfer_height(5, left=True, back=True)
        .chamfer_height(10, right=True, front=True)
        .align(left=mirror_y.left - 3, back=mirror_x.back - 3)
    )
    cable_hole = (
        ~Volume(
            width=10,
            depth=10,
            height=300 + TT,
            left=mirror_y.right + 2,
            back=mirror_x.front + 2,
        )
        .chamfer_height(2, left=True, back=True)
        .chamfer_height(9, right=True, front=True)
    )


if __name__ == "__main__":
    Frame().render_to_file()
