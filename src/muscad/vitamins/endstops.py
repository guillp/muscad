from typing_extensions import Self

from muscad import Circle, Cube, Cylinder, Hull, Object, Part, Volume
from muscad.utils.surface import Surface
from muscad.utils.tube import Tube
from muscad.vitamins.bolts import Bolt


class OptoSwitch(Part):
    base = Volume(width=24.5, depth=3.5, height=6.4)
    left_side = Volume(
        width=4.45,
        depth=11.3,
        height=6.3,
        left=base.left + 6.63,
        back=base.back,
        bottom=base.bottom,
    )
    right_side = Volume(
        width=4.45,
        depth=11.3,
        height=6.3,
        right=base.right - 6.63,
        back=base.back,
        bottom=base.bottom,
    )

    left_hole = ~Cylinder(d=3, h=4.5).bottom_to_front().align(
        center_x=base.left + 2.75,
        center_y=base.center_y,
        center_z=base.center_z,
    )
    right_hole = ~Cylinder(d=3, h=4.5).bottom_to_front().align(
        center_x=base.right - 2.75,
        center_y=base.center_y,
        center_z=base.center_z,
    )


class OpticalEndstop(Part):
    base = Volume(width=33, depth=1.6, height=10.5).color("red")
    switch = OptoSwitch().align(right=base.right - 0.1, back=base.front, center_z=base.center_z).color("grey")
    connector = (
        Volume(
            width=5.8,
            depth=7,
            height=10.5,
            left=base.left - 0.2,
            front=base.back,
            center_z=base.center_z,
        )
        .color("white")
        .misc()
    )
    led = Volume(
        width=2,
        depth=0.7,
        height=1.5,
        center_x=4.5,
        back=base.front,
        center_z=base.center_z,
    ).color("blue")
    left_hole = ~Cylinder(d=3, h=4.5).bottom_to_front().align(
        center_x=switch.left + 2.75,
        center_y=base.center_y,
        center_z=base.center_z,
    )
    right_hole = ~Cylinder(d=3, h=4.5).bottom_to_front().align(
        center_x=switch.right - 2.75,
        center_y=base.center_y,
        center_z=base.center_z,
    )

    def add_bolts(self, bolt: Object) -> Self:
        self.left_bolt = (
            bolt.bottom_to_front()
            .align(
                center_x=self.left_hole.center_x,
                front=self.switch.base.front,
                center_z=self.left_hole.center_z,
            )
            .misc()
        )
        self.right_bolt = (
            bolt.bottom_to_front()
            .align(
                center_x=self.right_hole.center_x,
                front=self.switch.base.front,
                center_z=self.right_hole.center_z,
            )
            .misc()
        )
        return self


class BIQUEndstop(Part):
    body = Surface.free(Circle(d=7).align(center_x=-10), Circle(d=7).align(center_x=10)).z_linear_extrude(
        bottom=0, top=1
    )
    endstop = Volume(
        width=13,
        depth=6,
        height=4,
        center_x=body.center_x,
        back=body.front,
        bottom=body.top,
    )


class MechanicalSwitchEndstop(Part):
    body = Volume(width=14, depth=6, height=6)
    switch = (
        Volume(width=1, depth=1, height=6)
        .align(
            center_x=body.left + 3,
            back=body.front,
            center_z=body.center_z,
        )
        .misc()
    )
    lever = (
        (
            Volume(width=13.5, depth=0.5, height=6).align(right=0, back=0)
            + (Cube(10, 10, 20).y_translate(5.5) & (Cylinder(d=4, h=6) - Cylinder(d=3, h=7))).translate(x=1.5, y=-0.5)
        )
        .align(left=body.left, back=body.front)
        .z_rotate(15, center_x=body.left, center_y=body.front)
        .misc()
    )


class InductionSensor(Part):
    def init(self, diameter: float, length: float) -> None:  # type: ignore[override]
        self.sensor = Cylinder(d=diameter, h=length)

    @classmethod
    def LJ12A3(cls, T: float = 0.2) -> Self:
        return cls(12 + 2 * T, 60)


class MechanicalEndstopOnPCB(Part):
    pcb = Volume(width=40, depth=16, height=1.6)
    switch = MechanicalSwitchEndstop().align(right=pcb.right - 6, front=pcb.front, bottom=pcb.top)
    connector = Volume(width=10, depth=10, height=6).align(left=pcb.left, center_y=pcb.center_y, bottom=pcb.top)

    switch_welds = (
        Volume(
            center_x=switch.center_x,
            width=switch.width,
            center_y=pcb.center_y,
            depth=4,
            top=pcb.bottom,
            height=2,
        )
        .fillet_width(1, bottom=True)
        .fillet_depth(1, bottom=True)
        .misc()
    )
    connector_welds = (
        Volume(
            center_x=connector.right,
            width=3,
            center_y=pcb.center_y,
            depth=connector.depth,
            top=pcb.bottom,
            height=2,
        )
        .fillet_width(1, bottom=True)
        .fillet_depth(1, bottom=True)
        .misc()
    )

    def init(self, bolt: Object = Bolt.M3(10).add_nut(-3), z_offset: float = -3) -> None:  # type: ignore[override]
        if bolt:
            self.bolts = (
                bolt.bottom_to_top()
                .align(
                    center_x=self.pcb.right - 3.5,
                    center_y=self.pcb.front - 2.5,
                )
                .z_translate(z_offset)
                .x_symmetry(self.switch.center_x)
                .misc()
            )


class BLTouchClassic(Part):
    attachment = (
        Hull(
            Surface.square(width=6, depth=11.53),
            Surface.circle(radius=4, center_x=9).x_symmetry(),
        )
        - Surface.circle(diameter=3.2, center_x=9).x_symmetry()
    ).z_linear_extrude(2.3)
    cylinder = Tube(diameter=11, top=attachment.bottom, height=7.7)
    body = Tube(diameter=13, top=cylinder.bottom, height=26.3) & Volume(
        width=13, depth=11.53, top=cylinder.bottom, height=27
    ) - Surface.chamfer(12).align(right=0).z_rotational_extrude(bottom=cylinder.bottom - 30)
    pin = Tube(diameter=2, top=body.bottom, height=11)

    def init(  # type: ignore[override]
        self, bolt: Object = Bolt.M3(20).add_nut(-4, inline_clearance_size=10)
    ) -> None:
        self.bolts = bolt.align(center_x=9, bottom=self.attachment.bottom - 3).x_symmetry().misc()
