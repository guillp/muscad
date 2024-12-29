from muscad import EE, E, Import, Part, Tube, Volume, middle_of
from muscad.vitamins.boards import Board
from muscad.vitamins.bolts import Bolt

T = 0.2
WALL_DEPTH = 2.5
COVER_MARGIN = 1.2
SHIELD_MARGIN = 1.6


class Raspberry4Case(Part):
    raspberry = Board.raspberry_pi_4b().disable()
    box = (
        Volume(
            left=raspberry.left - 5,
            right=raspberry.right + 5,
            back=raspberry.back - 4,
            front=raspberry.front + 4,
            bottom=raspberry.bottom - 5,
            height=42,
        )
        .fillet_height(r=4)
        .remove(
            lambda parent: Volume(
                left=parent.left + WALL_DEPTH,
                right=parent.right - WALL_DEPTH,
                front=parent.front - WALL_DEPTH,
                back=parent.back + WALL_DEPTH,
                bottom=parent.bottom + 2.5,
                top=parent.top + E,
            )
            .fillet_width(r=1, bottom=True)
            .fillet_depth(r=1, bottom=True)
            .fillet_height(r=3)
        )
    )

    cover = ~Volume(
        left=box.left + COVER_MARGIN,
        right=box.right - COVER_MARGIN,
        front=box.front - COVER_MARGIN,
        back=box.back + COVER_MARGIN,
        top=box.top + E,
        height=2,
    ).fillet_height(r=4)

    screws = ~Bolt.M3(6).align(center_x=box.left + 8, center_y=box.back + 8, bottom=box.bottom - E).array(
        2, x=58
    ).array(2, y=49)
    screws_mounts = (
        Tube(diameter=6, height=2.8, center_x=box.left + 8, center_y=box.back + 8, bottom=box.bottom + 2.5)
        .reverse_fillet_bottom(r=1.5)
        .array(2, x=58)
        .array(2, y=49)
    )

    ventilation_holes = ~Volume(
        width=35, depth=7, height=3, left=box.left + 12, back=box.back + 12.5, bottom=box.bottom - E
    ).fillet_height().array(4, y=11).array(2, x=40)

    microsd_slot = ~Volume(
        left=box.left - E, center_y=box.center_y, bottom=box.bottom - E, width=8, depth=13, height=8
    ).fillet_width(r=1, top=True).fillet_height(r=1, right=True)

    usbc_microhdmi_slots = ~Volume(
        left=box.left + 10, width=40, back=box.back - E, depth=3, bottom=box.bottom + 3.5, height=9
    ).fillet_depth(r=1.5)

    jack_slot = ~Tube(diameter=9, height=5).top_to_back().align(
        center_x=box.left + 58.5, back=box.back - E, center_z=box.bottom + 10
    )

    usba_slot1 = ~Volume(
        right=box.right + E, width=2.5, back=box.back + 6, depth=15, bottom=box.bottom + 7, height=16.5
    ).fillet_width(r=1)
    usba_slot2 = ~usba_slot1.forward(18)
    ethernet_slot = ~Volume(
        right=box.right + E, width=3, back=box.back + 41.5, depth=18, bottom=box.bottom + 7, height=14
    ).fillet_width(r=1)

    right_supports = (
        Volume(
            right=box.right - 2,
            width=6,
            center_y=middle_of(usba_slot1.front, usba_slot2.back),
            depth=3,
            bottom=box.bottom + 2.5,
            height=6,
        )
        .remove(
            lambda parent: Volume(
                left=parent.left - E,
                width=2.8,
                depth=parent.depth + EE,
                center_y=parent.center_y,
                top=parent.top + E,
                height=3,
            )
            .reverse_chamfer_top(r=1, right=True)
            .reverse_chamfer_left(r=1, bottom=True)
        )
        .add(lambda parent: parent.forward(18))
    ).debug()

    # left_supports = right_supports.x_mirror(center=box.center_x).forward(1)

    hat_shield_slot = ~Volume(
        left=box.left + 6, width=64, front=box.back + 3, depth=1.6, top=box.top + E, height=28
    ).fillet_depth(r=6, bottom=True).add(
        lambda parent: Volume(
            left=parent.left + SHIELD_MARGIN,
            right=parent.right - SHIELD_MARGIN,
            front=parent.back + E,
            depth=3,
            bottom=parent.bottom + SHIELD_MARGIN,
            top=parent.top,
        ).fillet_depth(r=5, bottom=True)
    )


case = Raspberry4Case()


class Raspberry4Cover(Part):
    cover = (
        Volume(width=case.cover.width - T * 2, depth=case.cover.depth - T * 2, top=case.top - E, height=1.6)
        .fillet_height(r=3.2)
        .add(
            lambda parent: Volume(
                center_x=parent.center_x,
                width=parent.width - 3,
                center_y=parent.center_x,
                depth=parent.depth - 3,
                top=parent.bottom,
                height=1,
            ).fillet_height(r=4.2)
        )
        .add(
            lambda parent: Volume(
                left=case.hat_shield_slot.left + SHIELD_MARGIN + T,
                right=case.hat_shield_slot.right - SHIELD_MARGIN - T,
                front=parent.back,
                depth=2,
                top=parent.top,
                height=1.6,
            )
        )
    )

    hexes = ~Tube(
        diameter=6, height=5, segments=6, left=cover.left + 4, back=cover.back + 6, center_z=cover.center_z
    ).array(7, y=7).array(6, x=14).array(2, x=7, y=3.5)


cover = Raspberry4Cover()


class Shield(Part):
    body = (
        Volume(
            left=case.hat_shield_slot.left + T,
            right=case.hat_shield_slot.right - T,
            back=case.back + 1.6,
            depth=1.4,
            top=cover.bottom - T,
            bottom=case.hat_shield_slot.bottom + T,
        )
        .fillet_depth(r=6.2, bottom=True)
        .add(
            lambda parent: Volume(
                left=parent.left + SHIELD_MARGIN,
                right=parent.right - SHIELD_MARGIN,
                front=parent.back,
                depth=1.4,
                top=parent.top + 1 - T,
                bottom=case.hat_shield_slot.bottom + SHIELD_MARGIN + T,
            ).fillet_depth(r=5.2, bottom=True)
        )
    )


class IQAudioShield(Shield):
    jack_slot = ~Raspberry4Case.jack_slot.up(12).leftward(1)
    rca_slots = (
        Tube(diameter=12, height=6)
        .top_to_back()
        .align(center_x=jack_slot.center_x - 34, back=case.back - 1, center_z=jack_slot.center_z + 7)
        .slide(x=14)
        .hole()
    )


shield = IQAudioShield()

(
    case.color("grey")
    # + cover.color("red")
    # + shield.color("white")
    + Import(r"/home/guillaume/Téléchargements/Hifiberry_case_Pi_4_iqaudio-pro.stl").down(5).background()
    # + Import(r"/home/guillaume/Téléchargements/hifiberry_rca_cover_iqaudio-pro.stl").up(15).backward(31).leftward(17)
).render_to_file(r"raspberry4_case.scad")

# case.export_stl("raspberry_pi_4_case.stl")
shield.export_stl("iqaudio_dac_plus.stl")
# cover.export_stl("raspberry_pi_4_cover.stl")
