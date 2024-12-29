from muscad import TT, Part, Sphere, Tube, Volume


class Knob(Part):
    BODY_DIAMETER = 35
    BODY_HEIGHT = 3
    SHAFT_DIAMETER = 5.7 + TT + TT
    SHAFT_LENGTH = 11
    SHAFT_FLAT_DEPTH = 1.4 + TT + TT
    KNOB_WIDTH = 10
    KNOB_HEIGHT = 10
    KNOB_ANGLE = 45

    shaft = (
        ~Tube(diameter=SHAFT_DIAMETER, height=SHAFT_LENGTH + 5.8)
        .flatten(SHAFT_FLAT_DEPTH, bottom_offset=3, bottom_chamfer=True, angle=90)
        .fillet_top(2)
        .debug()
    )
    body = Tube(
        diameter=BODY_DIAMETER,
        height=BODY_HEIGHT + 3,
        bottom=shaft.top - 6,
        center_x=shaft.center_x,
        center_y=shaft.center_y,
    ).add_spherical_side(h=3, top=True, segments=200)
    shaft_holder = Tube(
        diameter=SHAFT_DIAMETER + 5,
        center_x=shaft.center_x,
        center_y=shaft.center_y,
        top=body.bottom,
        height=SHAFT_LENGTH,
    ).reverse_fillet_top(4)
    _knob = (
        Volume(
            width=KNOB_WIDTH,
            depth=BODY_DIAMETER,
            height=KNOB_HEIGHT,
            bottom=body.top - 3,
            center_x=body.center_x,
            center_y=body.center_y,
        )
        .add_cylindrical_side_z(d=BODY_DIAMETER, front=True, back=True)
        .add_cylindrical_side_x(h=3, top=True)
    )

    knob = _knob - Sphere(d=5).slide(y=3).align(center_x=_knob.center_x, center_y=_knob.front - 7, top=_knob.top + 1)


Knob().render_to_file()
