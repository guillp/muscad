"""Tests for `muscad.vitamins.gears`."""
from tests.conftest import compare_file

from muscad.vitamins.gears import BevelGear
from muscad.vitamins.gears import Gear


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
    bevel_gears_pair = BevelGear.pair()
    compare_file(bevel_gears_pair, "bevel_gears_pair.scad")
