from muscad import Part, Cylinder, Volume
from muscad.vitamins.bolts import Bolt


class DryingRackFix(Part):
    """A reinforcement part for my cheap drying rack made with welded tubes.

    This will keep a tube perdendicular to the other one even after the welding snapped.

    """

    vertical_tube = ~Cylinder(d=13, h=60).debug()
    horizontal_tube = (
        ~Cylinder(d=13, h=60)
        .bottom_to_left()
        .align(
            left=vertical_tube.center_x,
            center_y=vertical_tube.center_y,
            center_z=vertical_tube.center_z,
        )
        .debug()
    )

    left_bolt = (
        ~Bolt.M3(12, head_clearance=10)
        .add_nut(-1, inline_clearance_size=10, angle=180)
        .bottom_to_back()
        .align(
            right=vertical_tube.left - 1,
            center_y=vertical_tube.center_y,
            center_z=horizontal_tube.center_z,
        )
    )
    top_bolt = (
        ~Bolt.M3(12, head_clearance=10)
        .add_nut(-1, inline_clearance_size=10, angle=180)
        .bottom_to_back()
        .align(
            left=vertical_tube.right + 3,
            center_y=vertical_tube.center_y,
            bottom=horizontal_tube.top + 1,
        )
    )
    bottom_bolt = (
        ~Bolt.M3(12, head_clearance=10)
        .add_nut(-1, inline_clearance_size=10, angle=180)
        .bottom_to_back()
        .align(
            left=vertical_tube.right + 3,
            center_y=vertical_tube.center_y,
            top=horizontal_tube.bottom - 1,
        )
    )

    reinforcement = (
        Volume(
            left=left_bolt.left - 1,
            right=top_bolt.right + 1,
            front=vertical_tube.front + 2,
            back=vertical_tube.back - 2,
            bottom=bottom_bolt.bottom - 1,
            top=top_bolt.top + 1,
        )
        .fillet_depth(4, right=True)
        .fillet_depth(14, left=True)
    )


drying_rack_fix_bottom, drying_rack_fix_top = (
    DryingRackFix().back_to_bottom().align(center_z=0).divide(z=0, T=0.2)
)

drying_rack_fix_bottom.render_to_file("drying_rack_fix_bottom.scad")
drying_rack_fix_top.render_to_file("drying_rack_fix_top.scad")


# drying_rack_fix_top.export_stl("drying_rack_fix_top.scad")


class DryingRackFoot(Part):
    """A replacement foot for that same drying rack.

    It initially had wheels but one of them feel and got lost.

    """

    vertical_tube = ~Cylinder(d=13.8, h=60).debug()
    feet = Cylinder(d=24, d2=18, h=60).align(top=vertical_tube.bottom + 20)
    bolt = (
        ~Bolt.M3(20)
        .add_nut(-2)
        .bottom_to_left()
        .align(
            center_x=vertical_tube.center_x + 2,
            center_y=vertical_tube.center_y,
            center_z=feet.top - 10,
        )
        .debug()
    )


drying_rack_foot = DryingRackFoot()
drying_rack_foot.render_to_file()
