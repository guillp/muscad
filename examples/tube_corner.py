from muscad import E, Hull, Part, T, Tube, Volume
from muscad.vitamins.bolts import Bolt


class TubeCorner(Part):
    tube1 = ~Tube(diameter=19.5, height=45).bottom_to_back()
    tube2 = ~Tube(diameter=19.5, height=45).bottom_to_left().align(
        left=tube1.right, front=tube1.back, center_z=tube1.center_z
    )

    holder1 = (
        Tube(diameter=23, height=37)
        .bottom_to_back()
        .align(center_x=tube1.center_x, back=tube1.back, center_z=tube1.center_z)
    )
    holder2 = (
        Tube(diameter=23, height=37)
        .bottom_to_left()
        .align(left=tube2.left, center_y=tube2.center_y, center_z=tube2.center_z)
    )
    joiner = (
        Volume(
            left=holder1.left,
            right=holder1.right,
            back=holder2.back,
            front=holder1.back,
            bottom=holder2.bottom,
            top=holder2.top,
        )
        .fillet_depth(23 / 2, left=True)
        .fillet_width(23 / 2, back=True)
    )

    bolt = (
        ~Bolt.M3(16, head_clearance=10)
        .add_nut(-1, inline_clearance_size=16)
        .align(right=joiner.right - 3, front=joiner.front - 3, bottom=joiner.bottom + 1)
        .debug()
    )


part1, part2 = TubeCorner().divide(z=0)

part1.top_to_bottom().render_to_file("tube_corner_part1")
part2.render_to_file("tube_corner_part2")


class TubeCornerV2(Part):
    _joiner = Volume(width=24, depth=24, height=24)
    tube_x = ~Tube(diameter=19.5, height=45).bottom_to_left().align(
        left=_joiner.right, center_y=_joiner.center_y, center_z=_joiner.center_z
    )
    _holder_x = (
        Tube(diameter=24, height=37)
        .bottom_to_left()
        .align(left=tube_x.left, center_y=tube_x.center_y, center_z=tube_x.center_z)
    )
    body = Hull(_joiner, _holder_x)

    top_clearance = ~Volume(
        left=_joiner.left - E,
        right=_joiner.right + E,
        back=_joiner.back - E,
        front=_joiner.front + E,
        top=_joiner.top + E,
        height=_joiner.height / 3 + T,
    )
    middle_clearance = ~Volume(
        width=34, depth=34, height=_joiner.height / 3 - T, center_x=_joiner.left, center_y=_joiner.front
    ).z_rotate(45, center_x=_joiner.left, center_y=_joiner.front)
    bolt1 = ~Bolt.M3(16, head_clearance=10).add_nut(-1, inline_clearance_size=10).align(
        right=_joiner.right - 3, back=_joiner.back + 3, bottom=_joiner.bottom + 1
    )
    bolt2 = ~Bolt.M3(16, head_clearance=10).add_nut(-1, inline_clearance_size=10).bottom_to_top().align(
        left=_joiner.left + 3, front=_joiner.front - 3, bottom=_joiner.bottom + 1
    )


TubeCornerV2().render_to_file("tube_corner_v2")
