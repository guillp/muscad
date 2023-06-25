"""A port of https://www.thingiverse.com/thing:3575 in MuSCAD."""
from typing import Iterable, Literal

from muscad import (
    EE,
    Circle,
    Cube,
    Cylinder,
    E,
    Object,
    Part,
    Polygon,
    Polyhedron,
    Union,
)
from muscad.helpers import asin, atan, catheti, cos, degrees, hypotenuse, pi, sin, tan
from muscad.point import Point2D, Point3D


class Gear(Part):
    def init(  # type: ignore[override]
        self,
        nb_teeth: int = 15,
        circular_pitch: float | None = None,
        diametral_pitch: float | None = None,
        pressure_angle: float = 28,
        clearance: float = 0.2,
        gear_thickness: float = 5,
        rim_thickness: float = 8,
        rim_width: float = 5,
        hub_thickness: float = 10,
        hub_diameter: float = 15,
        bore_diameter: float = 5,
        nb_holes: int = 0,
        backlash: float = 0,
        twist: float = 0,
        involute_facets: int | Literal["auto"] = "auto",
    ) -> None:
        if diametral_pitch and not circular_pitch:
            circular_pitch = 180 / diametral_pitch

        if not circular_pitch:
            raise ValueError(
                "gear module needs either a diametral_pitch or circular_pitch"
            )

        # Pitch diameter: Diameter of pitch circle
        pitch_diameter = nb_teeth * circular_pitch / 180
        pitch_radius = pitch_diameter / 2

        # Base Circle
        base_radius = pitch_radius * cos(pressure_angle)
        # Addendum: Radial distance from pitch circle to outside circle.
        addendum = pitch_diameter / nb_teeth
        # Outer Circle
        outer_radius = pitch_radius + addendum
        # Dedendum: Radial distance from pitch circle to root diameter
        dedendum = addendum + clearance

        # Root diameter: Diameter of bottom of tooth spaces.
        root_radius = pitch_radius - dedendum
        backlash_angle = backlash / pitch_radius * 180 / pi
        half_thick_angle = (360 / nb_teeth - backlash_angle) / 4

        # Variables controlling the rim.
        rim_radius = root_radius - rim_width

        gear = self.gear_shape(
            nb_teeth,
            pitch_radius=pitch_radius,
            root_radius=root_radius,
            base_radius=base_radius,
            outer_radius=outer_radius,
            half_thick_angle=half_thick_angle,
            involute_facets=involute_facets,
        ).linear_extrude(rim_thickness, convexity=10, twist=twist)
        if gear_thickness < rim_thickness:
            gear -= Cylinder(
                d=rim_radius * 2, h=rim_thickness - gear_thickness + E
            ).align(bottom=gear_thickness)

        self.add_child(gear, "gear")
        if gear_thickness > rim_thickness:
            self.add_child(Cylinder(d=rim_radius * 2, h=gear_thickness).align(bottom=0))
        if hub_thickness > gear_thickness:
            self.add_child(
                Cylinder(d=hub_diameter, h=hub_thickness - gear_thickness).align(
                    bottom=gear_thickness
                ),
                "axis",
            )

        self.add_hole(
            Cylinder(
                d=bore_diameter,
                h=2 + max(rim_thickness, hub_thickness, gear_thickness),
            ).align(bottom=-E),
            "rim",
        )
        if nb_holes > 0:
            # Variables controlling the circular holes in the gear.
            holes_circle_diameter = hub_diameter / 2 + rim_radius
            holes_circle_perimeter = pi * holes_circle_diameter

            # Limit the circle size to 90% of the gear face.
            hole_diameter = min(
                0.70 * holes_circle_perimeter / nb_holes,
                (rim_radius - hub_diameter / 2) * 0.9,
            )
            for i in range(nb_holes):
                self.add_hole(
                    Cylinder(
                        d=hole_diameter,
                        h=max(gear_thickness, rim_thickness) + EE,
                    )
                    .align(center_x=holes_circle_diameter / 2, bottom=-E)
                    .z_rotate(i * 360 / nb_holes)
                )

    @classmethod
    def gear_shape(
        cls,
        nb_teeth: int,
        pitch_radius: float,
        root_radius: float,
        base_radius: float,
        outer_radius: float,
        half_thick_angle: float,
        involute_facets: int | Literal["auto"] = "auto",
    ) -> Object:
        return Circle(segments=nb_teeth * 2, d=root_radius * 2) + Union(
            cls.involute_gear_tooth(
                pitch_radius=pitch_radius,
                root_radius=root_radius,
                base_radius=base_radius,
                outer_radius=outer_radius,
                half_thick_angle=half_thick_angle,
                involute_facets=involute_facets,
            ).z_rotate(i * 360 / nb_teeth)
            for i in range(1, nb_teeth + 1)
        )

    @staticmethod
    def involute_gear_tooth(
        pitch_radius: float,
        root_radius: float,
        base_radius: float,
        outer_radius: float,
        half_thick_angle: float,
        involute_facets: int | Literal["auto"] = "auto",
    ) -> Object:
        min_radius = max(base_radius, root_radius)
        pitch_angle = Point2D.involute(
            base_radius, involute_intersect_angle(base_radius, pitch_radius)
        ).angle()
        center_angle = pitch_angle + half_thick_angle

        start_angle = involute_intersect_angle(base_radius, min_radius)
        stop_angle = involute_intersect_angle(base_radius, outer_radius)

        if involute_facets == "auto":
            involute_facets = int(base_radius * pi / 200) or 5

        def iter_facets(involute_facets: int) -> Iterable[Polygon]:
            for i in range(1, involute_facets + 1):
                point1 = Point2D.involute(
                    base_radius,
                    start_angle
                    + (stop_angle - start_angle) * (i - 1) / involute_facets,
                ).z_rotate(center_angle)
                point2 = Point2D.involute(
                    base_radius,
                    start_angle + (stop_angle - start_angle) * i / involute_facets,
                ).z_rotate(center_angle)
                yield Polygon(
                    (0, 0),
                    point1,
                    point2,
                    point2.y_mirror(),
                    point1.y_mirror(),
                )

        return Union(iter_facets(involute_facets))


class BevelGear(Part):
    def init(  # type: ignore[override]
        self,
        nb_teeth: int = 11,
        cone_distance: float = 100,
        face_width: float = 20,
        outside_circular_pitch: float = 1000,
        pressure_angle: float = 30,
        clearance: float = 0.2,
        bore_diameter: float = 5,
        gear_thickness: float = 15,
        backlash: float = 0,
        involute_facets: int | Literal["auto"] = "auto",
        finish: Literal["bevel_gear_flat", "bevel_gear_back_cone"] | None = None,
        nb_holes: int = 0,
    ) -> None:
        outside_pitch_diameter = nb_teeth * outside_circular_pitch / 180
        outside_pitch_radius = outside_pitch_diameter / 2
        pitch_apex = catheti(cone_distance, outside_pitch_radius)
        pitch_angle = asin(outside_pitch_radius / cone_distance)

        if not finish:
            finish = "bevel_gear_flat" if pitch_angle < 45 else "bevel_gear_back_cone"

        apex_to_apex = cone_distance / cos(pitch_angle)
        back_cone_radius = apex_to_apex * sin(pitch_angle)

        # Calculate and display the pitch angle. This is needed to determine the angle to mount two meshing cone gears.

        # Base Circle for forming the involute teeth shape.
        base_radius = back_cone_radius * cos(pressure_angle)

        # Addendum: Radial distance from pitch circle to outside circle.
        addendum = outside_pitch_diameter / nb_teeth

        # Outer Circle
        outer_radius = back_cone_radius + addendum

        # Dedendum: Radial distance from pitch circle to root diameter
        dedendum = addendum + clearance
        dedendum_angle = atan(dedendum / cone_distance)
        root_angle = pitch_angle - dedendum_angle

        root_cone_full_radius = tan(root_angle) * apex_to_apex
        back_cone_full_radius = apex_to_apex / tan(pitch_angle)

        back_cone_end_radius = (
            outside_pitch_radius
            - dedendum * cos(pitch_angle)
            - gear_thickness / tan(pitch_angle)
        )
        back_cone_descent = dedendum * sin(pitch_angle) + gear_thickness

        # Root diameter: Diameter of bottom of tooth spaces.
        root_radius = back_cone_radius - dedendum

        half_tooth_thickness = (
            outside_pitch_radius * sin(360 / (4 * nb_teeth)) - backlash / 4
        )
        half_thick_angle = asin(half_tooth_thickness / back_cone_radius)

        face_cone_height = apex_to_apex - face_width / cos(pitch_angle)
        face_cone_full_radius = face_cone_height / tan(pitch_angle)
        face_cone_descent = dedendum * sin(pitch_angle)

        face_cone_end_radius = (
            outside_pitch_radius
            - face_width / sin(pitch_angle)
            - face_cone_descent / tan(pitch_angle)
        )

        # For the bevel_gear_flat finish option, calculate the height of a cube to select the portion of the gear that includes the full pitch face.
        bevel_gear_flat_height = pitch_apex - (cone_distance - face_width) * cos(
            pitch_angle
        )

        base = Cylinder(
            d=root_cone_full_radius * 2,
            d2=0,
            h=apex_to_apex,
            segments=nb_teeth * 2,
        ).align(bottom=pitch_apex - apex_to_apex).z_rotate(half_thick_angle) + Union(
            self.involute_bevel_gear_tooth(
                back_cone_radius=back_cone_radius,
                root_radius=root_radius,
                base_radius=base_radius,
                outer_radius=outer_radius,
                pitch_apex=pitch_apex,
                cone_distance=cone_distance,
                half_thick_angle=half_thick_angle,
                involute_facets=involute_facets,
            ).z_rotate(i * 360 / nb_teeth)
            for i in range(1, nb_teeth + 1)
        )
        if finish == "bevel_gear_back_cone":
            self.add_child(
                base
                & Cylinder(
                    d=back_cone_end_radius * 2,
                    d2=back_cone_full_radius * 4,
                    h=apex_to_apex + back_cone_descent,
                    segments=nb_teeth * 2,
                ).align(bottom=-back_cone_descent),
                comment="base",
            )
        else:
            self.add_child(
                base
                & Cube(
                    3 * outside_pitch_radius,
                    3 * outside_pitch_radius,
                    bevel_gear_flat_height,
                ).align(center_x=0, center_y=0, bottom=0),
                comment="base",
            )
        if finish == "bevel_gear_back_cone":
            self.add_hole(
                Cylinder(
                    d=face_cone_end_radius * 2,
                    d2=face_cone_full_radius * 4,
                    h=face_cone_height + face_cone_descent + pitch_apex,
                    segments=nb_teeth * 2,
                ).align(bottom=-face_cone_descent),
                "hollow_center",
            )
            if nb_holes > 0:
                # Variables controlling the circular holes in the gear.
                holes_circle_perimeter = pi * face_cone_end_radius

                # Limit the circle size to 60% of the gear face.
                circle_diameter = min(
                    0.70 * holes_circle_perimeter / nb_holes,
                    face_cone_end_radius * 0.6,
                )
                for i in range(nb_holes):
                    self.add_hole(
                        Cylinder(
                            d=circle_diameter,
                            h=apex_to_apex,
                        )
                        .align(
                            center_x=face_cone_end_radius / 2,
                            bottom=pitch_apex - apex_to_apex,
                        )
                        .z_rotate(i * 360 / nb_holes)
                    )

        self.add_hole(
            Cylinder(d=bore_diameter, h=apex_to_apex, segments=8).align(
                bottom=pitch_apex - apex_to_apex
            ),
            "bore",
        )

    @classmethod
    def pair(
        cls,
        nb_tooth1: int = 41,
        nb_tooth2: int = 16,
        axis_angle: float = 90,
        outside_circular_pitch: float = 1000,
        nb_holes1: int = 0,
        nb_holes2: int = 0,
    ) -> tuple[Object, Object]:
        outside_pitch_radius1 = nb_tooth1 * outside_circular_pitch / 360
        outside_pitch_radius2 = nb_tooth2 * outside_circular_pitch / 360

        pitch_apex1 = outside_pitch_radius2 * sin(axis_angle) + (
            outside_pitch_radius2 * cos(axis_angle) + outside_pitch_radius1
        ) / tan(axis_angle)
        cone_distance = hypotenuse(pitch_apex1, outside_pitch_radius1)
        pitch_apex2 = catheti(cone_distance, outside_pitch_radius2)

        pitch_angle1 = asin(outside_pitch_radius1 / cone_distance)
        pitch_angle2 = asin(outside_pitch_radius2 / cone_distance)

        return (
            cls(
                nb_teeth=nb_tooth1,
                cone_distance=cone_distance,
                pressure_angle=30,
                outside_circular_pitch=outside_circular_pitch,
                nb_holes=nb_holes1,
            )
            .up(20)
            .z_rotate(90),
            cls(
                nb_teeth=nb_tooth2,
                cone_distance=cone_distance,
                pressure_angle=30,
                outside_circular_pitch=outside_circular_pitch,
                nb_holes=nb_holes2,
            )
            .down(pitch_apex2)
            .y_rotate(-pitch_angle1 - pitch_angle2)
            .up(pitch_apex1 + 20)
            .z_rotate(90),
        )

    @staticmethod
    def involute_bevel_gear_tooth(
        back_cone_radius: float,
        root_radius: float,
        base_radius: float,
        outer_radius: float,
        pitch_apex: float,
        cone_distance: float,
        half_thick_angle: float,
        involute_facets: int | Literal["auto"] = "auto",
    ) -> Object:
        min_radius = max(base_radius * 2, root_radius * 2)
        pitch_angle = Point2D.involute(
            base_radius * 2,
            involute_intersect_angle(base_radius * 2, back_cone_radius * 2),
        ).angle()
        center_angle = pitch_angle + half_thick_angle
        start_angle = involute_intersect_angle(base_radius * 2, min_radius)
        stop_angle = involute_intersect_angle(base_radius * 2, outer_radius * 2)

        if involute_facets == "auto":
            involute_facets = int(base_radius * 3.14 / 200) or 5

        def iter_facets(involute_facets: int) -> Iterable[Polyhedron]:
            for i in range(1, involute_facets + 1):
                point1 = Point2D.involute(
                    base_radius * 2,
                    start_angle
                    + (stop_angle - start_angle) * (i - 1) / involute_facets,
                ).z_rotate(center_angle)
                point2 = Point2D.involute(
                    base_radius * 2,
                    start_angle + (stop_angle - start_angle) * i / involute_facets,
                ).z_rotate(center_angle)
                yield Polyhedron(
                    points=(
                        Point3D(back_cone_radius * 2 + 0.1, 0, cone_distance * 2),
                        point1.to_3d(),
                        point2.to_3d(),
                        point2.y_mirror().to_3d(),
                        point1.y_mirror().to_3d(),
                        (0.1, 0, 0),
                    ),
                    faces=(
                        (0, 1, 2),
                        (0, 2, 3),
                        (0, 3, 4),
                        (0, 5, 1),
                        (1, 5, 2),
                        (2, 5, 3),
                        (3, 5, 4),
                        (0, 4, 5),
                    ),
                )

        return (
            Union(iter_facets(involute_facets))
            .translate(x=-back_cone_radius * 2, z=-cone_distance * 2)
            .y_rotate(-atan(back_cone_radius / cone_distance))
            .up(pitch_apex)
        )


def involute_intersect_angle(base_radius: float, radius: float) -> float:
    return degrees(catheti(radius / base_radius, 1))


if __name__ == "__main__":
    Gear(
        circular_pitch=700,
        gear_thickness=12,
        rim_thickness=15,
        hub_thickness=17,
        nb_holes=8,
    ).render_to_file()
    gear1, gear2 = BevelGear.pair(nb_tooth1=40, nb_tooth2=40, nb_holes1=6, nb_holes2=4)
    (gear1 + gear2).render_to_file("gear_pair")
