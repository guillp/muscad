from muscad import EE, TT, E, Part, Volume


class MigoLinkSupportSide(Part):
    body = Volume(width=48, depth=40, height=2).fillet_height()
    clips = (
        Volume(width=body.width - 4, depth=4, height=4, center_x=body.center_x, bottom=body.top, back=body.back + 2)
        .fillet_width(2, top=True)
        .fillet_height()
        .y_symmetry(body.center_y)
    )
    cutout = ~Volume(
        width=10 + TT,
        center_x=body.center_x - 8,
        depth=2 + TT,
        center_y=body.center_y,
        center_z=body.center_z,
        height=body.height + EE,
    ).x_symmetry(body.center_x)


left_side = MigoLinkSupportSide()
right_side = MigoLinkSupportSide().bottom_to_top().align(top=left_side.bottom + 147)


class MigoLinkSupportJunction(Part):
    body = Volume(width=38, depth=2, bottom=left_side.body.top, top=right_side.body.bottom)
    arms = (
        Volume(
            width=10 - TT,
            center_x=left_side.center_x - 8,
            depth=2 - TT,
            center_y=body.center_y,
            top=body.bottom,
            height=5,
        )
        .fillet_depth(bottom=True)
        .x_symmetry(body.center_x)
        .z_symmetry(body.center_z)
    )
    gap = ~Volume(
        top=left_side.bottom - TT, height=1, center_x=body.center_x, width=10, center_y=body.center_y, depth=3
    ).z_mirror(body.center_z)
    holes1 = ~Volume(
        width=26, depth=3, height=50, center_x=body.center_x, center_y=body.center_y, top=body.center_z - 10
    ).fillet_depth(4).z_symmetry(body.center_z)
    holes2 = ~Volume(
        width=10, depth=3, height=10, left=body.left - E, center_y=body.center_y, center_z=body.center_z
    ).fillet_depth(right=True).reverse_fillet_left(4, top=True, bottom=True).x_symmetry(body.center_x)


junction = MigoLinkSupportJunction()


class Stop(Part):
    handle = Volume(
        center_x=junction.gap.center_x,
        width=junction.gap.width + 4,
        front=junction.back,
        depth=4,
        center_z=junction.gap.center_z,
        height=1.2,
    ).fillet_height(back=True)
    stop = Volume(
        center_x=junction.gap.center_x,
        width=junction.gap.width,
        back=handle.front,
        depth=5,
        center_z=junction.gap.center_z,
        height=junction.gap.height - TT,
    ).fillet_height(front=True)


stop = Stop()

(left_side + right_side + junction + stop).render_to_file("migo_link")
left_side.render_to_file("migo_side")
junction.front_to_bottom().render_to_file("migo_junction")
