"""Tests for Extrusions."""

from muscad import Object
from muscad.vitamins.extrusions import Extrusion


def test_extrusion() -> None:
    """Bounding box checks."""
    extrusion: Object = Extrusion.e2020(30, T=0)
    assert extrusion.bottom == -15
    assert extrusion.top == 15
    assert extrusion.left == -10
    assert extrusion.right == 10
    assert extrusion.back == -10
    assert extrusion.front == 10

    extrusion = Extrusion.e2020(30, T=0).bottom_to_back()
    assert extrusion.bottom == -10
    assert extrusion.top == 10
    assert extrusion.left == -10
    assert extrusion.right == 10
    assert extrusion.back == -15
    assert extrusion.front == 15

    extrusion = Extrusion.e2020(30, T=0).bottom_to_left()
    assert extrusion.bottom == -10
    assert extrusion.top == 10
    assert extrusion.left == -15
    assert extrusion.right == 15
    assert extrusion.back == -10
    assert extrusion.front == 10
