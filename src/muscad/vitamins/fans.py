from muscad import Cylinder
from muscad import E
from muscad import Hull
from muscad import Part
from muscad.utils.volume import Volume
from muscad.vitamins.bolts import Bolt


class Blower(Part):
    def init(
        self,
        *,
        diameter,
        blower_width,
        height,
        blower_clearance=20,
        bolt=None,
    ):
        self.fan = Cylinder(d=diameter, h=height)
        self.blower = Volume(
            left=self.fan.left - 1.5,
            width=blower_width,
            back=self.fan.center_y,
            front=self.fan.front + blower_clearance,
            bottom=self.fan.bottom,
            top=self.fan.top,
        ).misc()
        self._back_bolt_holder = Cylinder(d=bolt.diameter + 2, h=height).align(
            center_x=self.fan.center_x - 23,
            center_y=self.fan.center_y - 19,
            bottom=self.fan.bottom,
        )
        self._front_bolt_holder = Cylinder(d=bolt.diameter + 2, h=height).align(
            center_x=self.fan.center_x + 19.5,
            center_y=self.fan.center_y + 19.3,
            bottom=self.fan.bottom,
        )
        self.bolt_holders = Hull(self._back_bolt_holder, self._front_bolt_holder)
        if bolt:
            self.back_bolt = bolt.align(
                center_x=self._back_bolt_holder.center_x,
                center_y=self._back_bolt_holder.center_y,
                bottom=self.bottom - 3,
            ).misc()

            self.front_bolt = bolt.align(
                center_x=self._front_bolt_holder.center_x,
                center_y=self._front_bolt_holder.center_y,
                bottom=self.bottom - 3,
            ).misc()

    @classmethod
    def blower50x50x15(
        cls, bolt=Bolt.M4(20).add_nut(-E, inline_clearance_size=20), T=0.2
    ):
        return cls(
            blower_width=19 + 2 * T,
            diameter=50 + 2 * T,
            height=15 + 2 * T,
            bolt=bolt,
        )


class Fan(Part):
    def init(self, *, width, height, r):
        self.body = Volume(
            width=width,
            center_x=0,
            depth=width,
            center_y=0,
            height=height,
            center_z=0,
        ).fillet_height(r)

    def add_bolts(self, bolt, spacing, holes=(0, 1, 2, 3)):
        """
        Add up to 4 bolts in the stepper fixing holes (as miscellaneous items)
        :param bolt: the bolt to add (must be head up)
        :param spacing: edge distance between 2 bolt centers
        :param depth: depth of the fixing holes inside the stepper
        :param holes: index of the bolts to add. Modify it if you only want 2 or 3 bolts.
        :return: the stepper object, with bolts added
        """
        radius = ((spacing ** 2) * 2) ** 0.5 / 2
        self.bolts = (
            sum(bolt.rightward(radius).z_rotate(45 + 90 * i) for i in holes)
            .align(bottom=self.body.bottom)
            .misc()
        )
        return self

    def add_tunnel(self, diameter, length, d2=None):
        self.tunnel = (
            Cylinder(d=diameter, d2=d2, h=length)
            .align(
                center_x=self.body.center_x,
                center_y=self.body.center_y,
                center_z=self.body.center_z,
            )
            .misc()
        )
        return self

    @classmethod
    def fan40x40x20(cls, bolts=True, bolt=Bolt.M3(25).add_nut(-E), T=0.2):
        fan = cls(width=40 + 2 * T, height=20 + 2 * T, r=2)
        if bolts:
            fan.add_bolts(bolt, 32)
        return fan
