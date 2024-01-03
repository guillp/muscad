from __future__ import annotations

import sys
from typing import Literal

from muscad import (
    EE,
    TT,
    TTT,
    Chamfer,
    Circle,
    Cylinder,
    E,
    Fillet,
    Hull,
    Object,
    Part,
    Sphere,
    Surface,
    SymmetricPart,
    T,
    Union,
    Volume,
    middle_of,
)
from muscad.utils.tube import Tube
from muscad.vitamins.bearings import (
    BushingLinearBearing,
    LinearBearing,
    RotationBearing,
)
from muscad.vitamins.belts import Belt
from muscad.vitamins.boards import Board
from muscad.vitamins.bolts import Bolt, Nut
from muscad.vitamins.brackets import CastBracket
from muscad.vitamins.endstops import (
    InductionSensor,
    MechanicalEndstopOnPCB,
)
from muscad.vitamins.extruders import E3Dv6Extruder
from muscad.vitamins.extrusions import Extrusion, Extrusion3030Insert
from muscad.vitamins.fans import Blower, Fan
from muscad.vitamins.pulleys import Pulley
from muscad.vitamins.rods import BrassNut, Rod, ThreadedRod
from muscad.vitamins.steppers import StepperMotor

# heating bed size, adjust to your own bed
BED_WIDTH = 330
BED_DEPTH = 330
BED_THICKNESS = 3  # may include glass or other plates

# offset from the bed left or right side to Y rods centers
BED_SIDE_TO_Y_ROD_CENTER_X_OFFSET = 100
# Y offset of the bed compared to the Y rod
BED_CENTER_Y_TO_Y_ROD_CENTER_Y_OFFSET = 20
# height of the Y rods compared to the bed
BED_TOP_TO_Y_ROD_CENTER_Z_OFFSET = 100

# offset from the Z rods to the side of the bed
BED_SIDE_TO_Z_ROD_CENTER_X_OFFSET = 27

# Y distance between the 2 left or the 2 right Z rods
Z_RODS_DISTANCE = 65 * 2
Z_HEIGHT = 480  # Maximum Z travel

Y_ROD_OFFSET = 17.5  # Z distance between an Y rod center and the upper Y extrusion bottom
X_ROD_OFFSET = 47  # Z distance between the 2 X rods

X_ROD_LENGTH = 500  # length of the X rods
Y_ROD_LENGTH = 440  # length of the Y rods
Z_ROD_LENGTH = 500  # length of the Z rods
Z_THREADED_ROD_LENGTH = Z_ROD_LENGTH - 60

Y_ROD_CENTER_TO_STEPPER_SHAFT_CENTER = 36.25
STEPPER_Z_OFFSET = 60

X_PULLEYS_Z_OFFSET = -1
Y_PULLEYS_Z_OFFSET = +1
BACK_BELT_Y_OFFSET = -2

BED_CENTER_X = 0
BED_CENTER_Y = 0
BED_CENTER_Z = 0


EXTRUSION_SIZE = 30

X_EXTRUSION_LENGTH = BED_WIDTH + 140
Y_EXTRUSION_LENGTH = Y_ROD_LENGTH
Z_EXTRUSION_LENGTH = Z_ROD_LENGTH + 100

MIDDLE_Y_EXTRUSION_OFFSET = 130

X_EXTRUSION = Extrusion.e3030(X_EXTRUSION_LENGTH).bottom_to_right()
Y_EXTRUSION = Extrusion.e3030(Y_EXTRUSION_LENGTH).bottom_to_front()
Z_EXTRUSION = Extrusion.e3030(Z_EXTRUSION_LENGTH)

CABLE_CHAIN_WIDTH = 19


class Bed(Part):
    bed = Volume(
        width=BED_WIDTH,
        depth=BED_DEPTH,
        height=BED_THICKNESS,
        center_x=BED_CENTER_X,
        center_y=BED_CENTER_Y,
        center_z=BED_CENTER_Z,
    )

    y_extrusion_left = (
        Extrusion.e2020(bed.depth - 75)
        .bottom_to_back()
        .align(left=bed.left - 20, center_y=bed.center_y, top=bed.bottom - 6)
    ).misc()
    y_extrusion_right = y_extrusion_left.x_mirror(center=bed.center_x).misc()
    x_extrusion_front = (
        Extrusion.e2020(X_EXTRUSION_LENGTH - 10)
        .bottom_to_left()
        .align(
            center_x=bed.center_x,
            back=y_extrusion_left.front,
            center_z=y_extrusion_left.center_z,
        )
        .misc()
    )
    x_extrusion_back = x_extrusion_front.y_mirror(center=y_extrusion_right.center_y).misc()

    bolt_front = (
        Bolt.M3(40, thread_clearance=20)
        .bottom_to_top()
        .align(center_x=bed.center_x, center_y=bed.front - 2, top=bed.top)
    )
    bolt_left = (
        Bolt.M3(40, thread_clearance=20)
        .bottom_to_top()
        .align(center_x=bed.left + 2, center_y=bed.back + 2, top=bed.top)
    )
    bolt_right = (
        Bolt.M3(40, thread_clearance=20)
        .bottom_to_top()
        .align(center_x=bed.right - 2, center_y=bed.back + 2, top=bed.top)
    )


bed = Bed()

glass_plate = Volume(
    width=310 + TT,
    depth=310 + TT,
    height=3,
    center_x=bed.center_x,
    center_y=bed.center_y,
    bottom=bed.top,
)


class GlassPlateCorner(Part):
    glass_plate = ~glass_plate
    corner = Volume(
        left=bed.left,
        right=glass_plate.left + 10,
        front=bed.front,
        back=glass_plate.front - 10,
        bottom=glass_plate.bottom + TT,
        top=glass_plate.top - TT,
    ).fillet_height(2)
    pin = Tube(
        diameter=3 - TT,
        center_x=bed.left + 5 - TT,
        center_y=bed.front - 5 + TT,
        height=3,
        top=corner.bottom,
    )


glass_plate_corner_left_front = GlassPlateCorner()
glass_plate_corner_right_front = glass_plate_corner_left_front.x_mirror().align(right=bed.right, front=bed.front)


class GlassPlateFrontFix(Part):
    glass_plate = ~glass_plate
    body = Volume(
        center_x=bed.center_x,
        width=20,
        back=bed.back,
        front=glass_plate.back,
        bottom=bed.top,
        top=glass_plate.top - TT,
    ).fillet_height(2, back=True)
    pin = Tube(
        diameter=3 - TT,
        center_x=bed.center_x,
        center_y=bed.back + 5 - TT,
        height=3,
        top=body.bottom,
    )


glass_plate_front_fix = GlassPlateFrontFix()


class Frame(Part):
    x_extrusion_front_top = X_EXTRUSION.align(
        center_x=bed.center_x,
        back=bed.front + 40,
        bottom=bed.top + 120,
    )

    z_extrusion_left_front = Z_EXTRUSION.align(
        right=x_extrusion_front_top.left,
        center_y=x_extrusion_front_top.center_y,
        top=x_extrusion_front_top.top - 6,
    )
    z_extrusion_right_front = Z_EXTRUSION.align(
        left=x_extrusion_front_top.right,
        center_y=x_extrusion_front_top.center_y,
        top=x_extrusion_front_top.top - 6,
    )

    y_extrusion_left_top = Y_EXTRUSION.align(
        center_x=z_extrusion_left_front.center_x,
        front=z_extrusion_left_front.back,
        top=x_extrusion_front_top.top,
    )
    y_extrusion_right_top = Y_EXTRUSION.align(
        center_x=z_extrusion_right_front.center_x,
        front=z_extrusion_right_front.back,
        top=x_extrusion_front_top.top,
    )

    z_extrusion_left_back = Z_EXTRUSION.align(
        center_x=y_extrusion_left_top.center_x,
        front=y_extrusion_left_top.back,
        top=y_extrusion_left_top.top - 6,
    )
    z_extrusion_right_back = Z_EXTRUSION.align(
        center_x=y_extrusion_right_top.center_x,
        front=y_extrusion_right_top.back,
        top=y_extrusion_right_top.top - 6,
    )

    x_extrusion_back_top = X_EXTRUSION.align(
        left=z_extrusion_left_back.right,
        center_y=z_extrusion_left_back.center_y,
        top=x_extrusion_front_top.top,
    )
    x_extrusion_back_bottom = X_EXTRUSION.align(
        left=z_extrusion_left_back.right,
        center_y=z_extrusion_left_back.center_y,
        bottom=z_extrusion_left_back.bottom,
    )

    y_extrusion_left_bottom = Y_EXTRUSION.align(
        center_x=z_extrusion_left_back.center_x,
        back=z_extrusion_left_back.front,
        bottom=z_extrusion_left_back.bottom,
    )
    y_extrusion_right_bottom = Y_EXTRUSION.align(
        center_x=z_extrusion_right_back.center_x,
        back=z_extrusion_left_back.front,
        bottom=z_extrusion_left_back.bottom,
    )

    y_extrusion_left_middle = Y_EXTRUSION.align(
        center_x=z_extrusion_left_back.center_x,
        back=z_extrusion_left_back.front,
        center_z=y_extrusion_left_top.center_z - MIDDLE_Y_EXTRUSION_OFFSET,
    )
    y_extrusion_right_middle = y_extrusion_left_middle.x_mirror(x_extrusion_front_top.center_x)

    x_extrusion_front_bottom = X_EXTRUSION.align(
        left=z_extrusion_left_front.right,
        front=z_extrusion_left_front.front,
        bottom=z_extrusion_left_front.bottom,
    )

    cast_left_back_top = CastBracket.bracket3030().align(
        left=y_extrusion_left_top.right,
        back=x_extrusion_back_top.front,
        center_z=x_extrusion_front_top.center_z,
    )
    cast_left_front_top = cast_left_back_top.y_mirror(y_extrusion_left_top.center_y)
    cast_right_back_top = cast_left_back_top.x_mirror(x_extrusion_back_top.center_x)
    cast_right_front_top = cast_left_front_top.x_mirror(x_extrusion_front_top.center_x)


frame = Frame()

X_ROD = Rod.d8(X_ROD_LENGTH + EE).bottom_to_right()
Y_ROD = Rod.d12(Y_ROD_LENGTH + EE).bottom_to_front()
Z_ROD = Rod.d12(Z_ROD_LENGTH + EE)

Z_THREADED_ROD = ThreadedRod.T8(Z_THREADED_ROD_LENGTH)


class Gantry(Part):
    y_rod_left = Y_ROD.align(
        center_x=frame.y_extrusion_left_top.center_x,
        center_y=frame.y_extrusion_left_top.center_y,
        center_z=frame.y_extrusion_left_top.bottom - 40,
    )

    x_rod_top = X_ROD.align(
        center_x=frame.center_x,
        center_y=frame.center_y,
        center_z=y_rod_left.center_z + X_ROD_OFFSET / 2,
    )

    y_rod_right = y_rod_left.x_mirror(center=bed.center_x)

    x_rod_bottom = x_rod_top.z_mirror(center=y_rod_left.center_z)

    x_bearing_top_right = (
        BushingLinearBearing.SC8UU(bolt_head_clearance=10, T=0.15)
        .left_to_top()
        .align(
            left=bed.center_x + 0.5,
            center_y=x_rod_top.center_y,
            center_z=x_rod_top.center_z,
        )
    )
    x_bearing_top_left = x_bearing_top_right.x_mirror(center=bed.center_x)
    x_bearing_bottom = (
        BushingLinearBearing.SC8UU(bolt_head_clearance=10, T=0.15)
        .left_to_top()
        .align(
            center_x=bed.center_x,
            center_y=x_rod_bottom.center_y,
            center_z=x_rod_bottom.center_z,
        )
    )

    z_stepper_left = StepperMotor.nema17(bolt=Bolt.M3(8).top_to_bottom()).align(
        center_x=bed.y_extrusion_left.left - BED_SIDE_TO_Z_ROD_CENTER_X_OFFSET,
        center_y=bed.center_y,
        top=frame.y_extrusion_left_bottom.top,
    )
    z_stepper_right = z_stepper_left.x_mirror(bed.center_x)

    z_threaded_rod_left = Z_THREADED_ROD.align(
        center_x=z_stepper_left.center_x,
        center_y=z_stepper_left.center_y,
        bottom=z_stepper_left.top + 20,
    )
    z_threaded_rod_right = z_threaded_rod_left.x_mirror(center=bed.center_x)

    z_rod_left_back = Z_ROD.align(
        center_x=z_threaded_rod_left.center_x,
        center_y=z_threaded_rod_left.center_y - Z_RODS_DISTANCE / 2,
        bottom=frame.bottom - 10,
    )
    z_rod_left_front = z_rod_left_back.y_mirror(center=bed.center_y)
    z_rod_right_back = z_rod_left_back.x_mirror(center=bed.center_x)
    z_rod_right_front = z_rod_right_back.y_mirror(center=bed.center_y)

    x_stepper = StepperMotor.nema17().align(
        right=frame.z_extrusion_right_back.left,
        back=frame.z_extrusion_right_back.back,
        top=y_rod_right.center_z - 20,
    )

    y_stepper = StepperMotor.nema17().align(
        left=frame.z_extrusion_left_front.right,
        back=frame.z_extrusion_left_back.back,
        top=y_rod_left.center_z - 20,
    )


gantry = Gantry()


class Extrusion3030Endcap(Part):
    base = Volume(width=30, depth=30, height=6).fillet_height(4)
    x_insert = (
        Extrusion3030Insert(25).front_to_right().align(left=base.right, center_y=base.center_y, bottom=base.bottom)
    )
    y_insert = Extrusion3030Insert(25).align(center_x=base.center_x, back=base.front, bottom=base.bottom)
    x_insert_left = (
        Extrusion3030Insert(25)
        .back_to_top()
        .back_to_left()
        .align(left=base.left, center_y=base.center_y, bottom=base.top)
    )
    z_insert_back = (
        Extrusion3030Insert(25).bottom_to_back().align(center_x=base.center_x, back=base.back, bottom=base.top)
    )

    def __stl__(self) -> Object:
        return self.upside_down()


endcap_left_back = (
    Extrusion3030Endcap().upside_down().z_rotate(-90).align(left=frame.left, back=frame.back, top=frame.top)
)
endcap_left_front = (
    Extrusion3030Endcap().upside_down().z_rotate(180).align(left=frame.left, front=frame.front, top=frame.top)
)
endcap_right_back = Extrusion3030Endcap().upside_down().align(right=frame.right, back=frame.back, top=frame.top)
endcap_right_front = (
    Extrusion3030Endcap().upside_down().z_rotate(90).align(right=frame.right, front=frame.front, top=frame.top)
)


class BedBracket(Part):
    extrusion = ~bed.x_extrusion_front
    bed_bolt = ~bed.bolt_front

    _base = (
        Volume(
            center_x=bed_bolt.center_x,
            width=20,
            front=extrusion.front + 4,
            back=extrusion.back + 4,
            bottom=extrusion.bottom - 6,
            top=extrusion.top - 4,
        )
        .fillet_height(r=4)
        .fillet_depth(6, top=True)
    )

    _bolt_holder = Tube(
        diameter=10,
        center_x=bed_bolt.center_x,
        center_y=bed_bolt.center_y,
        top=extrusion.bottom,
        bottom=_base.bottom,
    )

    body = Hull(_base, _bolt_holder)

    bottom_bolt = ~Bolt.M5(10).slide(y=-10).align(
        center_x=_base.center_x,
        center_y=extrusion.center_y,
        center_z=extrusion.bottom - 2,
    )
    front_bolt = ~Bolt.M5(10, head_clearance=20).bottom_to_front().slide(z=10).align(
        center_x=_base.center_x,
        center_y=extrusion.front,
        center_z=extrusion.center_z,
    )

    clearance = ~Volume(
        center_x=bed_bolt.center_x,
        width=10,
        back=extrusion.front + 6,
        front=_bolt_holder.front,
        bottom=extrusion.bottom,
        height=extrusion.height,
    ).fillet_height(r=2, back=True).fillet_depth(bottom=True)


bed_bracket_front = BedBracket()
bed_bracket_left = bed_bracket_front.y_mirror(bed.center_y).align(center_x=bed.left + 2)
bed_bracket_right = bed_bracket_left.align(center_x=bed.right - 2)


class ThumbWheel(Part):
    bed_bolt = ~bed.bolt_front
    nut = ~Nut.M3().align(
        center_x=bed_bolt.center_x,
        center_y=bed_bolt.center_y,
        bottom=bed_bolt.bottom + 1,
    )

    wheel = Tube(
        diameter=16,
        center_x=bed_bolt.center_x,
        center_y=bed_bolt.center_y,
        bottom=nut.bottom - 4,
        top=nut.top + 2,
    )

    def init(self) -> None:  # type: ignore[override]
        self.wheel_holes = ~Union(
            Tube(
                diameter=3,
                height=self.wheel.height + EE,
                center_x=self.nut.center_x,
                center_y=self.wheel.front,
                center_z=self.wheel.center_z,
            ).z_rotate(i * 30, center_x=self.nut.center_x, center_y=self.nut.center_y)
            for i in range(0, 12)
        )


thumbwheel_front = ThumbWheel()
thumbwheel_left = thumbwheel_front.align(center_x=bed.bolt_left.center_x, center_y=bed.bolt_left.center_y)
thumbwheel_right = thumbwheel_front.align(center_x=bed.bolt_right.center_x, center_y=bed.bolt_right.center_y)


class ZTopEndStop(Part):
    bed_extrusion = ~bed.x_extrusion_front
    frame_extrusion = ~frame.y_extrusion_right_middle
    endstop = (
        ~MechanicalEndstopOnPCB(Bolt.M3(10).add_nut(-3, side_clearance_size=10, angle=-90))
        .front_to_bottom()
        .front_to_right()
        .align(
            left=bed_extrusion.right - 10,
            front=bed_extrusion.center_y,
            bottom=bed_extrusion.top + 5,
        )
        .debug()
    )

    bolt = ~Bolt.M5(12, head_clearance=30).bottom_to_left().align(
        center_x=frame_extrusion.left,
        center_y=endstop.back - 10,
        center_z=frame_extrusion.center_z + 20,
    ).slide(z=-30)
    plate = Volume(
        width=6,
        right=frame_extrusion.left - TT,
        front=bolt.front + 10,
        back=bolt.back - 10,
        top=bolt.top + 5,
        bottom=frame_extrusion.bottom - 5,
    ).fillet_width(4)
    endstop_attach = Volume(
        left=endstop.right,
        right=plate.right,
        front=endstop.front,
        back=endstop.back,
        bottom=endstop.bottom,
        top=endstop.top,
    ).fillet_width(2)

    def __stl__(self) -> Object:
        return self.right_to_bottom()


z_top_endstop = ZTopEndStop()


class XCarriage(Part):
    x_bearing_top_left = ~gantry.x_bearing_top_left
    x_bearing_top_right = ~gantry.x_bearing_top_right
    x_bearing_bottom = ~gantry.x_bearing_bottom

    body = Volume(
        left=x_bearing_top_left.left + E,
        right=x_bearing_top_right.right - E,
        front=x_bearing_bottom.back - E,
        depth=8,
        bottom=gantry.x_bearing_bottom.top + 1,
        top=x_bearing_top_left.top - E,
    ).fillet_depth() + Volume(
        left=x_bearing_bottom.left,
        right=x_bearing_bottom.right,
        front=x_bearing_bottom.back - E,
        depth=8,
        bottom=x_bearing_bottom.bottom + E,
        top=x_bearing_bottom.top + 1,
    ).fillet_depth(bottom=True, left=True).reverse_fillet_top(left=True, right=True)

    center_pulleys_bolt = ~Bolt.M3(20, head_clearance=100).add_nut(
        -1, inline_clearance_size=10
    ).bottom_to_front().align(center_x=body.center_x, back=body.back, center_z=body.center_z)

    extruder_holder = Volume(
        center_x=body.center_x,
        width=50,
        front=body.back,
        back=body.back - 30,
        center_z=body.center_z,
        bottom=x_bearing_bottom.top + 1,
    ).fillet_depth()

    extruder = (
        ~E3Dv6Extruder()
        .z_rotate(180)
        .align(
            center_x=body.center_x,
            center_y=extruder_holder.back + 2,
            top=extruder_holder.top + 4,
        )
        .debug()
    )

    blower = (
        ~Blower.blower50x50x15(bolt=Bolt.M3(20).add_nut(-E, inline_clearance_size=20))
        .x_rotate(-90)
        .align(
            left=body.center_x - 9,
            front=body.back - T,
            bottom=extruder_holder.top,
        )
        .debug()
    )

    right_blower_holder = (
        Volume(
            right=blower.front_bolt.right + 1,
            left=body.right,
            depth=4,
            back=body.back,
            bottom=blower.front_bolt.bottom - 2,
            top=blower.front_bolt.top + 2,
        )
        .fillet_depth(r=4, right=True)
        .reverse_fillet_left(top=True, bottom=True)
        .misc()
    )

    cable_guide_top = (
        Volume(
            center_x=body.center_x,
            width=24,
            back=body.back,
            front=body.front,
            bottom=body.top - E,
            top=frame.y_extrusion_right_top.top - 1,
        )
        .reverse_fillet_bottom(left=True, right=True)
        .fillet_depth(r=6, top=True)
    )

    cable_guide_bolts = (
        ~Bolt.M3(10)
        .add_nut(-T, inline_clearance_size=10)
        .bottom_to_back()
        .align(
            center_x=cable_guide_top.center_x,
            back=cable_guide_top.back - E,
            center_z=cable_guide_top.top - 6,
        )
        .z_mirror(cable_guide_top.top - 10)
        .debug()
    )

    cable_guide_side = (
        Volume(
            left=gantry.x_bearing_bottom.right,
            right=body.right,
            back=body.back,
            front=body.front,
            bottom=body.bottom,
            height=12,
        )
        .fillet_depth(right=True)
        .reverse_fillet_left(top=True)
    )
    cable_hole = ~Volume(
        right=body.right + E,
        width=10,
        front=x_bearing_bottom.front,
        back=body.back - 1,
        bottom=body.bottom + 3,
        height=6,
    ).fillet_depth(2)

    fan = (
        ~Fan.fan40x40x20(bolt=None)
        .add_bolts(
            bolt=Bolt.M3(30).add_nut(-8.5, side_clearance_size=10, angle=180, T=0.1),
            spacing=32,
            holes=(2, 3),
        )
        .add_bolts(
            bolt=Bolt.M3(55).add_nut(-6, inline_clearance_size=40),
            spacing=32,
            holes=(0, 1),
        )
        .x_rotate(90)
        .z_rotate(180)
        .align(
            center_x=extruder_holder.center_x,
            front=extruder_holder.back - 13,
            top=extruder_holder.top,
        )
        .debug()
    )

    anti_warp = ~(
        Volume(
            center_x=body.center_x,
            width=1,
            front=body.front + E,
            depth=1,
            top=cable_guide_top.top - 1,
            bottom=body.bottom + 1,
        ).fillet_height(0.5, front=True)
        + Volume(
            left=body.left + 1,
            right=body.right - 1,
            front=body.front + E,
            depth=1,
            top=x_bearing_top_left.bottom,
            height=1,
        ).fillet_width(0.5, front=True)
        + Volume(
            left=body.left + 1,
            right=body.right - 1,
            front=body.front + E,
            depth=1,
            bottom=x_bearing_bottom.top,
            height=1,
        ).fillet_width(0.5, front=True)
        + Volume(
            left=body.left + 1,
            right=body.right - 1,
            front=body.front + E,
            depth=1,
            bottom=x_bearing_top_left.top,
            height=1,
        ).fillet_width(0.5, front=True)
    )

    def __stl__(self) -> Object:
        return self.back_to_top()


x_carriage = XCarriage()


class XAxisPulleys(Part):
    x_rod_bottom = ~gantry.x_rod_bottom
    center_pulleys_bolt = x_carriage.center_pulleys_bolt
    bottom_bearing = ~gantry.x_bearing_bottom

    left_pulley = ~Pulley.placeholder(15, 10.3).add_clearance(20, angle=90).align(
        right=gantry.x_bearing_bottom.left - 0.5,
        center_y=gantry.x_rod_top.center_y,
        top=gantry.y_rod_left.center_z + X_PULLEYS_Z_OFFSET,
    )

    right_pulley = ~left_pulley.x_mirror(center=bed.center_x)

    left_pulley_shaft = (
        ~Bolt.M3(20, head_clearance=10)
        .add_nut(-1, angle=90, inline_clearance_size=10)
        .top_to_bottom()
        .align(
            center_x=left_pulley.center_x,
            center_y=left_pulley.center_y,
            center_z=left_pulley.center_z,
        )
        .debug()
    )
    right_pulley_shaft = ~left_pulley_shaft.x_mirror(center=bed.center_x)

    body = Volume(
        left=x_carriage.body.left,
        right=x_carriage.body.right,
        back=x_carriage.body.front + T,
        front=bottom_bearing.front - E,
        bottom=gantry.x_rod_bottom.top + 0.5,
        top=gantry.x_bearing_top_left.bottom - T,
    )

    cable_guide = (
        Volume(
            right=body.right,
            left=bottom_bearing.right,
            back=gantry.x_rod_bottom.front + 2,
            front=body.front,
            top=body.bottom + E,
            bottom=x_carriage.body.bottom,
        )
        .fillet_depth(bottom=True)
        .reverse_fillet_top(back=True)
        + Volume(
            right=body.right,
            left=bottom_bearing.right,
            front=body.front,
            back=body.back,
            bottom=x_carriage.body.bottom,
            height=12,
        ).fillet_depth()
        - x_carriage.cable_hole
    )

    right_endstop = (
        ~MechanicalEndstopOnPCB(
            bolt=Bolt.M3(12, thread_clearance=4).add_nut(-1, side_clearance_size=10, angle=-90).upside_down(),
            z_offset=5.5,
        )
        .front_to_right()
        .back_to_bottom()
        .align(right=body.right, back=body.front, bottom=body.bottom - 1)
        .debug()
    )

    left_endstop = (
        ~MechanicalEndstopOnPCB(bolt=Bolt.M3(8).add_nut(-2, side_clearance_size=10, angle=-90))
        .back_to_right()
        .back_to_top()
        .align(left=body.left, back=body.front, bottom=body.bottom - 1)
        .debug()
    )

    cable_guide_bolts = ~Bolt.M3(16, head_clearance=10).add_nut(-3, inline_clearance_size=20).bottom_to_front().align(
        center_x=body.center_x + 8,
        front=body.front + 8,
        center_z=center_pulleys_bolt.center_z,
    ).x_symmetry(center=center_pulleys_bolt.center_x)

    def __stl__(self) -> Object:
        return self.bottom_to_back()


x_axis_pulleys = XAxisPulleys()


class CableClampBack(Part):
    bolts = x_axis_pulleys.cable_guide_bolts

    body = Volume(
        center_x=x_axis_pulleys.center_x,
        left=x_axis_pulleys.left_endstop.right + 2,
        back=x_axis_pulleys.body.front + 2,
        depth=4,
        top=x_axis_pulleys.body.top,
        bottom=x_axis_pulleys.bottom_bearing.top,
    ).fillet_depth(2)

    def __stl__(self) -> Object:
        return self.back_to_bottom()


cable_clamp_back = CableClampBack()


class ExtruderClamp(Part):
    _extruder_holder = x_carriage.extruder_holder

    extruder = x_carriage.extruder

    fan = x_carriage.fan
    sensor = (
        ~InductionSensor.LJ12A3()
        .align(
            center_x=extruder.center_x - 35,
            front=x_carriage.body.back - 3,
            bottom=extruder.bottom + 4,
        )
        .debug()
    )

    clamp = Volume(
        left=_extruder_holder.left,
        right=_extruder_holder.right,
        front=_extruder_holder.back - 0.5,
        back=fan.front + T,
        bottom=_extruder_holder.bottom - 29,
        top=_extruder_holder.top,
    ).fillet_depth()

    tunnel = ~Hull(
        Volume(
            center_x=clamp.center_x,
            width=36,
            front=clamp.back,
            back=clamp.back - 1,
            top=clamp.top - 7,
            bottom=clamp.bottom + 5,
        ).fillet_depth(7),
        Volume(
            left=clamp.left + 8,
            right=clamp.right - 8,
            front=clamp.front + 1,
            back=clamp.front,
            top=clamp.top - 13,
            bottom=clamp.bottom - 1,
        ).fillet_depth(4),
    )

    cable_guide = Volume(
        left=clamp.right,
        width=3,
        front=clamp.front,
        back=clamp.back,
        bottom=clamp.bottom,
        height=6,
    ).fillet_depth(1, right=True).reverse_fillet_left(top=True).reverse_fillet_bottom(left=True) - Volume(
        left=clamp.right,
        width=4,
        front=clamp.front + E,
        back=clamp.back - E,
        center_z=clamp.bottom + 3,
        height=3,
    ).fillet_depth(1, left=True)

    sensor_holder_up = (
        Volume(
            right=clamp.left - TT,
            width=18,
            depth=18,
            center_y=sensor.center_y,
            top=clamp.top - 2,
            height=9,
        )
        .fillet_height(6, left=True)
        .fillet_height(6, front=True, right=True)
    )

    sensor_holder_down = sensor_holder_up.z_mirror(center=clamp.center_z)

    sensor_arm_up = Volume(
        right=clamp.left - TT,
        width=3,
        back=clamp.back,
        front=sensor_holder_up.back,
        top=sensor_holder_up.top,
        bottom=sensor_holder_up.bottom,
    ).fillet_height(back=True, left=True).reverse_fillet_front(left=True) + Volume(
        right=clamp.left,
        width=1,
        front=clamp.front,
        back=clamp.back,
        top=sensor_holder_up.top,
        bottom=sensor_holder_up.bottom,
    )

    sensor_arm_down = sensor_arm_up.z_mirror(center=clamp.center_z)

    def __stl__(self) -> Object:
        return self.back_to_bottom()


extruder_clamp = ExtruderClamp()


class Tunnel(Part):
    NOZZLE_SIZE = 0.4

    _center_x = x_carriage.extruder_holder.center_x

    tunnel = Volume(
        left=x_carriage.blower.blower.left + T,
        right=x_carriage.blower.blower.right - T,
        front=x_carriage.body.back - T,
        back=x_carriage.blower.blower.back + T,
        top=x_carriage.extruder_holder.center_z,
        bottom=x_carriage.bottom,
    ).fillet_height(NOZZLE_SIZE * 3) - Volume(
        left=x_carriage.blower.blower.left + NOZZLE_SIZE * 3.1 + T,
        right=x_carriage.blower.blower.right - NOZZLE_SIZE * 3.1 - T,
        front=x_carriage.body.back - NOZZLE_SIZE * 3.1 - T,
        back=x_carriage.blower.blower.back + NOZZLE_SIZE * 3.1 + T,
        top=x_carriage.extruder_holder.center_z + E,
        bottom=x_carriage.bottom - E,
    ).fillet_height(NOZZLE_SIZE * 2)

    blower = Hull(
        Volume(
            center_x=_center_x,
            width=30,
            back=x_carriage.extruder.center_y + 5,
            depth=5,
            bottom=x_carriage.extruder.bottom + 1,
            height=E,
        ).fillet_height(NOZZLE_SIZE * 3),
        Volume(
            left=tunnel.left,
            right=tunnel.right,
            back=tunnel.back,
            front=tunnel.front,
            top=tunnel.bottom,
            height=E,
        ).fillet_height(NOZZLE_SIZE * 2),
    ) - Hull(
        Volume(
            center_x=_center_x,
            width=28,
            back=x_carriage.extruder.center_y + 5,
            depth=3,
            bottom=x_carriage.extruder.bottom,
            height=E,
        ).fillet_height(NOZZLE_SIZE * 3),
        Volume(
            left=tunnel.left + NOZZLE_SIZE * 3.1,
            right=tunnel.right - NOZZLE_SIZE * 3.1,
            back=tunnel.back + NOZZLE_SIZE * 3.1,
            front=tunnel.front - NOZZLE_SIZE * 3.1,
            top=tunnel.bottom + E,
            height=E,
        ).fillet_height(NOZZLE_SIZE * 3),
    )

    bolt_left = ~Bolt.M2(10).bottom_to_back().align(
        center_x=tunnel.left - 3,
        center_y=x_carriage.body.back,
        center_z=x_carriage.bottom + 20,
    )
    bolt_holder_left = (
        Volume(
            center_x=bolt_left.center_x,
            right=tunnel.left + 0.5,
            front=x_carriage.body.back - T,
            depth=3,
            center_z=bolt_left.center_z + 2,
            height=15,
        )
        .chamfer_depth(8, top=True, left=True)
        .fillet_depth(bottom=True, left=True)
    )

    bolt_right = ~bolt_left.x_mirror(center=tunnel.center_x)
    bolt_holder_right = bolt_holder_left.x_mirror(center=tunnel.center_x)

    def __stl__(self) -> Object:
        return self.upside_down()


tunnel = Tunnel()


class CableChainCarriageAttachment(Part):
    bolts = x_carriage.cable_guide_bolts
    body = Volume(
        left=x_carriage.cable_guide_top.left,
        right=x_carriage.cable_guide_top.right,
        back=x_carriage.cable_guide_top.front,
        depth=3,
        bottom=x_carriage.x_bearing_top_right.top + 1,
        top=x_carriage.cable_guide_top.top,
    ).fillet_depth(6)

    chain_attach = (
        Tube(
            diameter=16 + 3 + 2 * T,
            center_x=body.left - 1.5,
            back=body.back,
            bottom=frame.y_extrusion_right_top.center_z + CABLE_CHAIN_WIDTH / 2 + T,
            height=4,
        )
        .add_corner(angle=270)
        .z_symmetry(center=frame.y_extrusion_right_top.center_z)
    )

    shaft = (
        ~Bolt.M5(25)
        .upside_down()
        .align(
            center_x=chain_attach.center_x,
            center_y=chain_attach.center_y,
            center_z=chain_attach.center_z + 1,
        )
        .debug()
    )

    cable_guide = Volume(
        center_x=body.center_x,
        width=6,
        back=body.front,
        depth=16,
        top=bolts.bottom - 2,
        bottom=body.bottom,
    ).fillet_depth(2, top=True)

    cable_clamp_bolt = (
        ~Bolt.M3(10)
        .add_nut(-1.5, side_clearance_size=12.6)
        .bottom_to_right()
        .align(
            center_x=cable_guide.center_x + 2,
            center_y=cable_guide.back + 3.5,
            center_z=cable_guide.center_z,
        )
        .debug()
    )

    def __stl__(self) -> Object:
        return self.back_to_bottom()


cable_chain_carriage_attachment = CableChainCarriageAttachment()


class CableClampTop(Part):
    bolt = cable_chain_carriage_attachment.cable_clamp_bolt

    body = Volume(
        left=cable_chain_carriage_attachment.cable_guide.right + 2,
        width=3,
        back=cable_chain_carriage_attachment.cable_guide.back + TTT,
        front=cable_chain_carriage_attachment.cable_guide.front + TTT,
        bottom=cable_chain_carriage_attachment.cable_guide.bottom,
        top=cable_chain_carriage_attachment.cable_guide.top,
    ).fillet_width(2, back=True)

    side = (
        Volume(
            right=body.right,
            left=cable_chain_carriage_attachment.cable_guide.left,
            back=body.front,
            depth=3,
            bottom=body.bottom,
            top=body.top,
        )
        .fillet_depth(left=True)
        .fillet_height(2, right=True, front=True)
    )

    def __stl__(self) -> Object:
        return self.right_to_bottom()


cable_clamp_top = CableClampTop()


class CableChainFrameAttachement(Part):
    extrusion = ~frame.y_extrusion_right_top

    body = Volume(
        right=extrusion.left,
        width=6,
        bottom=extrusion.bottom + 2,
        top=extrusion.top - 2,
        front=frame.cast_right_front_top.back - 3,
        depth=60,
    ).fillet_width(4)

    frame_bolts = (
        ~Bolt.M5(16)
        .bottom_to_left()
        .align(left=body.left - 1, center_y=body.back + 8, center_z=body.center_z)
        .y_symmetry(body.center_y)
        .debug()
    )
    chain_bolts = (
        ~Bolt.M3(8)
        .add_nut(-1)
        .bottom_to_left()
        .align(right=body.right + 1, center_z=body.center_z)
        .y_symmetry(center=-7.5 / 2)
        .align(center_y=body.back + 24)
        .debug()
    )

    clamp_bolts = (
        ~Bolt.M3(10, thread_clearance=5)
        .add_nut(-1, inline_clearance_size=5)
        .bottom_to_left()
        .align(
            right=body.right - 1,
            center_y=chain_bolts.front + 8,
            center_z=body.center_z + 8,
        )
        .z_mirror(center=body.center_z)
        .debug()
    )

    support = Volume(
        right=body.left,
        width=5,
        back=body.back + 4,
        front=chain_bolts.front,
        top=chain_bolts.center_z - CABLE_CHAIN_WIDTH / 2,
        bottom=body.bottom,
    ).fillet_height(left=True)

    def __stl__(self) -> Object:
        return self.right_to_bottom()


cable_chain_frame_attachment = CableChainFrameAttachement()


class CableClampFrame(Part):
    bolts = cable_chain_frame_attachment.clamp_bolts

    body = Volume(
        left=bolts.left + 1,
        width=3,
        center_y=bolts.center_y,
        depth=12,
        top=bolts.top + 2,
        bottom=bolts.bottom - 2,
    ).fillet_width()

    def __stl__(self) -> Object:
        return self.right_to_bottom()


cable_clamp_frame = CableClampFrame()


class XYStepperMount(Part):
    y_rod = ~gantry.y_rod_left
    y_extrusion = ~frame.y_extrusion_left_top
    z_extrusion = ~frame.z_extrusion_left_back

    stepper = ~gantry.y_stepper

    base = (
        Volume(
            left=z_extrusion.left + 2,
            right=stepper.right,
            back=z_extrusion.back + 2,
            front=stepper.front,
            bottom=stepper.top + E,
            height=8,
        )
        .fillet_height(r=5, front=True)
        .fillet_height(r=5, back=True, right=True)
    )

    front_upper_bolt = ~Bolt.M6(8).bottom_to_front().align(
        center_x=z_extrusion.center_x,
        front=base.front + E,
        center_z=y_extrusion.bottom - 13,
    )

    right_upper_bolt = ~Bolt.M6(8).bottom_to_right().align(
        center_x=z_extrusion.right,
        center_y=z_extrusion.center_y,
        center_z=y_extrusion.bottom - 13,
    )
    right_lower_bolt = ~right_upper_bolt.align(center_z=y_rod.center_z)

    walls = (
        Volume(
            left=base.left,
            right=right_upper_bolt.right - E,
            back=base.back,
            front=front_upper_bolt.front - E,
            bottom=base.bottom,
            top=y_extrusion.bottom,
        )
        .fillet_height(r=2)
        .fillet_height(6, front=True, right=True)
    )

    shaft_bearing = ~RotationBearing.b605zz().align(
        center_x=stepper.center_x, center_y=stepper.center_y, top=base.top + E
    )

    clamp_clearance = ~(
        Volume(
            width=1,
            center_x=y_rod.center_x,
            back=z_extrusion.front - E,
            front=base.front + E,
            bottom=base.bottom - E,
            top=y_rod.center_z,
        )
    )

    clamp_bolt = ~Bolt.M3(length=16).add_nut(-1, angle=-15, side_clearance_size=10).bottom_to_left().align(
        center_x=clamp_clearance.right,
        center_y=walls.front - 7,
        top=y_rod.bottom - 3,
    )

    inner_y_pulley = ~Pulley.placeholder(13, 10.3).align(
        center_x=stepper.center_x,
        center_y=base.front - 5,
        bottom=y_rod.center_z + Y_PULLEYS_Z_OFFSET,
    )

    def __stl__(self) -> Object:
        return self.front_to_bottom()


class XYStepperMountLeft(XYStepperMount):
    x_belt_holder = (
        Volume(
            right=XYStepperMount.base.right,
            left=XYStepperMount.walls.right,
            back=XYStepperMount.stepper.center_y + 8,
            front=XYStepperMount.base.front,
            bottom=XYStepperMount.base.top,
            height=10,
        )
        .fillet_height(5, right=True)
        .reverse_fillet_left(6, back=True)
        .reverse_fillet_front(left=True)
    )

    x_belt = ~(
        Belt.GT2(60, 15)
        .front_to_right()
        .align(
            center_x=XYStepperMount.inner_y_pulley.center_x + 5,
            back=XYStepperMount.base.back - 1,
            bottom=XYStepperMount.base.top + T,
        )
        + Belt.GT2(60, 15)
        .front_to_left()
        .align(
            center_x=XYStepperMount.inner_y_pulley.center_x - 5,
            back=XYStepperMount.base.back - 1,
            bottom=XYStepperMount.base.top + T,
        )
        + Volume(
            center_x=XYStepperMount.stepper.center_x,
            width=10,
            back=x_belt_holder.back - 2,
            depth=2,
            bottom=XYStepperMount.base.top,
            top=x_belt_holder.top + 2,
        )
    )


xy_stepper_mount_left = XYStepperMountLeft()


class XYStepperMountRight(XYStepperMount):
    shaft = (
        ~Bolt.M3(35)
        .add_nut(-1, inline_clearance_size=10, angle=0)
        .upside_down()
        .align(
            center_x=XYStepperMount.inner_y_pulley.center_x,
            center_y=XYStepperMount.inner_y_pulley.center_y,
            bottom=XYStepperMount.base.bottom + 2,
        )
        .debug()
    )

    pulleys_box = Volume(
        left=XYStepperMount.z_extrusion.right,
        right=XYStepperMount.base.right,
        back=XYStepperMount.inner_y_pulley.back,
        front=XYStepperMount.base.front,
        bottom=XYStepperMount.base.top - E,
        top=gantry.x_rod_top.top,
    ).fillet_height(5, right=True) - Volume(
        left=XYStepperMount.inner_y_pulley.left - 1,
        center_x=shaft.center_x,
        back=XYStepperMount.inner_y_pulley.back - E,
        front=XYStepperMount.base.front + E,
        bottom=XYStepperMount.base.top,
        top=XYStepperMount.inner_y_pulley.top + 0.3,
    ).reverse_fillet_front(left=True, right=True).reverse_fillet_back(left=True, right=True)

    y_pulley_support = Volume(
        center_x=XYStepperMount.stepper.center_x,
        width=6,
        front=XYStepperMount.base.front,
        center_y=shaft.center_y,
        bottom=XYStepperMount.base.top,
        height=10,
    ).fillet_height()


xy_stepper_mount_right = XYStepperMountRight().x_mirror(center=frame.center_x)


class XYIdler(Part):
    y_rod = ~gantry.y_rod_left
    x_extrusion = ~frame.x_extrusion_front_top
    y_extrusion = ~frame.y_extrusion_left_top
    z_extrusion = ~frame.z_extrusion_left_front

    body = (
        Volume(
            left=z_extrusion.left + 2,
            right=z_extrusion.right + 14,
            back=z_extrusion.back - 14,
            front=z_extrusion.front - 2,
            top=y_extrusion.bottom - T,
            center_z=y_rod.center_z,
        )
        .fillet_height(r=2, right=True)
        .fillet_width(back=True)
        .fillet_depth(right=True)
    )

    back_top_bolt = ~Bolt.M6(12).bottom_to_back().align(
        center_x=z_extrusion.center_x,
        back=body.back - E,
        center_z=x_extrusion.bottom - 13,
    )
    back_bottom_bolt = ~back_top_bolt.z_mirror(center=y_rod.center_z)

    right_top_bolt = ~Bolt.M6(12).bottom_to_right().align(
        right=body.right + E,
        center_y=z_extrusion.center_y,
        center_z=x_extrusion.bottom - 13,
    )
    right_bottom_bolt = ~right_top_bolt.z_mirror(y_rod.center_z)

    pulleys_holder = Volume(
        left=body.right - 2,
        width=29,
        back=body.back,
        front=body.front,
        center_z=y_rod.center_z,
        height=34,
    ).fillet_depth(right=True)

    inner_y_pulley = ~Pulley.placeholder(18, 10.3).add_clearance(10, 270).add_belt_clearance(
        10, angle=270, left=True
    ).add_belt_clearance(40, angle=180).align(
        center_x=gantry.y_stepper.center_x + 10,
        center_y=z_extrusion.back,
        bottom=y_rod.center_z + Y_PULLEYS_Z_OFFSET,
    )

    inner_y_pulley_bolt = ~Bolt.M3(20).add_nut(-2, side_clearance_size=20).top_to_bottom().align(
        center_x=inner_y_pulley.center_x,
        center_y=inner_y_pulley.center_y,
        top=pulleys_holder.top + E,
    )

    clamp = ~(
        Volume(
            right=y_rod.center_x + 0.5,
            left=body.left - E,
            back=body.back - E,
            front=z_extrusion.back + E,
            center_z=y_rod.center_z,
            top=back_top_bolt.bottom - 3,
        )
    )

    clamp_bolt_top = ~Bolt.M3(16, head_clearance=10).add_nut(
        -2, side_clearance_size=20, angle=195
    ).bottom_to_left().align(
        center_x=y_rod.center_x,
        center_y=middle_of(body.back, z_extrusion.back),
        center_z=(back_top_bolt.center_z + y_rod.center_z) / 2 - 2,
    )

    clamp_bolt_bottom = ~clamp_bolt_top.align(center_z=(back_bottom_bolt.center_z + y_rod.center_z) / 2 + 2)

    def __stl__(self) -> Object:
        return self.back_to_bottom()


class XYIdlerClamp(Part):
    _idler = XYIdler()
    y_rod = _idler.y_rod
    top_bolt = _idler.clamp_bolt_top
    bottom_bolt = _idler.clamp_bolt_bottom
    body = Volume(
        right=y_rod.center_x - 0.5,
        left=_idler.left,
        back=_idler.back,
        front=_idler.z_extrusion.back,
        center_z=y_rod.center_z,
        top=_idler.back_top_bolt.bottom - 3.5,
    )

    def __stl__(self) -> Object:
        return self.right_to_bottom()


xy_idler_clamp_left = XYIdlerClamp()
xy_idler_clamp_right = xy_idler_clamp_left.x_mirror(center=frame.center_x)


class XYIdlerLeft(XYIdler):
    outer_y_pulley = ~Pulley.placeholder(18, height=10.3).add_clearance(20, 0).add_belt_clearance(
        40, angle=180
    ).add_belt_clearance(70, angle=270, left=True).align(
        center_x=XYIdler.y_rod.center_x + Y_ROD_CENTER_TO_STEPPER_SHAFT_CENTER,
        center_y=XYIdler.z_extrusion.center_y - BACK_BELT_Y_OFFSET,
        bottom=XYIdler.y_rod.center_z + Y_PULLEYS_Z_OFFSET,
    )

    outer_y_pulley_bolt = ~Bolt.M3(20).add_nut(-2, side_clearance_size=20, angle=-90).top_to_bottom().align(
        center_x=outer_y_pulley.center_x,
        center_y=outer_y_pulley.center_y,
        top=XYIdler.pulleys_holder.top + E,
    )

    x_pulley = ~Pulley.placeholder(18, height=10.3).add_clearance(10, 270).add_belt_clearance(
        10, angle=270, left=True
    ).add_belt_clearance(40, angle=180).align(
        center_x=outer_y_pulley.center_x + 10,
        center_y=XYIdler.z_extrusion.center_y - BACK_BELT_Y_OFFSET,
        top=XYIdler.y_rod.center_z + X_PULLEYS_Z_OFFSET - 1,
    )

    x_pulley_bolt = ~Bolt.M3(16).add_nut(-1, inline_clearance_size=3).align(
        center_x=x_pulley.center_x,
        center_y=x_pulley.center_y,
        bottom=XYIdler.pulleys_holder.bottom - E,
    )


xy_idler_left = XYIdlerLeft()


class XYIdlerRight(XYIdler):
    outer_x_pulley = ~Pulley.placeholder(18, height=10.3).add_clearance(20, 0).add_belt_clearance(
        40, angle=180
    ).add_belt_clearance(40, angle=270, left=True).align(
        center_x=gantry.y_stepper.center_x,
        center_y=XYIdler.z_extrusion.center_y - BACK_BELT_Y_OFFSET,
        top=XYIdler.y_rod.center_z + X_PULLEYS_Z_OFFSET,
    )

    inner_x_belt = ~Belt.GT2(42, 16).front_to_left().align(
        center_x=XYIdler.inner_y_pulley.center_x - 5,
        front=outer_x_pulley.back,
        top=XYIdler.y_rod.center_z + X_PULLEYS_Z_OFFSET - 1,
    )

    outer_y_pulley = ~Pulley.placeholder(18, height=10.3).add_clearance(20, angle=0).add_belt_clearance(
        40, angle=180
    ).add_belt_clearance(70, angle=270, left=True).align(
        center_x=gantry.y_stepper.center_x,
        center_y=XYIdler.z_extrusion.center_y - BACK_BELT_Y_OFFSET,
        bottom=XYIdler.y_rod.center_z + Y_PULLEYS_Z_OFFSET,
    )

    outer_y_pulley_bolt = ~Bolt.M3(35).add_nut(29, inline_clearance_size=20).top_to_bottom().align(
        center_x=outer_y_pulley.center_x,
        center_y=outer_y_pulley.center_y,
        top=XYIdler.pulleys_holder.top + E,
    )


xy_idler_right = XYIdlerRight().x_mirror(center=frame.center_x)


class YCarriage(Part):
    y_rod = ~gantry.y_rod_left
    x_rod_top = ~gantry.x_rod_top
    x_rod_bottom = ~gantry.x_rod_bottom

    y_bearing = (
        ~LinearBearing.LM12UU(hollow=False)
        .add_rod_clearance()
        .bottom_to_front()
        .align(
            center_x=y_rod.center_x,
            center_y=x_rod_top.center_y,
            center_z=y_rod.center_z,
        )
        .debug()
    )

    front_x_pulley = ~Pulley.placeholder(18, 10.3).add_bolt(
        Bolt.M3(25).add_nut(-1, side_clearance_size=20),
        z_offset=2,
    ).add_clearance(20, 270).add_clearance(20, 0).align(
        center_x=y_bearing.center_x + Y_ROD_CENTER_TO_STEPPER_SHAFT_CENTER + 10,
        center_y=y_bearing.center_y + 10,
        top=y_bearing.center_z + X_PULLEYS_Z_OFFSET,
    )

    back_x_pulley = ~front_x_pulley.y_mirror(y_bearing.center_y)

    pulleys_holder = Volume(
        left=y_bearing.center_x,
        right=front_x_pulley.right - E,
        back=back_x_pulley.back + E,
        front=front_x_pulley.front - E,
        top=x_rod_top.bottom - 1,
        bottom=x_rod_bottom.top + 1,
    ).fillet_width()

    body = Volume(
        left=y_bearing.center_x,
        right=front_x_pulley.left - 1,
        back=back_x_pulley.back + E,
        front=front_x_pulley.front - E,
        top=x_rod_top.top + 5,
        bottom=x_rod_bottom.bottom - 5,
    ).fillet_width(r=10, front=True)

    y_clamp_bolt_top_front = ~Bolt.M3(16, head_clearance=10).add_nut(
        placement=-2, side_clearance_size=30, angle=180
    ).bottom_to_left().align(
        left=body.left - 8,
        center_y=body.front - 4.5,
        center_z=y_bearing.top + 2.4,
    )

    y_clamp_bolt_top_back = ~y_clamp_bolt_top_front.y_mirror(y_bearing.center_y)
    y_clamp_bolt_bottom_front = ~y_clamp_bolt_top_front.z_mirror(y_bearing.center_z)
    y_clamp_bolt_bottom_back = ~y_clamp_bolt_top_back.z_mirror(y_bearing.center_z)

    clamp_clearance_bottom = ~Volume(
        left=body.left - E,
        right=body.right + E,
        front=body.center_y,
        depth=body.depth,
        bottom=x_rod_bottom.bottom,
        height=1.5,
    )

    clamp_clearance_up = ~clamp_clearance_bottom.z_mirror(y_bearing.center_z)

    clamp_bolt_up = ~Bolt.M3(12).add_nut(-E, side_clearance_size=30, angle=90).top_to_bottom().align(
        center_x=body.center_x, center_y=body.back + 9, top=body.top
    )

    clamp_bolt_down = ~clamp_bolt_up.z_mirror(y_bearing.center_z)

    y_belt_outer_clearance = ~Volume(
        center_x=y_bearing.center_x + Y_ROD_CENTER_TO_STEPPER_SHAFT_CENTER - 5,
        width=8,
        back=body.back - 1,
        front=body.front + 1,
        height=12,
        bottom=y_bearing.center_z + Y_PULLEYS_Z_OFFSET,
    )

    y_belt_inner_clearance = ~Volume(
        center_x=y_bearing.center_x + Y_ROD_CENTER_TO_STEPPER_SHAFT_CENTER + 5,
        width=8,
        back=body.back - 1,
        front=body.front + 1,
        height=12,
        bottom=y_bearing.center_z + Y_PULLEYS_Z_OFFSET,
    )

    def __stl__(self) -> Object:
        return self.back_to_bottom()


class YCarriageLeft(YCarriage):
    belt_fix_clearance_front = ~Volume(
        left=YCarriage.y_belt_inner_clearance.left,
        width=20,
        back=YCarriage.body.front - 16,
        front=YCarriage.body.front + E,
        bottom=YCarriage.y_belt_inner_clearance.bottom,
        top=YCarriage.y_belt_inner_clearance.top,
    ).fillet_depth(1, right=True).fillet_width(1, back=True)


y_carriage_left = YCarriageLeft()


class YBeltFixLeft(Part):
    belt = (
        ~Belt.GT2(60, 10)
        .front_to_left()
        .align(
            center_x=y_carriage_left.y_belt_inner_clearance.center_x,
            back=y_carriage_left.back - 10,
            center_z=y_carriage_left.y_belt_outer_clearance.center_z - 1.5,
        )
        .debug()
    )

    pulley = y_carriage_left.front_x_pulley

    body = Volume(
        left=y_carriage_left.y_belt_inner_clearance.left + TT,
        right=y_carriage_left.y_belt_inner_clearance.right - TT,
        front=y_carriage_left.front,
        back=y_carriage_left.center_y + 2,
        bottom=y_carriage_left.y_belt_outer_clearance.bottom + TT,
        top=y_carriage_left.y_belt_outer_clearance.top - TT,
    )

    bolt_holder = Hull(
        Volume(
            depth=16 - TT,
            front=body.front,
            left=body.left,
            right=y_carriage_left.right,
            bottom=body.bottom,
            top=body.top,
        )
        .fillet_depth(1, left=True)
        .fillet_width(1, back=True)
    )

    def __stl__(self) -> Object:
        return self.upside_down()


y_belt_fix_left = YBeltFixLeft()


class YCarriageRight(YCarriage):
    fan_fix_clearance = ~Volume(
        left=YCarriage.body.right,
        right=YCarriage.pulleys_holder.right + 1,
        back=YCarriage.pulleys_holder.front - 4.5,
        front=YCarriage.pulleys_holder.front + 1,
        bottom=YCarriage.y_belt_inner_clearance.bottom,
        top=YCarriage.pulleys_holder.top + E,
    ).reverse_fillet_top(2, back=True)

    belt_fix_clearance_front = ~Volume(
        left=YCarriage.y_belt_outer_clearance.left - 12,
        right=YCarriage.y_belt_outer_clearance.right,
        back=YCarriage.body.front - 12,
        front=YCarriage.body.front + E,
        bottom=YCarriage.y_belt_outer_clearance.bottom,
        top=YCarriage.y_belt_outer_clearance.top,
    ).fillet_depth(1, left=True)

    belt_fix_clearance_back = ~Volume(
        left=YCarriage.y_belt_outer_clearance.left - 12,
        right=YCarriage.y_belt_outer_clearance.right,
        back=YCarriage.body.back + 12,
        front=YCarriage.body.back - E,
        bottom=YCarriage.y_belt_outer_clearance.bottom,
        top=YCarriage.y_belt_outer_clearance.top,
    ).fillet_depth(1, left=True)
    y_fix_bolt = ~Bolt.M3(25).add_nut(-2, inline_clearance_size=20, angle=90).bottom_to_front().align(
        center_x=YCarriage.y_belt_outer_clearance.center_x - 9,
        center_y=YCarriage.body.center_y,
        center_z=YCarriage.y_belt_outer_clearance.center_z,
    )

    x_belt_clearance = ~Volume(
        center_x=YCarriage.y_bearing.center_x + Y_ROD_CENTER_TO_STEPPER_SHAFT_CENTER - 5,
        width=8,
        back=YCarriage.body.back - 1,
        front=YCarriage.body.front + 1,
        height=12,
        top=YCarriage.front_x_pulley.top,
    )

    def __stl__(self) -> Object:
        return self.front_to_bottom()


y_carriage_right = YCarriageRight().x_mirror(center=bed.center_x).y_mirror(center=y_carriage_left.center_y)


class YBeltFixFront(Part):
    belt = (
        ~Belt.GT2(100, 10, T=0.4)
        .front_to_left()
        .align(
            center_x=y_carriage_right.y_belt_outer_clearance.center_x,
            back=y_carriage_right.back,
            center_z=y_carriage_right.y_belt_outer_clearance.center_z - 1.5,
        )
        .debug()
    )

    bolt = ~y_carriage_right.y_fix_bolt

    body = Volume(
        left=y_carriage_right.y_belt_outer_clearance.left + TTT,
        right=y_carriage_right.y_belt_outer_clearance.right - TTT,
        back=y_carriage_right.center_y + 2,
        front=y_carriage_right.front,
        bottom=y_carriage_right.y_belt_outer_clearance.bottom + TTT,
        top=y_carriage_right.y_belt_outer_clearance.top - TTT,
    )

    bolt_holder = Volume(
        # y_carriage_right is y mirrored so back becomes front
        left=y_carriage_right.belt_fix_clearance_back.left + TTT,
        right=y_carriage_right.belt_fix_clearance_back.right - TTT,
        back=y_carriage_right.belt_fix_clearance_back.back + TTT,
        front=y_carriage_right.front,
        bottom=body.bottom,
        top=body.top,
    ).fillet_depth(1, right=True)

    def __stl__(self) -> Object:
        return self.upside_down()


y_belt_fix_front = YBeltFixFront()


class YBeltFixBack(Part):
    belt = (
        ~Belt.GT2(60, 10, T=0.4)
        .front_to_left()
        .align(
            center_x=y_carriage_right.y_belt_outer_clearance.center_x,
            back=y_carriage_right.back - 10,
            center_z=y_carriage_right.y_belt_outer_clearance.center_z - 1.5,
        )
        .debug()
    )

    bolt = ~y_carriage_right.y_fix_bolt

    body = Volume(
        left=y_carriage_right.y_belt_outer_clearance.left + TT,
        right=y_carriage_right.y_belt_outer_clearance.right - TT,
        front=y_carriage_right.center_y - 2,
        back=y_carriage_right.back,
        bottom=y_carriage_right.y_belt_outer_clearance.bottom + TT,
        top=y_carriage_right.y_belt_outer_clearance.top - TT,
    )

    bolt_holder = Volume(
        # y_carriage_right is y mirrored so back becomes front
        left=body.right,
        right=y_carriage_right.belt_fix_clearance_front.right - TT,
        back=y_carriage_right.back,
        front=y_carriage_right.belt_fix_clearance_front.front - T,
        bottom=body.bottom,
        top=body.top,
    ).fillet_depth(1, right=True)

    def __stl__(self) -> Object:
        return self.upside_down()


y_belt_fix_back = YBeltFixBack()


class YClamp(Part):
    y_bearing = y_carriage_left.y_bearing
    bolts = (
        y_carriage_left.y_clamp_bolt_bottom_front
        + y_carriage_left.y_clamp_bolt_bottom_back
        + y_carriage_left.y_clamp_bolt_top_front
        + y_carriage_left.y_clamp_bolt_top_back
    )

    body = Volume(
        left=y_carriage_left.y_bearing.left - 2,
        right=y_carriage_left.left,
        bottom=bolts.bottom - 1,
        top=bolts.top + 1,
        front=y_carriage_left.front,
        back=y_carriage_left.back,
    ).fillet_width()

    def __stl__(self) -> Object:
        return self.left_to_bottom()


y_clamp_left = YClamp()
y_clamp_right = YClamp().x_mirror(center=frame.center_x)


class YEndstopAttachmentBack(Part):
    y_rod = ~gantry.y_rod_right
    z_extrusion = ~frame.z_extrusion_right_back
    y_extrusion = ~frame.y_extrusion_right_top
    stepper_mount = ~xy_stepper_mount_right

    y_endstop = (
        ~MechanicalEndstopOnPCB(bolt=Bolt.M3(8).add_nut(-1, inline_clearance_size=10), z_offset=-3)
        .bottom_to_left()
        .bottom_to_front()
        .align(
            right=y_extrusion.left + 2,
            back=stepper_mount.front + 7,
            top=y_extrusion.bottom - 14,
        )
        .debug()
    )

    bolt = (
        ~Bolt.M5(10)
        .align(
            center_x=y_extrusion.center_x,
            center_y=y_endstop.front + 5,
            center_z=y_extrusion.bottom,
        )
        .debug()
    )

    attachment = Volume(
        center_x=y_extrusion.center_x,
        left=y_endstop.right,
        back=stepper_mount.front,
        front=bolt.front + 3,
        top=y_extrusion.bottom,
        height=5,
    ).fillet_height(6, front=True)

    body = (
        Volume(
            width=5,
            left=y_endstop.right,
            back=stepper_mount.front,
            front=y_endstop.front,
            top=attachment.bottom,
            bottom=y_endstop.bolts.bottom - 2,
        )
        .fillet_width(2, bottom=True)
        .reverse_fillet_top(right=True)
    )

    def __stl__(self) -> Object:
        return self.left_to_bottom()


y_endstop_attachement_back = YEndstopAttachmentBack()


class Feet(Part):
    z_extrusion = ~frame.z_extrusion_left_back
    y_extrusion = ~frame.y_extrusion_left_bottom
    x_extrusion = ~frame.x_extrusion_back_bottom

    BALL_DIAMETER = 44
    FEET_HEIGHT = 33

    right_bolt = ~Bolt.M5(10, head_clearance=10).align(
        center_x=z_extrusion.right + 40,
        center_y=x_extrusion.center_y,
        bottom=z_extrusion.bottom - 7,
    )

    front_bolt = ~Bolt.M5(10).align(
        center_x=y_extrusion.center_x,
        center_y=z_extrusion.front + 40,
        bottom=right_bolt.bottom,
    )

    center_bolt = ~Bolt.M8(20).align(
        center_x=z_extrusion.center_x,
        center_y=z_extrusion.center_y,
        bottom=z_extrusion.bottom - 10,
    )

    base = Surface.free(
        Circle(d=6).align(left=y_extrusion.left, back=x_extrusion.back),
        Circle(d=10).align(left=y_extrusion.left, front=front_bolt.front + 10),
        Circle(d=10).align(right=right_bolt.right + 10, back=x_extrusion.back),
        Circle(d=10).align(right=right_bolt.right + 10, front=x_extrusion.front),
        Circle(d=10).align(right=x_extrusion.left, front=front_bolt.front + 10),
    ).z_linear_extrude(6, top=z_extrusion.bottom)

    ball_holder = Tube(
        diameter=BALL_DIAMETER + 4,
        left=z_extrusion.left + 1,
        back=z_extrusion.back + 1,
        top=z_extrusion.bottom,
        height=FEET_HEIGHT,
    )

    fillet = Surface.fillet(10).y_mirror().z_rotational_extrude(
        radius=BALL_DIAMETER / 2 + 2,
        center_x=ball_holder.center_x,
        center_y=ball_holder.center_y,
        top=base.bottom,
    ) & Volume(
        left=base.left,
        right=base.right,
        back=base.back,
        front=base.front,
        top=base.bottom,
        bottom=ball_holder.bottom,
    )

    squash_ball = ~Sphere(BALL_DIAMETER).align(
        center_x=ball_holder.center_x,
        center_y=ball_holder.center_y,
        center_z=ball_holder.bottom + 1,
    )

    def __stl__(self) -> Object:
        return self.upside_down()


feet_left_back = Feet()
feet_right_back = feet_left_back.x_mirror(center=frame.center_x)
feet_left_front = feet_left_back.y_mirror(center=frame.center_y)
feet_right_front = feet_right_back.y_mirror(center=frame.center_y)


class YEndstopFront(Part):
    endstop = (
        ~MechanicalEndstopOnPCB(bolt=Bolt.M3(10).add_nut(-1, inline_clearance_size=10))
        .upside_down(x_axis=True)
        .align(
            right=xy_idler_right.body.left - 1,
            back=frame.x_extrusion_front_top.back - 16,
            top=frame.x_extrusion_front_top.bottom - 8,
        )
        .debug()
    )

    bolt = ~Bolt.M5(10).align(
        center_x=endstop.left - 10,
        center_y=frame.x_extrusion_front_top.center_y,
        bottom=endstop.top - 2,
    )

    extrusion_attachment = Volume(
        right=frame.z_extrusion_right_front.left,
        left=bolt.left - 10,
        back=frame.x_extrusion_front_top.back + 2,
        front=frame.x_extrusion_front_top.front - 2,
        top=frame.x_extrusion_front_top.bottom,
        bottom=endstop.top,
    ).fillet_height(12, left=True)

    endstop_attachment = (
        Volume(
            left=endstop.left - 2,
            right=endstop.right + 2,
            front=extrusion_attachment.back,
            back=endstop.back,
            top=extrusion_attachment.top,
            bottom=extrusion_attachment.bottom,
        )
        .fillet_height(back=True)
        .reverse_fillet_front(6, left=True, right=True)
    )


y_endstop_front = YEndstopFront()


class ExtruderStepperMount(Part):
    y_extrusion = ~frame.y_extrusion_right_top

    stepper = (
        ~StepperMotor.nema17(
            height=45,
            gearbox_height=24,
            shaft_diameter=10,
            bolt=Bolt.M3(10, head_clearance=4).top_to_bottom(),
        )
        .bottom_to_front()
        .align(
            left=y_extrusion.right + 2,
            back=y_extrusion.back + 50,
            top=y_extrusion.top + 6,
        )
        .debug()
    )

    stepper_holder = (
        Volume(
            left=y_extrusion.right,
            right=stepper.right,
            front=stepper.body.back - TTT,
            back=stepper.back - 4,
            bottom=stepper.bottom,
            top=stepper.top,
        )
        .fillet_depth(4, bottom=True)
        .fillet_depth(4, top=True, right=True)
    )

    bolts = (
        ~Bolt.M3(16, thread_clearance=5)
        .add_nut(-4, side_clearance_size=10, angle=-90)
        .bottom_to_back()
        .align(
            center_x=stepper.center_x + 15.52,
            center_y=stepper_holder.back,
            center_z=stepper.center_z + 15.52,
        )
        .x_symmetry(center=stepper.center_x)
        .z_symmetry(center=stepper.center_z)
        .debug()
    )

    attachment = (
        Volume(
            right=stepper_holder.left + E,
            left=y_extrusion.left + 2,
            back=stepper_holder.back,
            front=stepper.front,
            bottom=y_extrusion.top,
            top=stepper_holder.top,
        )
        .fillet_height(4, left=True)
        .fillet_height(4, front=True, right=True)
    )

    attachment_fillet = (
        Fillet(2)
        .z_linear_extrude(bottom=attachment.bottom, top=attachment.top)
        .z_rotate(180)
        .align(left=attachment.right, back=stepper_holder.front)
    )

    bolt_top_back = ~Bolt.M6(12).upside_down().align(
        center_x=y_extrusion.center_x,
        center_y=stepper_holder.center_y,
        center_z=y_extrusion.top,
    )
    bolt_top_front = ~bolt_top_back.y_mirror(attachment.center_y)

    def __stl__(self) -> Object:
        return self.back_to_bottom()


extruder_stepper_mount = ExtruderStepperMount()


class SpoolHolder(Part):
    LENGTH = 88

    y_extrusion = ~frame.y_extrusion_right_middle

    rod = (
        ~Cylinder(h=62, d=8 + 2 * T)
        .bottom_to_right()
        .align(
            left=y_extrusion.right + 6,
            center_y=y_extrusion.back + 80,
            center_z=y_extrusion.top + 3,
        )
        .slide(z=8)
        .debug()
    )

    bearing_center = (
        ~RotationBearing.b608zz(T=1, hole=False)
        .bottom_to_right()
        .align(
            center_x=rod.center_x,
            center_y=rod.center_y,
            center_z=rod.center_z,
        )
        .debug()
    )

    bearing_right = (
        ~RotationBearing.b608zz(T=1, hole=False)
        .bottom_to_right()
        .align(
            center_x=rod.center_x + LENGTH / 4,
            center_y=rod.center_y,
            center_z=rod.center_z,
        )
        .debug()
    )

    bearing_left = (
        ~RotationBearing.b608zz(T=1, hole=False)
        .bottom_to_right()
        .align(
            center_x=rod.center_x - LENGTH / 4,
            center_y=rod.center_y,
            center_z=rod.center_z,
        )
        .debug()
    )

    stopper_right = (
        Volume(
            left=rod.right,
            width=4,
            center_y=rod.center_y,
            depth=30,
            bottom=rod.bottom - 6,
            top=bearing_right.top + 2,
        )
        .fillet_width(12, top=True)
        .fillet_width(12, back=True, bottom=True)
    )

    bolt_right = ~Bolt.M6(16).bottom_to_right().slide(y=20).align(
        center_x=y_extrusion.right,
        center_y=stopper_right.center_y + 10,
        center_z=y_extrusion.center_z,
    )

    arm = (
        Volume(
            left=y_extrusion.right,
            right=stopper_right.right - T,
            center_y=rod.center_y,
            depth=30,
            top=rod.top + 2,
            bottom=stopper_right.bottom,
        )
        .fillet_width(8, top=True)
        .fillet_width(12, front=True, bottom=True)
    )

    fix = (
        Volume(
            left=y_extrusion.left + 2,
            right=y_extrusion.right + 6,
            back=arm.back,
            depth=32,
            bottom=y_extrusion.bottom + 2,
            top=y_extrusion.top + 6,
        )
        .fillet_width(4, top=True)
        .fillet_width(8, bottom=True, front=True)
        .fillet_height(16, left=True)
    )

    reinforcement = Hull(
        Volume(
            width=1,
            left=fix.right - 1,
            depth=6,
            back=fix.back,
            height=E,
            bottom=fix.bottom,
        ),
        Volume(
            width=1,
            left=fix.right,
            depth=6,
            back=fix.back,
            height=E,
            top=arm.bottom + E,
        ),
        Volume(
            width=1,
            back=fix.back,
            right=stopper_right.right,
            depth=6,
            height=E,
            top=arm.bottom + E,
        ),
    )

    stopper_left = Volume(
        left=y_extrusion.right,
        width=6,
        center_y=fix.center_y,
        depth=fix.depth,
        bottom=y_extrusion.top,
        top=bearing_right.top + 2,
    ).fillet_width(12, top=True)

    bolt_top = ~Bolt.M6(12).upside_down().align(
        center_x=y_extrusion.center_x,
        center_y=fix.center_y,
        center_z=y_extrusion.top,
    )

    def __stl__(self) -> Object:
        return self.back_to_bottom()


spool_holder = SpoolHolder()


class ZBedMount(SymmetricPart, y=True):
    extrusion = ~bed.y_extrusion_left
    z_rod = ~gantry.z_rod_left_front
    t8 = ~gantry.z_threaded_rod_left

    bearing = (
        ~LinearBearing.LM12UU()
        .add_rod_clearance()
        .align(
            center_x=z_rod.center_x,
            center_y=z_rod.center_y,
            center_z=extrusion.center_z,
        )
        .debug()
    )

    bolts = ~Bolt.M5(10, head_clearance=30).bottom_to_left().align(
        left=extrusion.left - 10,
        center_y=bearing.back - 7,
        center_z=extrusion.center_z,
    ).slide(y=-10).y_symmetry(center=z_rod.center_y)

    base = Surface.free(
        Circle(d=30).align(center_x=bearing.center_x, center_y=bearing.center_y),
        Circle(d=4).align(front=bolts.front, right=extrusion.right - 2),
        Circle(d=4).align(back=bolts.back, right=extrusion.right - 2),
        Circle(d=8).align(front=bolts.front, right=extrusion.left - 2),
        Circle(d=8).align(back=bolts.back, right=extrusion.left - 2),
    ).z_linear_extrude(bottom=bearing.bottom + E, top=bearing.top + 2)

    insert = ~Volume(
        right=bearing.center_y,
        width=40,
        center_y=base.center_y,
        depth=z_rod.depth + 2,
        center_z=base.center_z,
        height=base.height + 2,
    )

    arm = Volume(
        left=base.left,
        center_x=t8.center_x,
        back=t8.back,
        front=z_rod.center_y,
        top=base.top,
        height=2,
    )

    left_border = Volume(
        left=arm.left,
        width=3,
        back=arm.back,
        front=arm.front,
        top=arm.bottom,
        height=7,
    )
    right_border = Volume(
        right=arm.right,
        width=3,
        back=arm.back,
        front=arm.front,
        top=arm.bottom,
        height=7,
    )
    center_border = Volume(
        center_x=arm.center_x,
        width=3,
        back=arm.back,
        front=arm.front,
        top=arm.bottom,
        height=7,
    )

    rings = Volume(
        left=base.left,
        center_x=t8.center_x,
        back=t8.back,
        front=z_rod.center_y,
        top=arm.bottom,
        height=7,
    ) & Union(
        Tube(diameter=8 * i, center_x=0, center_y=0, bottom=0, height=7).tunnel(8 * i - 4) for i in range(3, 15)
    ).align(center_x=t8.center_x, center_y=t8.center_y, top=arm.bottom)

    brass_nut_base = Tube(
        diameter=21.8,
        center_x=t8.center_x,
        center_y=t8.center_y,
        top=arm.bottom - E,
        bottom=rings.bottom - 1,
    )

    brass_nut = ~BrassNut.T8(Bolt.M3(16).add_nut(-5, inline_clearance_size=5)).align(
        center_x=t8.center_x, center_y=t8.center_y, top=brass_nut_base.bottom
    )

    tilted_clearance = ~(
        Chamfer(radius=extrusion.width)
        .z_rotate(180)
        .y_linear_extrude(extrusion.depth, center_y=extrusion.center_y)
        .align(
            center_x=extrusion.left,
            center_z=extrusion.bottom,
        )
        + Volume(
            left=extrusion.left,
            right=extrusion.right,
            back=extrusion.back,
            front=extrusion.front,
            top=extrusion.bottom + 2,
            bottom=base.bottom - 1,
        )
    )

    top_bolts = ~Bolt.M5(10).bottom_to_top().align(
        center_x=extrusion.center_x,
        center_y=bearing.center_y + 16,
        center_z=extrusion.top + 2,
    ).slide(y=20).y_symmetry(bearing.center_y)

    def __stl__(self) -> Object:
        return self.upside_down()


z_bed_mount_left = ZBedMount()
z_bed_mount_right = ZBedMount().x_mirror(center=frame.center_x)


class ZBracketBottom(Part):
    extrusion = ~frame.y_extrusion_left_bottom
    rod = ~gantry.z_rod_left_back

    front_bolt = ~Bolt.M5(10, head_clearance=10).bottom_to_right().slide(z=20).align(
        right=extrusion.right + 8,
        back=rod.front,
        center_z=extrusion.center_z,
    )

    bottom_bolt = ~Bolt.M6(10).align(
        center_x=extrusion.center_x,
        center_y=front_bolt.center_y,
        center_z=extrusion.bottom - 2,
    )

    body = (
        Volume(
            left=extrusion.left + 3,
            right=extrusion.right + 6,
            center_y=front_bolt.center_y,
            depth=18,
            bottom=rod.bottom + E,
            top=extrusion.top - 4,
        )
        .fillet_width(4, top=True)
        .fillet_height(6, left=True)
        # .fillet_height(4, right=True, front=True)
    )

    rod_holder = Surface.free(
        Circle(d=8).align(right=body.right, front=body.front),
        Circle(d=6).align(right=rod.right + 3, front=rod.front + 3),
        Circle(d=6).align(right=rod.right + 3, back=rod.back - 3),
        Circle(d=4).align(left=rod.left - 13, back=rod.back - 3),
    ).z_linear_extrude(bottom=body.bottom, distance=15)

    rod_holder_clearance = ~Volume(
        right=rod.left + E,
        width=20,
        center_y=rod.center_y,
        depth=2,
        bottom=rod_holder.bottom - E,
        top=rod_holder.top + E,
    )
    rod_holder_bolt = ~Bolt.M3(16, head_clearance=10).add_nut(
        -0.1, angle=90, inline_clearance_size=20
    ).bottom_to_back().align(
        center_x=rod.left - 5,
        center_y=rod_holder_clearance.center_y,
        center_z=rod_holder.center_z,
    )


z_bracket_bottom_left_back = ZBracketBottom()
z_bracket_bottom_left_front = z_bracket_bottom_left_back.y_mirror(center=gantry.z_threaded_rod_left.center_y)
z_bracket_bottom_right_back = z_bracket_bottom_left_back.x_mirror(center=bed.center_x)
z_bracket_bottom_right_front = z_bracket_bottom_right_back.y_mirror(center=gantry.z_threaded_rod_right.center_y)


class ZBracketTopLeft(Part):
    extrusion = ~frame.y_extrusion_left_middle
    rod = ~gantry.z_rod_left_front

    body = (
        Volume(
            left=extrusion.left + 3,
            right=extrusion.right + 6,
            back=rod.back - 18,
            front=rod.front - 10,
            bottom=extrusion.bottom + 4,
            top=rod.top - E,
        )
        .fillet_height(10, left=True)
        .fillet_height(4, right=True)
        .fillet_width(4, bottom=True)
    )

    rod_holder = Surface.free(
        Circle(d=8).align(right=body.right, back=body.back),
        Circle(d=6).align(right=rod.right + 3, back=rod.back - 5),
        Circle(d=6).align(right=rod.right + 3, front=rod.front + 3),
        Circle(d=4).align(left=rod.left - 15, front=rod.front + 3),
    ).z_linear_extrude(top=body.top, distance=10)

    rod_holder_bolt = ~Bolt.M3(20, head_clearance=20).add_nut(
        -4, angle=90, inline_clearance_size=20
    ).bottom_to_front().align(
        center_x=rod.left - 5,
        center_y=rod.center_y - 2,
        center_z=rod_holder.center_z,
    )
    rod_holder_clearance = ~Volume(
        right=rod.left + 1,
        width=20,
        center_y=rod.center_y,
        depth=2,
        center_z=rod_holder.center_z,
        height=rod_holder.height + 1,
    )

    top_bolt = ~Bolt.M6(12, head_clearance=40).top_to_bottom().align(
        center_x=extrusion.center_x,
        center_y=body.center_y,
        center_z=extrusion.top + 3,
    )

    front_bolt = (
        ~Bolt.M6(12)
        .bottom_to_right()
        .align(
            center_x=extrusion.right,
            center_y=body.center_y,
            center_z=extrusion.center_z,
        )
        .slide(z=-20)
        .debug()
    )

    rounding = (
        Fillet(6)
        .linear_extrude(rod_holder.height)
        .z_rotate(-90)
        .align(
            right=extrusion.right + 1.5,
            top=rod_holder.top,
            back=body.front - E,
        )
    )

    def __stl__(self) -> Object:
        return self.upside_down()


z_bracket_top_left_front = ZBracketTopLeft()
z_bracket_top_left_back = z_bracket_top_left_front.y_mirror(gantry.z_threaded_rod_left.center_y)
z_bracket_top_right_front = z_bracket_top_left_front.x_mirror(bed.center_x)
z_bracket_top_right_back = z_bracket_top_left_back.x_mirror(bed.center_x)


class ZBracketTop(SymmetricPart, y=True):
    extrusion = ~frame.y_extrusion_left_middle
    rod = ~gantry.z_rod_left_front.debug()

    body = (
        Volume(
            left=extrusion.left + 3,
            right=extrusion.right - 1,
            back=0,
            front=rod.front - 10,
            bottom=extrusion.bottom + 4,
            top=rod.top - E,
        )
        .fillet_height(4, left=True, front=True)
        .fillet_width(4, bottom=True)
    )

    rod_holder = Surface.free(
        Circle(d=16).align(center_x=extrusion.right - 1, front=rod.back),
        Circle(d=6).align(right=rod.right + 3, back=rod.back - 5),
        Circle(d=6).align(right=rod.right + 3, front=rod.front + 3),
        Circle(d=4).align(left=rod.left - 15, front=rod.front + 3),
        Circle(d=4).align(center_x=body.right, front=body.front),
    ).z_linear_extrude(top=body.top, distance=10)

    rod_holder_bolt = ~Bolt.M3(20, head_clearance=20).add_nut(
        -4, angle=90, inline_clearance_size=20
    ).bottom_to_front().align(
        center_x=rod.left - 5,
        center_y=rod.center_y - 2,
        center_z=rod_holder.center_z,
    )
    rod_holder_clearance = ~Volume(
        right=rod.left + 1,
        left=extrusion.left,
        center_y=rod.center_y,
        depth=2,
        center_z=rod_holder.center_z,
        height=rod_holder.height + 1,
    )

    top_bolt = ~Bolt.M6(12, head_clearance=40).top_to_bottom().align(
        center_x=extrusion.center_x,
        center_y=body.front - 10,
        center_z=extrusion.top + 3,
    )

    side_bolt = (
        ~Bolt.M6(12)
        .bottom_to_left()
        .align(
            center_x=extrusion.left,
            center_y=0,
            center_z=extrusion.center_z,
        )
        .slide(z=-20)
        .debug()
    )


z_bracket_top = ZBracketTop()
z_bracket_top.render_to_file()


class ZStepperMount(Part):
    extrusion = ~frame.y_extrusion_left_bottom
    stepper = ~gantry.z_stepper_left

    bearing = (
        ~RotationBearing.b605zz()
        .align(
            center_x=stepper.center_x,
            center_y=stepper.center_y,
            bottom=stepper.top + 2,
        )
        .debug()
    )

    side_bolt_front = ~Bolt.M5(10).bottom_to_right().slide(y=20).align(
        right=extrusion.right + 7,
        center_y=stepper.front + 15,
        center_z=extrusion.center_z,
    )

    side_bolt_back = ~side_bolt_front.y_mirror(stepper.center_y)

    top_bolt_front = ~Bolt.M5(10).top_to_bottom().align(
        center_x=extrusion.center_x,
        center_y=side_bolt_front.center_y - 3,
        center_z=extrusion.top + 2,
    )

    top_bolt_back = ~top_bolt_front.y_mirror(stepper.center_y)
    top_bold_center = ~Bolt.M5(10).top_to_bottom().align(
        center_x=extrusion.center_x,
        center_y=stepper.center_y,
        center_z=extrusion.top + 2,
    )

    body = (
        Volume(
            left=extrusion.left + 4,
            right=extrusion.right + 4,
            back=top_bolt_back.back - 4,
            center_y=stepper.center_y,
            bottom=extrusion.bottom + 4,
            top=extrusion.top + 7,
        )
        .fillet_width(r=5, bottom=True, front=True, back=True)
        .fillet_depth(r=4, top=True, right=True)
        .fillet_height(r=5, left=True, front=True, back=True)
    )

    stepper_box = (
        Volume(
            left=extrusion.right,
            right=stepper.right + 2,
            back=stepper.back - 8,
            center_y=stepper.center_y,
            bottom=extrusion.bottom + 4,
            top=body.top,
        )
        .fillet_height(r=5, right=True, front=True, back=True)
        .chamfer_depth(28, right=True, bottom=True)
    )

    stepper_clearance = ~Volume(
        left=stepper_box.left - E,
        right=stepper_box.right + E,
        back=stepper_box.back + 4,
        front=stepper_box.front - 4,
        bottom=stepper_box.bottom - 10,
        top=stepper_box.top - 8,
    ).fillet_width(r=4, top=True, front=True, back=True)

    tilted_clearance = (
        ~Volume(
            width=stepper_clearance.width,
            center_x=stepper_box.center_x,
            depth=stepper_box.depth + EE,
            center_y=stepper.center_y,
            height=stepper_box.height,
            top=stepper_clearance.top - 25,
        )
        .y_rotate(35)
        .disable()
    )

    def __stl__(self) -> Object:
        return self.upside_down()


z_stepper_mount_left = ZStepperMount()
z_stepper_mount_right = z_stepper_mount_left.x_mirror(frame.center_x)


class ZBottomEndStop(Part):
    endstop = (
        MechanicalEndstopOnPCB(
            bolt=Bolt.M3(16).add_nut(-1, inline_clearance_size=10).upside_down(),
            z_offset=5,
        )
        .top_to_right()
        .align(
            right=gantry.z_rod_right_back.left - 10,
            front=gantry.z_rod_right_back.center_y,
            top=frame.y_extrusion_right_bottom.top,
        )
        .debug()
    )
    endstop_attachment = Volume(
        left=endstop.right + T,
        width=6,
        front=endstop.front,
        back=endstop.back,
        bottom=endstop.bottom,
        top=endstop.top,
    )
    arm = Volume(
        left=endstop_attachment.right,
        right=frame.y_extrusion_right_bottom.left - T,
        back=endstop_attachment.back,
        depth=6,
        bottom=endstop_attachment.bottom,
        top=frame.y_extrusion_right_bottom.top - 2,
    ).reverse_fillet_left(top=True)
    bolt = ~Bolt.M5(10).bottom_to_left().align(
        center_x=frame.y_extrusion_right_bottom.left,
        center_y=arm.back - 10,
        center_z=frame.y_extrusion_right_bottom.center_z,
    ).debug().slide(z=20)
    frame_attachment = Volume(
        right=frame.y_extrusion_right_bottom.left - T,
        width=6,
        front=arm.back,
        center_y=bolt.center_y,
        top=frame.y_extrusion_right_bottom.top - 2,
        bottom=frame.y_extrusion_right_bottom.bottom + 6,
    ).fillet_width(6, bottom=True)


z_bottom_endstop = ZBottomEndStop()


class BoardMountSide(Part):
    z_extrusion = ~frame.z_extrusion_left_back

    def init(  # type: ignore[override]
        self,
        board: Board,
        side: Literal["left", "right"] = "left",
        bolt_spacing: float = 15,
    ) -> None:
        if side == "left":
            self.board = (
                ~board.top_to_right()
                .align(
                    left=self.z_extrusion.left + 15,
                    back=self.z_extrusion.front + 10,
                    center_z=self.z_extrusion.center_z,
                )
                .debug()
            )
            self.mount = (
                Volume(
                    left=self.z_extrusion.left + 2,
                    width=6,
                    back=self.z_extrusion.front,
                    front=self.board.front + 2,
                    top=self.board.top + 2,
                    bottom=self.board.bottom - 2,
                ).fillet_width()
                - Volume(
                    left=self.z_extrusion.left,
                    width=10,
                    back=self.z_extrusion.front + 20,
                    front=self.board.front - 10,
                    top=self.board.top - 10,
                    bottom=self.board.bottom + 10,
                ).fillet_width()
            )
            self.z_bolt_top = ~Bolt.M6(10).bottom_to_front().align(
                center_x=self.z_extrusion.center_x,
                center_y=self.z_extrusion.front,
                center_z=self.mount.top + 10,
            )

            self.z_bolt_bottom = ~Bolt.M6(10).bottom_to_front().align(
                center_x=self.z_extrusion.center_x,
                center_y=self.z_extrusion.front,
                center_z=self.mount.bottom - 10,
            )

            self.z_attach = Volume(
                center_x=self.z_extrusion.center_x,
                width=26,
                back=self.z_extrusion.front,
                depth=6,
                bottom=self.z_bolt_bottom.bottom - 5,
                top=self.z_bolt_top.top + 5,
            ).fillet_depth(13)

        elif side == "right":
            self.board = (
                ~board.top_to_right()
                .align(
                    left=self.z_extrusion.left + 15,
                    front=self.z_extrusion.back - 10,
                    center_z=self.z_extrusion.center_z,
                )
                .debug()
            )
            self.mount = (
                Volume(
                    left=self.z_extrusion.left + 2,
                    width=6,
                    front=self.z_extrusion.back,
                    back=self.board.back - 2,
                    top=self.board.top + 2,
                    bottom=self.board.bottom - 2,
                ).fillet_width()
                - Volume(
                    left=self.z_extrusion.left,
                    width=10,
                    front=self.z_extrusion.back - 20,
                    back=self.board.back + 10,
                    top=self.board.top - 10,
                    bottom=self.board.bottom + 10,
                ).fillet_width()
            )

            self.z_bolt_top = ~Bolt.M6(10).bottom_to_back().align(
                center_x=self.z_extrusion.center_x,
                center_y=self.z_extrusion.back,
                center_z=self.mount.top + bolt_spacing,
            )

            self.z_bolt_bottom = ~Bolt.M6(10).bottom_to_back().align(
                center_x=self.z_extrusion.center_x,
                center_y=self.z_extrusion.back,
                center_z=self.mount.bottom - bolt_spacing,
            )

            self.z_attach = Volume(
                center_x=self.z_extrusion.center_x,
                width=26,
                front=self.z_extrusion.back,
                depth=6,
                bottom=self.z_bolt_bottom.bottom - 5,
                top=self.z_bolt_top.top + 5,
            ).fillet_depth(13)

    def __stl__(self) -> Object:
        return self.left_to_bottom()


class BoardMountCorner(Part):
    z_extrusion = ~frame.z_extrusion_right_back
    y_extrusion = ~frame.y_extrusion_right_bottom

    def init(  # type: ignore[override]
        self,
        board: Object,
        hollow_offset_bottom: float = 10,
        hollow_offset_side: float = 10,
        brand: str | None = None,
    ) -> None:
        self.board = (
            ~board.bottom_to_left()
            .align(
                left=self.y_extrusion.center_x - 5,
                back=self.z_extrusion.front + 10,
                bottom=self.y_extrusion.top + 10,
            )
            .debug()
        )

        self.mount = (
            Volume(
                left=self.z_extrusion.left + 2,
                width=6,
                back=self.z_extrusion.front,
                front=self.board.front + 2,
                top=self.board.top + 2,
                bottom=self.y_extrusion.top,
            ).fillet_width()
            - Volume(
                left=self.z_extrusion.left,
                width=10,
                back=self.z_extrusion.front + hollow_offset_side,
                front=self.board.front - 10,
                top=self.board.top - 10,
                bottom=self.y_extrusion.top + hollow_offset_bottom,
            ).fillet_width()
        )

        self.z_bolt = ~Bolt.M6(10).bottom_to_front().align(
            center_x=self.z_extrusion.center_x,
            center_y=self.z_extrusion.front,
            center_z=self.mount.top + 10,
        )
        self.z_attach = (
            Volume(
                center_x=self.z_extrusion.center_x,
                width=26,
                back=self.z_extrusion.front,
                depth=6,
                bottom=self.y_extrusion.top,
                top=self.z_bolt.top + 5,
            )
            .fillet_depth(13, top=True)
            .fillet_width(back=True, bottom=True)
        )

        self.y_bolt = ~Bolt.M6(10).upside_down().align(
            center_x=self.y_extrusion.center_x,
            center_y=self.mount.front + 10,
            center_z=self.y_extrusion.top,
        )
        self.y_attach = (
            Volume(
                center_x=self.z_extrusion.center_x,
                width=26,
                back=self.z_extrusion.front,
                front=self.y_bolt.front + 5,
                bottom=self.y_extrusion.top,
                height=6,
            )
            .fillet_height(13, front=True)
            .fillet_width(back=True, bottom=True)
        )

    def __stl__(self) -> Object:
        return self.left_to_bottom()


class PowerSupplyMount(BoardMountCorner):
    def init(self) -> None:  # type: ignore[override]
        power_supply = Board.smps300rs(Bolt.M3(20).add_nut(-1).upside_down())
        return super().init(power_supply, hollow_offset_bottom=20)


power_supply_mount = (
    PowerSupplyMount()
    .x_rotate(90)
    .align(
        center_x=frame.y_extrusion_right_bottom.center_x,
        front=frame.z_extrusion_right_front.back,
        bottom=frame.y_extrusion_right_bottom.top,
    )
)


class ScreenMount(BoardMountSide):
    def init(self) -> None:  # type: ignore[override]
        screen = Board.lcd12864(Bolt.M3(25).add_nut(-1).upside_down().down(7.5))
        return super().init(screen, side="right")


screen_mount = (
    ScreenMount()
    .z_rotate(-90)
    .align(
        right=frame.z_extrusion_right_back.left,
        center_y=frame.z_extrusion_right_back.center_y,
        top=bed.top,
    )
)


class MainboardMount(BoardMountCorner):
    def init(self) -> None:  # type: ignore[override]
        mainboard = Board.mks_sbase(Bolt.M3(20).add_nut(-1).upside_down())
        return super().init(mainboard, hollow_offset_side=20)


mainboard_mount = (
    MainboardMount()
    .x_rotate(180)
    .align(
        center_x=frame.z_extrusion_right_front.center_x,
        front=frame.z_extrusion_right_front.back,
        top=frame.y_extrusion_right_middle.bottom,
    )
)


class RaspberryMount(BoardMountSide):
    def init(self) -> None:  # type: ignore[override]
        mainboard = Board.raspberry_pi_3b(Bolt.M3(26).add_nut(-E, inline_clearance_size=10).upside_down())
        return super().init(mainboard)


raspberry_mount = (
    RaspberryMount()
    .z_rotate(180)
    .y_rotate(180)
    .align(
        center_x=frame.z_extrusion_right_front.center_x,
        front=frame.z_extrusion_right_front.back,
        top=mainboard_mount.bottom - 10,
    )
)


class PowerPlugMount(Part):
    z_extrusion = ~frame.z_extrusion_right_front
    x_extrusion = ~frame.x_extrusion_front_bottom

    holder = Volume(
        right=z_extrusion.left - T,
        width=60,
        back=x_extrusion.back + 2,
        front=x_extrusion.front - 2,
        bottom=x_extrusion.top + T,
        height=50,
    ).fillet_depth(3, left=True, top=True)

    hollow = (
        ~Volume(
            center_x=holder.center_x,
            center_y=holder.center_y,
            center_z=holder.center_z,
            width=48,
            depth=z_extrusion.depth,
            height=28,
        )
        .chamfer_depth(3, right=True)
        .fillet_depth(1, left=True)
        .debug()
    )

    fixation_bolt_left = (
        ~Bolt.M6(10)
        .upside_down()
        .align(
            center_x=holder.left - 8,
            center_y=x_extrusion.center_y,
            center_z=x_extrusion.top,
        )
        .debug()
    )
    fixation_bolt_top = (
        ~Bolt.M6(10)
        .bottom_to_left()
        .align(
            center_x=z_extrusion.left,
            center_y=z_extrusion.center_y,
            center_z=holder.top + 8,
        )
        .debug()
    )

    fixation_left = Volume(
        right=holder.left - E,
        width=15,
        center_y=z_extrusion.center_y,
        depth=holder.depth,
        bottom=x_extrusion.top,
        height=4,
    ).fillet_height(9, left=True)
    fixation_top = Volume(
        right=z_extrusion.left,
        width=4,
        center_y=z_extrusion.center_y,
        depth=holder.depth,
        bottom=holder.top - E,
        height=15,
    ).fillet_width(9, top=True)

    def __stl__(self) -> Object:
        return self.back_to_bottom()


power_plug_mount = PowerPlugMount()


class CableClip(Part):
    body = Volume(width=12, depth=5, back=-1.5, height=6).fillet_height(1, back=True).fillet_height(4, front=True)

    center_clearance = ~Volume(
        center_x=body.center_x,
        width=6,
        back=0,
        front=body.front + E,
        bottom=body.bottom - E,
        top=body.top + E,
    ).fillet_height(1, back=True)

    side_clearance_right = ~Volume(
        left=4,
        width=5,
        front=2,
        back=0,
        bottom=body.bottom - E,
        top=body.top + E,
    )
    side_clearance_left = ~side_clearance_right.x_mirror()


cable_clip = CableClip()


class MotorCableGuide(Part):
    body = (
        Volume(
            left=frame.y_extrusion_right_middle.right,
            width=15,
            front=frame.z_extrusion_right_front.front + 15,
            back=mainboard_mount.back,
            top=frame.y_extrusion_right_middle.top - 2,
            bottom=frame.y_extrusion_right_middle.bottom + 2,
        )
        .fillet_width(back=True, r=8)
        .fillet_height(front=True, right=True)
    )
    front_part = Volume(
        left=frame.z_extrusion_right_front.left + 2,
        right=body.left,
        back=frame.z_extrusion_right_front.front,
        front=body.front,
        top=body.top,
        bottom=body.bottom,
    ).fillet_depth(left=True, r=8)

    bolt_back = ~Bolt.M5(30).bottom_to_right().align(
        right=body.right + E,
        back=body.back + 4,
        center_z=frame.y_extrusion_right_middle.center_z,
    )
    bolt_front = ~Bolt.M5(30).bottom_to_front().align(
        center_x=frame.z_extrusion_right_front.center_x,
        front=front_part.front + E,
        center_z=front_part.center_z,
    )
    cables = ~Volume(
        left=frame.z_extrusion_right_front.left + 6,
        right=body.right - 4,
        back=bolt_back.front + 4,
        front=body.front - 5,
        top=body.top + E,
        bottom=body.bottom + 4,
    ).fillet_height()
    cutout = ~(
        Union(
            Volume(
                left=frame.y_extrusion_right_middle.right - E,
                width=4,
                center_y=frame.z_extrusion_right_front.back - 110 + 20 * x,
                depth=10,
                bottom=frame.y_extrusion_right_middle.bottom - 5,
                top=frame.y_extrusion_right_middle.top + E,
            ).fillet_height(right=True)
            for x in range(5)
        )
        + Volume(
            center_x=frame.z_extrusion_right_front.center_x,
            width=10,
            back=frame.z_extrusion_right_front.front - E,
            depth=4,
            bottom=body.bottom - E,
            top=body.top + E,
        ).fillet_height(front=True)
    )


motor_cable_guide = MotorCableGuide()

frame_spacer = Volume(
    center_x=frame.y_extrusion_right_top.center_x,
    width=30,
    back=frame.z_extrusion_right_back.front,
    depth=3,
    top=frame.y_extrusion_right_top.bottom,
    bottom=frame.y_extrusion_right_middle.top,
).fillet_depth()
z_rod_spacer = Volume(
    center_x=frame.z_extrusion_right_front.center_x,
    width=30,
    front=frame.z_extrusion_right_front.back,
    back=z_bracket_top_right_front.body.front,
    bottom=frame.y_extrusion_right_middle.top,
    height=3,
).fillet_height()

if __name__ == "__main__":
    (
        x_carriage
        + x_axis_pulleys
        + cable_clamp_back
        + extruder_clamp
        + cable_chain_carriage_attachment
        + cable_clamp_top
        + tunnel
    ).render_to_file("x_carriage_assembled")

    (
        y_carriage_right
        + xy_stepper_mount_right
        + xy_idler_right
        + xy_idler_clamp_right
        + y_endstop_attachement_back
        + y_belt_fix_front.color("blue")
        + y_belt_fix_back.color("green")
        + cable_chain_frame_attachment
        + cable_clamp_frame
    ).render_to_file("right_side")

    (y_carriage_left + xy_stepper_mount_left + xy_idler_left + xy_idler_clamp_left + y_belt_fix_left).render_to_file(
        "left_side"
    )

    (
        (bed + glass_plate + gantry + frame).background()
        + (
            glass_plate_corner_left_front
            + glass_plate_corner_right_front
            + glass_plate_front_fix
            + xy_idler_left
            + xy_idler_right
            + xy_idler_clamp_left
            + xy_idler_clamp_right
            + xy_stepper_mount_right
            + xy_stepper_mount_left
            + y_endstop_attachement_back
            + cable_chain_frame_attachment
            + cable_clamp_frame
            + extruder_stepper_mount
            + y_endstop_front
            # + feet_left_back
            # + feet_right_back
            # + feet_left_front
            # + feet_right_front
            + spool_holder
            + power_supply_mount
            + screen_mount
            + mainboard_mount
            + raspberry_mount
            + endcap_left_back
            + endcap_left_front
            + endcap_right_back
            + endcap_right_front
            + power_plug_mount
            + z_bed_mount_left
            + z_bed_mount_right
            + z_bracket_bottom_left_back
            + z_bracket_bottom_left_front
            + z_bracket_bottom_right_back
            + z_bracket_bottom_right_front
            + z_bracket_top_left_front
            + z_bracket_top_left_back
            + z_bracket_top_right_front
            + z_bracket_top_right_back
            + z_stepper_mount_left
            + z_stepper_mount_right
            + z_top_endstop
            + z_bottom_endstop
            + motor_cable_guide
        ).color("#505050")
        + (
            x_carriage
            + x_axis_pulleys
            + cable_clamp_back
            + extruder_clamp
            + tunnel
            + cable_chain_carriage_attachment
            + cable_clamp_top
            + y_carriage_left
            + y_carriage_right
            + y_belt_fix_left
            + y_belt_fix_back
            + y_belt_fix_front
            + y_clamp_left
            + y_clamp_right
            + bed_bracket_front
            + bed_bracket_left
            + bed_bracket_right
            + thumbwheel_front
            + thumbwheel_left
            + thumbwheel_right
        ).color("orange")
        # + (frame_spacer + z_rod_spacer).color("green")
    ).render_to_file("muscad_printer")

    glass_plate_corner_left_front.render_to_file()
    glass_plate_corner_right_front.render_to_file()
    glass_plate_front_fix.render_to_file()
    feet_left_back.render_to_file()
    y_endstop_front.render_to_file()
    cable_clip.render_to_file()
    cable_chain_frame_attachment.render_to_file()
    raspberry_mount.render_to_file()
    bed_bracket_front.render_to_file()
    z_bed_mount_left.render_to_file()
    z_top_endstop.render_to_file()
    z_bottom_endstop.render_to_file()
    z_bracket_top_right_front.render_to_file("z_bracket_top_right_front")
    z_bracket_top_right_back.render_to_file("z_bracket_top_right_back")
    motor_cable_guide.render_to_file()

    if "--stl" in sys.argv:
        for part in (
            xy_idler_left,
            xy_idler_right,
            xy_idler_clamp_left,
            xy_stepper_mount_right,
            xy_stepper_mount_left,
            y_endstop_attachement_back,
            cable_chain_frame_attachment,
            cable_clamp_frame,
            extruder_stepper_mount,
            y_endstop_front,
            feet_left_back,
            spool_holder,
            power_supply_mount,
            screen_mount,
            mainboard_mount,
            raspberry_mount,
            endcap_left_back,
            power_plug_mount,
            z_bed_mount_left,
            z_bracket_bottom_left_back,
            z_bracket_bottom_left_front,
            z_bracket_top_left_front,
            z_bracket_top_left_back,
            z_stepper_mount_left,
            z_top_endstop,
            x_carriage,
            x_axis_pulleys,
            cable_clamp_back,
            extruder_clamp,
            tunnel,
            cable_chain_carriage_attachment,
            cable_clamp_top,
            y_carriage_left,
            y_carriage_right,
            y_belt_fix_left,
            y_belt_fix_back,
            y_belt_fix_front,
            y_clamp_left,
            bed_bracket_front,
            thumbwheel_front,
        ):
            part.export_stl()
