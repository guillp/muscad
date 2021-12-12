"""Contains fixtures and common utilities for all test cases."""
import os

from muscad import Object


def compare_file(part: Object, scad_file: str) -> bool:
    """Compares a part render to the target .scad file on the filesystem."""
    filepath = os.path.join(os.path.dirname(__file__), "target_scad_files", scad_file)
    with open(filepath, "rt") as finput:
        scad = "".join(finput.readlines()).strip()
    return compare_str(part, scad)


def compare_str(part: Object, scad: str) -> bool:
    """Compares a part render to the given string."""
    render = part.render()
    for line1, line2 in zip(render.split("\n"), scad.split("\n")):
        assert (
            line1.strip() == line2.strip()
        ), f"rendered: {render}\n\nexpected:\n{scad}"
    return True
