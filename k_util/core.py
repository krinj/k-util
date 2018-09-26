# -*- coding: utf-8 -*-

"""
Some core stuff like lerping n' shit.
"""

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


def interpolate_color(c1, c2, factor: float) -> list:
    """ Linear interpolate two 3-channel colors, using channel based interpolation. """
    assert(len(c1) == len(c2))

    new_color = []
    for i in range(len(c1)):
        new_color.append(int(interpolate(c1[i], c2[i], factor)))
    return new_color


def interpolate(f1: float, f2: float, factor: float) -> float:
    """ Linearly interpolate between two float values. """
    return f1 + (f2 - f1) * factor


def filter_value(old: float, new: float, factor: float) -> float:
    """ Linearly interpolate between two float values. """
    r_factor: float = 1 - factor
    return old * r_factor + new * factor
