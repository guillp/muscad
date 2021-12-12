from muscad import Cylinder
from muscad import E
from muscad import Part
from muscad.utils.volume import Volume


class StepperMotor(Part):
    def init(self, width, height, chamfer=4):
        self.body = Volume(
            center_x=0,
            width=width,
            center_y=0,
            depth=width,
            bottom=0,
            height=height,
        ).chamfer_height(chamfer)

    def add_bolts(self, bolt, spacing, depth=3, holes=(0, 1, 2, 3)):
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
            .align(bottom=self.body.top - depth)
            .misc()
        )
        return self

    def add_central_bulge(self, d, h):
        """
        Adds the cylindric bulge on the shaft side of the stepper.
        :param d: diameter of the bulge
        :param h: height of the bulge
        :return: the stepper object, with bulge added
        """
        self.central_bulge = (
            Cylinder(d=d, h=h + 1)
            .align(center_x=0, center_y=0, top=self.top + h)
            .misc()
        )
        return self

    def add_gearbox(
        self, d, h, bolt=None, bolt_spacing=None, holes=(0, 1, 2, 3), depth=5
    ):
        """
        Adds the gearbox on the shaft side of the stepper
        :param d: diameter of the gearbox
        :param h: height of the gearbox
        :return: the stepper object, with gearbox added
        """
        self.gearbox = Cylinder(d=d, h=h + E).align(
            center_x=self.body.center_x,
            center_y=self.body.center_y,
            top=self.body.top + h,
        )

        if bolt and bolt_spacing:
            radius = ((bolt_spacing ** 2) * 2) ** 0.5 / 2
            self.bolts = (
                sum(bolt.rightward(radius).z_rotate(45 + 90 * i) for i in holes)
                .align(bottom=self.gearbox.top - depth)
                .misc()
            )

        return self

    def add_shaft(self, d, length):
        """
        Adds a shaft.
        :param d: diameter of the shaft
        :param length: lenght of the shaft
        :return: the stepper object, with shaft added
        """
        self.shaft = (
            Cylinder(d=d, h=length + 2)
            .align(center_x=0, center_y=0, bottom=self.top - E)
            .misc()
        )
        return self

    @classmethod
    def nema17(
        cls,
        height=42,
        gearbox_height=0,
        bulge_height=3,
        shaft_diameter=5,
        shaft_height=25,
        bolt=None,
        holes=(0, 1, 2, 3),
        T=0.2,
    ):
        """
        Makes a Nema17 stepper.
        :param height: height of the stepper
        :param bulge_height: height of the central bulge. Use it to make a gearbox.
        :param shaft_height: lenght of the shaft
        :param bolt: bolts to add (must be M3 bolts, head up)
        :param holes: holes index to screw bolts in
        :param T: tolerance
        :return: a StepperMotor
        """
        width = 42.3
        spacing = 31.04
        nema = cls(width, height)

        if gearbox_height:
            nema.add_gearbox(
                d=36 + 2 * T,
                h=gearbox_height,
                bolt=bolt,
                bolt_spacing=20,
                depth=5,
            )
        elif bolt:
            nema.add_bolts(bolt=bolt, spacing=spacing, depth=3, holes=holes)
        nema.add_central_bulge(d=22 + 2 * T, h=bulge_height)
        nema.add_shaft(d=shaft_diameter + 2 * T, length=shaft_height)
        return nema

    @property
    def center_x(self):
        return 0

    @property
    def center_y(self):
        return 0
