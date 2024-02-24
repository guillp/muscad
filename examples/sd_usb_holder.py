from muscad import E, Part, Volume


class SdUsbHolder(Part):
    sd_part = Volume(width=60, depth=30, height=16).fillet_depth(r=4, top=True)
    sd_holes = ~Volume(
        left=sd_part.center_x + 3,
        width=25,
        back=sd_part.back + 1.6,
        depth=2.8,
        bottom=sd_part.bottom + 2,
        top=sd_part.top + E,
    ).reverse_chamfer_top(left=True, right=True).array(6, y=4.8).x_symmetry(sd_part.center_x)
    usb_part = Volume(
        right=sd_part.right, width=40, back=sd_part.front, depth=80, bottom=sd_part.bottom, height=16
    ).fillet_depth(r=4, top=True)
    usb_holes = ~Volume(
        left=usb_part.center_x + 4, width=13, back=usb_part.back + 1, depth=6, top=usb_part.top + E, height=13
    ).reverse_chamfer_top(left=True, right=True).array(8, y=10).x_symmetry(usb_part.center_x)
    microsd_part = (
        Volume(
            left=sd_part.left,
            right=usb_part.left,
            back=sd_part.front,
            front=usb_part.front,
            bottom=sd_part.bottom,
            height=10,
        )
        .fillet_depth(4, top=True, left=True)
        .reverse_fillet_right(top=True)
    )
    microsd_holes = ~Volume(
        center_x=microsd_part.center_x,
        width=12,
        back=microsd_part.back + 3,
        depth=1.4,
        bottom=usb_part.bottom + 2,
        top=microsd_part.top + E,
    ).reverse_chamfer_top(left=True, right=True).array(10, y=8)


SdUsbHolder().render_to_file(openscad=False)
