from __future__ import annotations

from muscad import Misc, Object, Part


def stack(*parts: Object | Misc, overlap: float = 0.01) -> Part:
    """Stack each part on top of each other.

    :param parts: all parts
    :param overlap: separation between each part (positive value: pieces will overlap, negative value: pieces will be separated)
    :return: parts stacked on top of each other, bottom to top.
    """
    s = Part()
    top = 0.0
    for part in parts:
        aligned_part = part.align(bottom=top - overlap)
        if isinstance(part, Misc):
            s.add_misc(aligned_part)
        else:
            s.add_child(aligned_part)
        top = aligned_part.top
    return s
