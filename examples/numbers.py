from muscad import Cylinder, E, Part, Polygon, T, Text


class Screw(Part):
    body = Cylinder(h=8, d=3.8)
    head = (
        Polygon((0, 0), (3.9, 0), (3.9, -0.4), (1.9, -3), (0, -2.8))
        .z_rotational_extrude()
        .align(bottom=body.top - E)
    )


class Number1(Part):
    number = (
        Text("1", size=75, direction="ttb", valign="center", font="Sancreek")
        .z_linear_extrude(5)
        .leftward(0.3)
        .backward(0.8)
    )
    screws = (
        ~Screw().align(center_x=0, center_y=30, top=number.top + T).y_mirror(keep=True)
    )


class Number2(Part):
    number = (
        Text("2", size=75, direction="ttb", valign="center", font="Sancreek")
        .z_linear_extrude(5)
        .leftward(0.3)
        .backward(0.8)
    )
    screw1 = ~Screw().align(center_x=-3, center_y=-34, top=number.top + T)
    screw2 = ~Screw().align(center_x=14, center_y=21, top=number.top + T)
    screw3 = ~Screw().align(center_x=-17, center_y=21, top=number.top + T)


class Number3(Part):
    number = (
        Text("3", size=75, direction="ttb", valign="center", font="Sancreek")
        .z_linear_extrude(5)
        .leftward(0.3)
        .backward(0.8)
    )
    screws = (
        ~Screw()
        .align(center_x=16, center_y=24, top=number.top + T)
        .y_mirror(keep=True)
        .x_mirror(keep=True)
    )


class Number4(Part):
    number = (
        Text("4", size=75, direction="ttb", valign="center", font="Sancreek")
        .z_linear_extrude(5)
        .leftward(0.3)
        .backward(0.8)
    )
    screws_right = (
        ~Screw()
        .align(center_x=10, center_y=10, top=number.top + T)
        .y_mirror(-10, keep=True)
    )
    screw_top = ~Screw().align(center_x=-4, center_y=32, top=number.top + T)
    screw_left = ~Screw().align(center_x=-22, center_y=-19, top=number.top + T)


class Number5(Part):
    number = (
        Text("5", size=75, direction="ttb", valign="center", font="Sancreek")
        .z_linear_extrude(5)
        .leftward(0.3)
        .backward(0.8)
    )
    screw1 = ~Screw().align(center_x=17, center_y=-12, top=number.top + T)
    screw2 = ~Screw().align(center_x=12, center_y=31, top=number.top + T)
    screw3 = ~Screw().align(center_x=-16, center_y=-20, top=number.top + T)


if __name__ == "__main__":
    Screw().render_to_file("screw.scad")
    Number1().render_to_file("number1.scad")
    Number2().render_to_file("number2.scad")
    Number3().render_to_file("number3.scad")
    Number4().render_to_file("number4.scad")
    Number5().render_to_file("number5.scad")
