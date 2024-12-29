from muscad import Import, Part, Volume


class SpoolClamp(Part):
    z_extrusion = (
        ~Volume(left=2, width=30, depth=21, bottom=0, top=100)
        .add(
            lambda parent: Volume(
                right=parent.right + 10.5,
                left=parent.right,
                front=parent.front,
                depth=6,
                bottom=parent.bottom,
                top=parent.top,
            )
        )
        .remove(
            lambda parent: Volume(
                left=parent.left + 25,
                right=parent.right + 5,
                back=parent.back + 3,
                front=parent.front - 4.5,
                bottom=parent.bottom - 1,
                top=parent.top + 1,
            )
        )
        .debug()
    )

    base = ~Volume(left=0, width=2, depth=40, top=0, height=34).add_cylindrical_side_x(h=1, bottom=True)


(
    (
        SpoolClamp()
        + Import("/home/guillaume/Téléchargements/compact spool repositioner v2 flat.stl")
        .z_rotate(180)
        .y_rotate(180)
        .translate(x=-100, y=102, z=50)
        .background()
    ).render_to_file("spool_clamp")
)
