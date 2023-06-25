"""Tests for `muscad.vitamins.gears`."""
from muscad.vitamins.gears import BevelGear, Gear
from tests.conftest import compare_file


def test_gear() -> None:
    """Creates a simple gear."""
    gear = Gear(
        circular_pitch=700,
        gear_thickness=12,
        rim_thickness=15,
        hub_thickness=17,
        nb_holes=8,
    )
    compare_file(gear, "gear.scad")


def test_bevel_gear() -> None:
    """Creates a Bevel Gear Pair."""
    gear1, gear2 = BevelGear.pair()
    compare_file(gear1 + gear2, "bevel_gears_pair.scad")
