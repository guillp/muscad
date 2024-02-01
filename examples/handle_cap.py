from muscad import Cylinder, E, Part, Text, Volume


class FilletMeasurement(Part):
    body = (
        Volume(width=50, depth=50, height=2)
        .fillet_height(6, right=True, front=True)
        .fillet_height(7, right=True, back=True)
        .fillet_height(8, left=True, back=True)
        .fillet_height(9, left=True, front=True)
    )

    l6 = (
        Text("6", size=4, halign="center", valign="center")
        .z_rotate(-45)
        .align(
            center_x=body.right - 4,
            center_y=body.front - 4,
        )
        .z_linear_extrude(1, bottom=body.top)
    )
    l7 = (
        Text("7", size=4, halign="center", valign="center")
        .z_rotate(-135)
        .align(center_x=body.right - 4, center_y=body.back + 4)
        .z_linear_extrude(1, bottom=body.top)
    )
    l8 = (
        Text("8", size=4, halign="center", valign="center")
        .z_rotate(135)
        .align(
            center_x=body.left + 4,
            center_y=body.back + 4,
        )
        .z_linear_extrude(1, bottom=body.top)
    )
    l9 = (
        Text("9", size=4, halign="center", valign="center")
        .z_rotate(45)
        .align(center_x=body.left + 4.5, center_y=body.front - 4.5)
        .z_linear_extrude(1, bottom=body.top)
    )

    d13 = ~Cylinder(d=13 * 2, h=body.width + 1).align(
        center_x=body.center_x, center_y=body.front + 3, center_z=body.center_z
    )
    l13 = (
        Text("13", size=4, halign="center", valign="center")
        .align(center_x=d13.center_x, center_y=d13.back - 2)
        .z_linear_extrude(1, bottom=body.top)
    )

    d14 = ~Cylinder(d=14 * 2, h=body.width + 1).align(
        center_x=body.right + 3, center_y=body.center_y, center_z=body.center_z
    )
    l14 = (
        Text("14", size=4, halign="center", valign="center")
        .front_to_right()
        .align(center_x=d14.left - 2, center_y=d14.center_y)
        .z_linear_extrude(1, bottom=body.top)
    )
    d15 = ~Cylinder(d=15 * 2, h=body.width + 1).align(
        center_x=body.center_x, center_y=body.back - 3, center_z=body.center_z
    )
    l15 = (
        Text("15", size=4, halign="center", valign="center")
        .front_to_back()
        .align(center_x=d15.center_x, center_y=d15.front + 2)
        .z_linear_extrude(1, bottom=body.top)
    )

    d16 = ~Cylinder(d=16 * 2, h=body.width + 1).align(
        center_x=body.left - 3, center_y=body.center_y, center_z=body.center_z
    )
    l16 = (
        Text("16", size=4, halign="center", valign="center")
        .front_to_left()
        .align(center_x=d16.right + 2, center_y=d16.center_y)
        .z_linear_extrude(1, bottom=body.top)
    )


FilletMeasurement().render_to_file()


class HandleCap(Part):
    bulge = ~Volume(width=27, depth=60, height=9).fillet_height(13)
    handle = ~Cylinder(d=23, h=10).align(center_x=bulge.center_x, center_y=bulge.center_y, bottom=bulge.top - E)

    cap = (
        Volume(
            left=bulge.left - 1.6,
            right=bulge.right + 1.6,
            back=bulge.back - 1.6,
            front=bulge.front + 1.6,
            bottom=bulge.bottom + E,
            top=bulge.top + 2,
        )
        .fillet_height(13)
        .chamfer_depth(2, top=True)
        .chamfer_width(2, top=True)
    )


HandleCap().render_to_file()
