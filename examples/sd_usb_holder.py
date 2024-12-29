from muscad import Cylinder, E, Part, Volume


class SdUsbHolder(Part):
    usb_holes = ~Volume(width=12.8, depth=5.4, height=16).reverse_chamfer_top(left=True, right=True).array(
        5, y=10
    ).array(2, x=-24)

    usb_part = (
        Volume(
            right=usb_holes.right + 3,
            left=usb_holes.left - 3,
            back=usb_holes.back,
            front=usb_holes.front + 3,
            bottom=usb_holes.bottom - 2,
            top=usb_holes.top - E,
        )
        .fillet_depth(r=3, top=True)
        .root()
    )

    sd_holes = ~Volume(
        right=usb_holes.right,
        width=25,
        front=usb_part.back - 3,
        depth=2.8,
        height=15,
        top=usb_holes.top,
    ).reverse_chamfer_top(left=True, right=True).array(4, y=-4.8).array(2, x=-30)
    sd_part = (
        Volume(
            left=sd_holes.left - 3,
            right=sd_holes.right + 3,
            back=sd_holes.back - 3,
            front=sd_holes.front + 3,
            bottom=usb_part.bottom,
            top=sd_holes.top - E,
        )
        .fillet_depth(r=3, top=True)
        .fillet_height(3, back=True)
    )

    fixing_holes = (
        Volume(
            left=sd_part.left, width=8, back=sd_part.back + 3, front=sd_part.back - 7, bottom=sd_part.bottom, height=4
        ).fillet_height(3, back=True)
        - Cylinder(d=3, h=5).align(center_x=sd_part.left + 4, center_y=sd_part.back - 4, bottom=sd_part.bottom - E)
    ).x_symmetry(sd_part.center_x)

    usbc_holes = ~Volume(
        right=usb_holes.right,
        width=8.8,
        back=usb_part.front + 3,
        depth=2.8,
        top=usb_holes.top - 8,
        height=9,
    ).fillet_height(1).array(3, x=-14)

    usbc_part = Volume(
        right=usb_part.right,
        left=usb_part.left,
        back=usb_part.front,
        front=usbc_holes.front + 3,
        bottom=usb_part.bottom,
        top=usbc_holes.top - E,
    ).fillet_height(3, right=True, front=True)

    microsd_holes = ~Volume(
        left=sd_holes.left,
        width=11.6,
        back=sd_part.front + 4,
        depth=1.3,
        top=usbc_holes.top,
        height=8,
    ).reverse_chamfer_top(left=True, right=True).array(9, y=6)

    microsd_part = (
        Volume(
            left=sd_part.left,
            right=usb_part.left,
            back=sd_part.front,
            front=usbc_part.front,
            bottom=sd_part.bottom,
            top=microsd_holes.top - E,
        )
        .fillet_depth(3, top=True, left=True)
        .fillet_height(3, front=True, left=True)
        # .reverse_fillet_right(top=True)
    )


SdUsbHolder().render_to_file(openscad=False)
